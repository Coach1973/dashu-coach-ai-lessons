-- 活動報名系統：來賓掃QR填資料，同一人跨活動只留一筆
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,          -- 網址用的短名，例如 ai-talk-0729
    name TEXT NOT NULL,                 -- 活動名稱
    event_date TEXT,                    -- 活動日期 YYYY-MM-DD
    start_time TEXT,                    -- 開始時間 HH:MM，同一天有多場時用來判斷auto模式該導去哪一場
    is_current INTEGER NOT NULL DEFAULT 0,  -- 1=固定QR立牌(/checkin)目前導向這場，同時只能有一筆是1
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS attendees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,         -- 正規化後的手機號（只留數字），同一人的身分證
    company_title TEXT,                 -- 公司／職稱（選填）
    line_user_id TEXT,                  -- 來賓在LINE傳問候訊息後比對到的身分，用來之後精準群發
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendee_id INTEGER NOT NULL REFERENCES attendees(id),
    event_id INTEGER NOT NULL REFERENCES events(id),
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE (attendee_id, event_id)      -- 同一人同一場只算一次
);

-- 簡單的key-value設定表，目前只放一筆：/checkin的切換模式
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- 抽獎轉盤：中獎名單直接查signups當名單來源，這裡只記「誰在這場抽中過」避免重複抽中
CREATE TABLE IF NOT EXISTS wheel_winners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL REFERENCES events(id),
    attendee_id INTEGER NOT NULL REFERENCES attendees(id),
    prize TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE (event_id, attendee_id)
);

-- 獎品清單：這場活動有哪些獎項、各自總數/剩餘數，轉盤下拉選單直接讀這裡，抽中自動扣庫存
CREATE TABLE IF NOT EXISTS wheel_prizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL REFERENCES events(id),
    name TEXT NOT NULL,
    total_qty INTEGER NOT NULL,
    remaining_qty INTEGER NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

-- 台南應用科技大學校友會「召集令」加入表單（2026-09-03交辦，聯想已完成前端，這裡接資料庫）
-- 5個分會共用同一張表，chapter欄位分流；同時服務event.bymyway.com/tut跟GitHub Pages兩個入口
CREATE TABLE IF NOT EXISTS tut_alumni_signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    grad_year TEXT,                      -- 畢業年，選填，格式不固定(民國/西元皆可能)不正規化
    department TEXT,                     -- 科系，選填
    chapter TEXT NOT NULL,               -- 台南/台中/高雄/台北/嘉義
    source TEXT,                         -- bymyway 或 github-pages，方便追蹤是哪個入口送出
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 「領導人溝通的藝術」9/10培訓報名（2026-09-03交辦，design(4).html邀請函+報名表單）
CREATE TABLE IF NOT EXISTS leader_workshop_signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    source TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 「人生四席・一日共鳴」10/10淺山綠茶席報名（2026-09-03交辦，Designs.zip落地頁）
CREATE TABLE IF NOT EXISTS event_1010_signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    source TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 教練個人待辦事項（2026-09-02交辦，仿Microsoft To Do核心功能），reminder_sent由
-- scripts/todo_reminder_check.py這支獨立cron檢查remind_at並發Telegram，避免跟網頁請求耦合
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    notes TEXT,
    due_date TEXT,                       -- 到期日 YYYY-MM-DD，選填
    remind_at TEXT,                      -- 提醒時間 YYYY-MM-DD HH:MM，選填，時間到會發Telegram
    completed INTEGER NOT NULL DEFAULT 0,
    reminder_sent INTEGER NOT NULL DEFAULT 0,
    reminder_cron_id TEXT,               -- 對應的OpenClaw一次性cron job id，完成/刪除時要取消
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    completed_at TEXT
);

-- coach888作品一覽的排版狀態(2026-09-03交辦)：教練反映在Mac改完排版，ACER開起來還是舊的，
-- 因為原本純靠每個瀏覽器自己的localStorage存檔，不同裝置/清快取就各自獨立、互不同步。
-- 這張表把layout/titles/badges/names/collapse五組狀態集中存一份，取代「靠localStorage各自
-- 為政+手動複製貼給AI固化」的舊流程，coach888的JS改成save時順便POST這裡、load時先GET這裡。
CREATE TABLE IF NOT EXISTS coach888_state (
    key TEXT PRIMARY KEY,                -- coach888_layout / coach888_titles / coach888_badges / coach888_names / coach888_collapse
    value TEXT NOT NULL,                 -- JSON字串，格式跟原本存進localStorage的值完全一致
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 教練課程教材線上觀看區(2026-09-04交辦)：教練把PPT/PDF上傳Google雲端硬碟(檢視者權限)，
-- 這裡只存Drive檔案ID+標題，實際檔案渲染交給Google Drive自己的embed viewer(iframe /preview)，
-- 學員在我們自己的網址看到品牌一致的清單頁，但不需要自建PDF轉檔/儲存管線。
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    drive_file_id TEXT NOT NULL,         -- 從Drive分享連結擷取出的檔案ID
    file_type TEXT,                      -- ppt / pdf，純顯示用標籤
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
