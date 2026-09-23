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
    source_guest_id INTEGER REFERENCES guests(id),  -- 由guests表「媒合」按鈕
                                 -- 首次點擊時轉入的來賓，避免重複轉入同一人
    uploaded_by TEXT,            -- 2026-09-02教練拍板：全站改需登入才能用，
                                 -- 上傳名片時記錄登入者display_name，才知道是誰上傳的
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
-- idx_cards_source_guest_id：只在db.py的init_db()建立(既有DB要先ALTER加欄位
-- 才能建索引，寫在這裡對舊DB會在欄位補上前就先執行而報錯)

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

-- 團隊成員（教練+白名單，跟進紀錄簿登入用）。2026-09-02教練拍板：查詢/瀏覽
-- 全站不需要帳號，只有「跟進」功能需要，開放給領導團隊/DNA自助申請帳號
-- （姓名+行動電話，密碼統一預設88888），教練後台審核通過才能登入。
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,      -- 手機號碼或教練手動建立的帳號名
    password_hash TEXT NOT NULL,
    display_name TEXT,
    status TEXT DEFAULT 'approved',     -- pending / approved / rejected
                                         -- 教練既有手動建立的帳號預設approved(不受影響)，
                                         -- 自助申請的新帳號預設pending，需教練審核
    applied_at TEXT DEFAULT (datetime('now')),
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

-- 來賓完整訪問歷程(2026-09-02)：guests表只保留「最新一次」訪問的分會/職業，
-- 教練指出這樣看不到來賓是哪個分會、什麼時候來過——同一人常有多筆不同分會/
-- 不同日期的訪問紀錄，來源：「地區-查看來賓」完整歷史報表(含訪問日期欄位)
CREATE TABLE IF NOT EXISTS guest_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER NOT NULL REFERENCES guests(id),
    chapter TEXT,
    visit_date TEXT,
    company TEXT,
    profession TEXT,
    invited_by TEXT,
    visit_type TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(guest_id, chapter, visit_date)
);

CREATE INDEX IF NOT EXISTS idx_guest_visits_guest ON guest_visits(guest_id);

-- BNI Connect大台南南區5分會離會會員「信用証」開立狀況清查(2026-08-27)，
-- 供 /bni-credit 網頁追蹤到期日+面額，教練可在網頁上直接改狀態(cert_status/usage_status)
CREATE TABLE IF NOT EXISTS bni_credit_certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bni_member_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    chapter TEXT NOT NULL,
    company TEXT,
    profession TEXT,
    scheduled_end_date TEXT,       -- 管理會員列表的「到期日」欄位(原定會期到期日,非實際離會日)
    actual_termination_date TEXT,  -- 會員資格歷史「終止會員資格」事件的實際日期
    cert_status TEXT NOT NULL,     -- issued / not_issued / ineligible(無剩餘會期)
    cert_id TEXT,
    issue_date TEXT,               -- 發行日期
    expiry_date TEXT,              -- 發行日期+2年
    usage_status TEXT,             -- active(尚可用) / transferred(已轉移) / redeemed(已贖回) / expired(已過期)
    transferred_to TEXT,
    transfer_date TEXT,
    credit_months INTEGER,         -- 證書面額(信用額度個月數)，只回填status='active'的記錄
    checked_at TEXT DEFAULT (datetime('now')),
    notes TEXT,
    sponsor_name TEXT              -- 推薦人(BNI Connect會員資格詳細資料tabs-6的「推薦人」欄位，2026-09-23新增)
);

CREATE INDEX IF NOT EXISTS idx_bcc_chapter ON bni_credit_certificates(chapter);

-- 通訊錄/會員名冊(2026-09-07教練交辦)：跟cards表(單張完整名片)分開存，
-- 因為一張照片對應多位聯絡人，不是「一張名片=一筆記錄」的結構。
-- 來源圖片在cards表仍留一筆status='roster'的標記列(company=org_name)，
-- 避免already_processed()重複觸發同一張圖，真正的逐人資料在這裡。
CREATE TABLE IF NOT EXISTS directory_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_filename TEXT NOT NULL,
    org_name TEXT,      -- 例如「嘉義嘉泰獅子會」
    org_type TEXT,      -- 獅子會/扶輪社/同濟會/校友會/公會/商會/協會/其他
    name TEXT NOT NULL,
    phone TEXT,
    profession TEXT,    -- 專業類別/職業別/擔任職務
    address TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_directory_org ON directory_contacts(org_name);
CREATE INDEX IF NOT EXISTS idx_directory_name ON directory_contacts(name);
CREATE INDEX IF NOT EXISTS idx_directory_image ON directory_contacts(image_filename);
CREATE INDEX IF NOT EXISTS idx_bcc_status ON bni_credit_certificates(cert_status);
