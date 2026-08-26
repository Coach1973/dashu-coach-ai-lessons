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
    bni_status TEXT DEFAULT 'unknown',  -- unknown / bni_member / not_bni
                                 -- 只對「已經有真實聯絡資料的人」標示才有意義，
                                 -- AI建議的抽象待招募角色(chain_members.is_gap=1)
                                 -- 沒有聯絡方式，標示會員與否沒有實際用途(教練親定)
    bni_note TEXT,               -- 選填備註，如「真誠分會」
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

-- 產業鏈：AI動態判斷/累積形成的產業鏈主題（不是預先寫死，隨名片收錄逐漸成形）
CREATE TABLE IF NOT EXISTS industry_chains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    core_theme TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 名片與產業鏈的關聯：這張名片適合放進哪條產業鏈的哪個角色位置
-- card_id為NULL代表這個角色位置目前是空缺(待招募)——這種AI建議的抽象角色
-- 沒有真實聯絡資料，不適合標示BNI會員狀態，那個標示掛在cards表(見上方)，
-- 只對「已經有真人聯絡資料」的名片才有意義(教練親定)
CREATE TABLE IF NOT EXISTS chain_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chain_id INTEGER NOT NULL REFERENCES industry_chains(id),
    card_id INTEGER REFERENCES cards(id),
    role_name TEXT NOT NULL,
    is_gap INTEGER DEFAULT 0,
    match_reason TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_chain_members_chain ON chain_members(chain_id);
CREATE INDEX IF NOT EXISTS idx_chain_members_card ON chain_members(card_id);

-- 團隊成員（教練+白名單，跟進紀錄簿登入用）
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 跟進狀態：一張名片一筆，代表目前跟進到哪個階段
CREATE TABLE IF NOT EXISTS follow_ups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER NOT NULL UNIQUE REFERENCES cards(id),
    stage TEXT DEFAULT '待邀約',
    assigned_to TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 跟進聯絡明細：每次聯絡累加一筆，保留完整歷程
CREATE TABLE IF NOT EXISTS follow_up_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follow_up_id INTEGER NOT NULL REFERENCES follow_ups(id),
    channel TEXT,
    content TEXT,
    logged_by TEXT,
    contacted_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_follow_up_logs_followup ON follow_up_logs(follow_up_id);

-- BNI Connect大台南南區「來賓」名單(訪客，非會員)，來源：地區-查看來賓報告
-- 同一人常有多筆訪問紀錄(不同分會/日期/職業)，依電話去重後每人一筆，
-- company/profession/chapter取該人「最新一次」訪問紀錄的值(2026-08-26補齊，
-- 原始三欄版漏抓了報表本來就有的公司/職業欄位)
CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT,
    email TEXT,
    company TEXT,
    profession TEXT,
    chapter TEXT,
    source TEXT DEFAULT 'bniconnect_region_visitor_report',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_guests_name ON guests(name);
CREATE INDEX IF NOT EXISTS idx_guests_mobile ON guests(mobile);
