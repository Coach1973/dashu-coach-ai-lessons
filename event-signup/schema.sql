-- 活動報名系統：來賓掃QR填資料，同一人跨活動只留一筆
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,          -- 網址用的短名，例如 ai-talk-0729
    name TEXT NOT NULL,                 -- 活動名稱
    event_date TEXT,                    -- 活動日期 YYYY-MM-DD
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
