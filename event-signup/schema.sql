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
-- 校友回憶牆投稿（2026-10-02），實際由 app.py _memwall_conn() 自動建表：pending→教練Telegram審核→approved才公開
CREATE TABLE IF NOT EXISTS memwall_notes (
    id TEXT PRIMARY KEY, slug TEXT NOT NULL, name TEXT, year TEXT, color TEXT,
    txt TEXT NOT NULL, photo_file TEXT, status TEXT NOT NULL DEFAULT 'pending',
    ip TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')), reviewed_at TEXT
);

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

-- 大臺南商圈整合計劃店家登錄（2026-09-04交辦，大台南策展中心店家招募落地頁）
CREATE TABLE IF NOT EXISTS tainan_shangquan_signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,       -- 填表人姓名
    shop TEXT NOT NULL,       -- 店名
    category TEXT NOT NULL,   -- 食/衣/住/行/育/樂
    contact TEXT NOT NULL,    -- 電話或LINE ID
    address TEXT NOT NULL,    -- 店家地址
    social TEXT,              -- FB/IG連結，選填
    items TEXT,               -- 想被推薦的招牌商品，選填
    source TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- KR養生廚房線上留言（2026-09-04交辦，Tooo.ai示範站整頁搬遷）
CREATE TABLE IF NOT EXISTS kr_contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    subject TEXT,
    message TEXT NOT NULL,
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

-- coach888作品一覽「熱門排行」點擊次數(2026-09-18教練交辦)：教練想依實際點擊次數
-- 自動排出常用項目，不用每次在一堆手動整理的分類裡找。每個url累計次數，前端獨立
-- 顯示成「🔥熱門排行」區塊，完全不影響教練手動拖曳整理的原始分類/順序。
CREATE TABLE IF NOT EXISTS coach888_clicks (
    url TEXT PRIMARY KEY,
    click_count INTEGER NOT NULL DEFAULT 0,
    last_clicked_at TEXT
);

-- 教練課程教材線上觀看區(2026-09-04交辦，同日追加link_type支援整個資料夾)：
-- 教練把PPT/PDF/圖片上傳Google雲端硬碟(檢視者權限)，這裡只存Drive檔案或資料夾ID，
-- 實際渲染交給Google Drive自己的embed viewer(單檔iframe /preview，整個資料夾用
-- embeddedfolderview)，學員在我們自己的網址看到品牌一致的清單頁，不需要自建轉檔/儲存管線。
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    drive_file_id TEXT NOT NULL,         -- 從Drive分享連結擷取出的檔案ID或資料夾ID
    file_type TEXT,                      -- ppt / pdf / image，純顯示用標籤
    link_type TEXT NOT NULL DEFAULT 'file',  -- file=單一檔案 / folder=整個資料夾(自動列出裡面所有檔案)
    visible INTEGER NOT NULL DEFAULT 1,  -- 1=學員看得到 / 0=僅在管理清單勾選區看得到，還沒公開
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 講座互動牆（2026-09-19交辦，中正大學社團幹部專場9/19早上場，原始需求是教練用tava-ai.com
-- 生成的獨立WordPress外掛包，改直接併入我們自己的event-signup，不用另外裝WordPress/管另一組帳密）：
-- 提問+按讚+即時回饋+課後影音共用一張表(kind區分)，event欄位對應前端EVENT_ID，
-- 換一個EVENT_ID就能給下一場活動重複使用同一套後端。
CREATE TABLE IF NOT EXISTS event_wall_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,            -- 前端產生的uuid，做寫入去重
    event TEXT NOT NULL,                 -- 對應前端EVENT_ID，例如ccu-club-leadership
    kind TEXT NOT NULL,                  -- question / echo
    topic TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    votes INTEGER NOT NULL DEFAULT 0,
    answered INTEGER NOT NULL DEFAULT 0,
    ts INTEGER NOT NULL DEFAULT 0,       -- 前端用毫秒時間戳排序
    ip_hash TEXT NOT NULL DEFAULT ''     -- 只存雜湊，不留原始IP
);
CREATE INDEX IF NOT EXISTS idx_event_wall_items_event_kind ON event_wall_items(event, kind);

-- 課後影音清單用app_settings存(key格式 event_wall_media_<event>，value是JSON陣列)，
-- 跟講者金鑰(key格式 event_wall_key_<event>)共用同一張既有key/value表，不必新增資料表。
