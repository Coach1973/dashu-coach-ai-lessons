CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_filename TEXT UNIQUE NOT NULL,
    name TEXT,
    title TEXT,
    company TEXT,
    mobile TEXT,
    landline TEXT,
    email TEXT,
    line_id TEXT,
    website TEXT,
    address TEXT,
    tagline TEXT,
    category TEXT,
    keywords TEXT,              -- JSON array 字串
    confidence_notes TEXT,
    raw_response TEXT,          -- AI原始回應，除錯用
    status TEXT DEFAULT 'ok',   -- ok / needs_review / failed
    extra_images TEXT,          -- 同一張名片的其他照片(如背面)，逗號分隔檔名
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id_a INTEGER NOT NULL REFERENCES cards(id),
    card_id_b INTEGER NOT NULL REFERENCES cards(id),
    relation_reason TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(card_id_a, card_id_b)
);

CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_company ON cards(company);
CREATE INDEX IF NOT EXISTS idx_cards_category ON cards(category);
