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
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    completed_at TEXT
);
