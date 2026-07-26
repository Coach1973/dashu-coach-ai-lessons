-- 結繩領導學工作坊（台南／台中／台北）報名＋繳費戰報，工作人員手動輸入
CREATE TABLE IF NOT EXISTS registrants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workshop TEXT NOT NULL,             -- '台南' | '台中' | '台北'
    name TEXT NOT NULL,
    phone TEXT,
    register_date TEXT NOT NULL,        -- YYYY-MM-DD，預設今天
    paid INTEGER NOT NULL DEFAULT 0,    -- 0=未繳費 1=已繳費
    paid_method TEXT,                   -- 'ATM' | 'PAYUNi' | '其他'
    paid_date TEXT,                     -- YYYY-MM-DD
    amount INTEGER,
    note TEXT,
    referrer TEXT,                       -- 邀請人：自由輸入（實際邀請人不限於固定名單）
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
