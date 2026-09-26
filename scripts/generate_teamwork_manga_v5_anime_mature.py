"""v5 模板 — 日本動漫成熟版（Mature Adult Anime）

教練 2026-09-26 12:28 選定風格 B（日本動漫成熟版）。

鎖定規格（教練親定，不准改）：
- 風格：Modern Japanese Anime Key-Visual — Mature Adult Anime
- 人物：40-50 歲東亞成熟專業人士（百工百業眾生圖）
- 構圖：1536×1024 / 3:2
- 教練本人：❌ 不出現（p28 除外）
- p28 例外：✅ 帶 coach_face_reference.jpg 鎖臉（邀請你加入團隊）
- 輸出：JPEG q=85，連號 pXX_narrative_v5.jpg
- prompt 模板：每張只換 [SCENE] 區塊，其他區塊一字不變

修改紀錄：
- 2026-09-26 12:38 v5 建立（教練 B 風格選定）
- 2026-09-26 13:02 v5 擴大為 100+ 種職業池
- 2026-09-26 14:36 v5 寫死最嚴格 5 條規則（教練 14:35 親定「當然要用最嚴格的 AI」）
   * Rule 1: 預設禁用 5 個濫用職業（廚師/工程帽工人/護理師/西裝上班族/醫師）
   * Rule 2: 過去 10 張已出現的職業禁止再用
   * Rule 3: 每張圖至少 5 個全新職業
   * Rule 4: 8 個人必須來自 8 個不同行業大類
   * Rule 5: 場景關鍵字強制對應（從 scene_desc 自動抓關鍵字）
- 2026-09-26 15:10 v5 加入防呆機制（教練 15:05 LK888 額度浪費事故後建立）
   * 🐛 Bug：教練 28 張需求，實際出圖 96 張，多跑了 68 張（p04 跑 17 次、p10 跑 13 次）
   * ✅ 防呆 1：run_panel 前檢查 mtime（< 60s 直接擋下、< 300s 警告放行）
   * ✅ 防呆 2：每次執行記錄到 state/lk888_run_history.json
   * ✅ 防呆 3：5 分鐘內同 panel 重複執行 → 自動擋下 + 立刻回報教練
   * 用法：教練訊息裡有「retry」關鍵字才允許 < 60s 重跑
"""

from pathlib import Path
import time
import sys
import json

# Import 工具函數
sys.path.insert(0, str(Path(__file__).parent))
from generate_teamwork_manga_narrative import call_lk88_generation, png_to_jpeg

DATA_DIR = Path('claude-brain/data/comic_source_20260926_teamwork_manga')
SEEN_JSON_PATH = DATA_DIR / '.occupations_seen.json'
RUN_HISTORY_PATH = Path('state/lk888_run_history.json')

# 🐛 防呆 1：mtime 檢查常數（教練 15:05 LK888 額度浪費事故後建立）
MTIME_HARD_LOCK_SECONDS = 60       # < 60s 絕對擋下（除非 --force-retry）
MTIME_WARN_PASS_SECONDS = 300      # < 300s 警告放行（5 分鐘內重複）


def _load_seen_occupations() -> dict:
    """讀取前 10 張已出現的職業歷史（自動讀取 .occupations_seen.json）"""
    if not SEEN_JSON_PATH.exists():
        return {}
    return json.loads(SEEN_JSON_PATH.read_text())


def _match_scene_keywords(scene_desc: str, keyword_map: dict) -> str:
    """從 scene_desc 自動抓取關鍵字 → 對應職業"""
    matched = []
    for keyword, occupations in keyword_map.items():
        for kw in keyword.split('/'):
            if kw and kw in scene_desc:
                matched.append(f'  - "{keyword}" → {", ".join(occupations)}')
                break
    return '\n'.join(matched) if matched else '  (scene_desc 沒有明確職業關鍵字)'


def _record_run(panel: str, size_bytes: int, mtime: float, exec_count: int, status: str) -> None:
    """防呆 2：每次執行記錄到 state/lk888_run_history.json"""
    RUN_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = []
    if RUN_HISTORY_PATH.exists():
        try:
            history = json.loads(RUN_HISTORY_PATH.read_text())
        except json.JSONDecodeError:
            history = []
    history.append({
        'panel': panel,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime(mtime)),
        'epoch': int(mtime),
        'size_bytes': size_bytes,
        'exec_count': exec_count,
        'status': status,  # 'success' / 'blocked' / 'forced-retry'
    })
    # 只保留最近 100 筆
    history = history[-100:]
    RUN_HISTORY_PATH.write_text(json.dumps(history, indent=2, ensure_ascii=False))


def _check_mtime_lock(idx: int, out_jpg: Path, force_retry: bool = False) -> dict:
    """🐛 防呆 3：檢查檔案 mtime，禁止短時間內重複執行同一個 panel

    Returns:
        dict: {
            'allow': bool,
            'reason': str,
            'age_seconds': float,
            'exec_count': int,
        }
    """
    if not out_jpg.exists():
        return {'allow': True, 'reason': 'file not exists (first run)', 'age_seconds': -1, 'exec_count': 0}

    mtime = out_jpg.stat().st_mtime
    size = out_jpg.stat().st_size
    age = time.time() - mtime

    # 讀歷史記錄，計算這個 panel 的 exec_count
    exec_count = 1  # 至少有現在這個
    if RUN_HISTORY_PATH.exists():
        try:
            history = json.loads(RUN_HISTORY_PATH.read_text())
            panel_str = f'p{idx:02d}'
            exec_count = sum(1 for r in history if r.get('panel') == panel_str) + 1
        except (json.JSONDecodeError, KeyError):
            pass

    if age < MTIME_HARD_LOCK_SECONDS and not force_retry:
        return {
            'allow': False,
            'reason': f'❌ {out_jpg.name} 才 {age:.0f} 秒前跑過（exec_count={exec_count}），禁止重跑。教練明確說 retry 才用 --force-retry',
            'age_seconds': age,
            'exec_count': exec_count,
        }
    elif age < MTIME_WARN_PASS_SECONDS:
        return {
            'allow': True,
            'reason': f'⚠️ {out_jpg.name} 才 {age:.0f} 秒前跑過（exec_count={exec_count}），繼續執行',
            'age_seconds': age,
            'exec_count': exec_count,
        }
    else:
        return {
            'allow': True,
            'reason': f'✅ {out_jpg.name} 已 {age:.0f} 秒前跑過，正常執行',
            'age_seconds': age,
            'exec_count': exec_count,
        }


def build_v5_prompt(scene_desc: str, idx: int = 0) -> str:
    """v5 模板 — 只換 [SCENE] 區塊，其他區塊一字不變

    Args:
        scene_desc: 場景描述（從 prompts.json 抓出來的 scene_desc 區塊）
        idx: panel 編號（p28 例外：保留 Coach 引用 + 帶 reference 圖鎖臉）

    Returns:
        完整 prompt 字串
    """
    # 讀取禁用清單 + 場景關鍵字對應表
    seen = _load_seen_occupations()
    rules = seen.get('next_panel_rules', {})
    hard_disallow = rules.get('hard_disallow', [])
    seen_occupations = seen.get('explicitly_seen_occupations', [])
    seen_industries = seen.get('industry_categories_seen', [])
    scene_keyword_map = rules.get('scene_keyword_map', {})

    # 場景關鍵字匹配
    scene_match_hint = _match_scene_keywords(scene_desc, scene_keyword_map)

    # p28 是邀請你加入團隊 — 保留 Coach 引用 + 鎖臉
    # 其他 27 張 — 自動清洗 Coach / 教練 引用，避免教練本人出現
    if idx != 28:
        scene_desc = scene_desc.replace("the Coach", "a mature Taiwanese professional")
        scene_desc = scene_desc.replace("Coach", "a mature Taiwanese professional")
        scene_desc = scene_desc.replace("教練", "一位成熟台灣專業人士")

    hard_disallow_str = '、'.join(hard_disallow) if hard_disallow else '（無）'
    seen_occupations_str = '、'.join(seen_occupations) if seen_occupations else '（無）'
    seen_industries_str = '、'.join(seen_industries) if seen_industries else '（無）'

    return f"""A wide cinematic composition, MODERN JAPANESE ANIME KEY-VISUAL STYLE — clean confident line art, saturated cinematic colors, dramatic lighting, anime aesthetics. MATURE ADULT ANIME (think Japanese business drama like 課長島耕作, NOT high school romance, NOT slice-of-life cute, NOT kawaii).

[CRITICAL: TEAM OF 8 TOTAL — DIVERSE MATURE TAIWANESE/CHINESE — NOT 20s, NOT KOREAN, NOT JAPANESE]
EXACTLY 8 characters TOTAL in the ENTIRE scene. ALL 40-50 years old mature TAIWANESE/CHINESE (台灣人/華人).

[TAIWANESE/CHINESE FACIAL FEATURES — 100% FORBIDDEN ELSE]
100% FORBIDDEN: Korean V-line face, Korean permed hair, Korean porcelain white skin, Korean large double eyelid, Korean idol-style features
100% FORBIDDEN: Japanese round face, Japanese pale skin, Japanese dyed hair, Japanese round anime eyes, Japanese kawaii features
MUST HAVE: oval-to-square face shape, almond-shaped eyes (single eyelid or inner double eyelid), warmer yellow skin tone, defined mature jawline

[MATURE CHARACTER DETAILS]
Visible thin smile lines at outer eye corners (1-2 subtle lines), mature solid face structure, short natural black hair (NOT spiky, NOT flowing, NOT permed, NOT dyed), calm composed steady gaze, solid mature body build

[🚨 ULTRA-STRICT 5 RULES — HIGHEST PRIORITY 🚨]

RULE 1 — HARD DISALLOW (預設禁用 — 必須 scene 明確要求才用):
{hard_disallow_str}
Use ONLY if [SCENE] EXPLICITLY mentions them (e.g., scene has a kitchen/restaurant → chef is OK).

RULE 2 — NEVER REPEAT PREVIOUSLY-SEEN OCCUPATIONS:
{seen_occupations_str}

RULE 3 — REQUIRE MIN 5 NEW OCCUPATIONS:
8 characters 中至少 5 個必須是「之前完全沒出現過」的全新職業。

RULE 4 — 8 DISTINCT INDUSTRY CATEGORIES (8 個不同行業大類):
已出現過的大類（禁止再用）: {seen_industries_str}
必須從以下 23 個大類中選 8 個「未出現過的」大類:
餐飲/烘焙、醫療、工程/營造、設計/藝術、銷售/商業、法律/金融、教育、農業/漁業、科技、藝術/媒體、公共服務、服務業、物流/交通、音樂/表演、警政、清潔/維護、殯葬、宗教、出版/文字、心理諮商、美容/美甲、寵物、體育、製造/工廠

RULE 5 — SCENE KEYWORD MATCHING (場景關鍵字強制對應):
{scene_match_hint}

[OCCUPATION POOL — 100+ UNSEEN, PREFER THESE]

從以下 100+ 種職業池中選 8 個「未出現過的、來自不同行業大類的」職業：

餐飲/烘焙: baker 烘焙師 (apron + bread), bartender 調酒師 (cocktail shaker), barista 咖啡師 (espresso machine), waiter 服務生, sommelier 侍酒師, food critic 美食評論家
醫療: pharmacist 藥師, dentist 牙醫, veterinarian 獸醫, optometrist 驗光師, psychologist 心理師, midwife 助產師, paramedic 救護員
工程/營造: HVAC technician 冷氣師傅, welder 焊接師傅, painter 油漆師傅, carpenter 木工師傅, crane operator 吊車操作員, plumber 水電工 (tool belt + wrench)
設計: interior designer 室內設計師 (fabric swatches), graphic designer 平面設計師, industrial designer 工業設計師, makeup artist 彩妝師, tattoo artist 刺青師, UI/UX designer
銷售/商業: insurance agent 保險業務, real estate agent 房地產銷售 (property photos), car salesperson 汽車銷售 (showroom), import/export specialist, retail salesperson 門市銷售
法律/金融: judge 法官 (robe), prosecutor 檢察官, accountant 會計師 (calculator), financial advisor 理財專員, tax consultant 記帳士, banker 銀行員
教育: university professor 教授, music teacher 音樂老師, driving instructor 駕訓教練, language teacher 語言老師, special education teacher 特教老師
農業/漁業: beekeeper 養蜂人 (bee suit), gardener 園丁, florist 花藝師 (flowers), rancher 牧場主人, ship captain 船長, fisherman 漁夫
科技: software engineer 軟體工程師 (laptop), data scientist 資料科學家, AI researcher AI研究員, cybersecurity specialist 資安專家, drone operator 無人機操作員, hardware engineer 硬體工程師
藝術/媒體: filmmaker 導演 (clapperboard), video editor 剪輯師, journalist 記者 (notepad), DJ 唱片DJ (headphones), dancer 舞者, sculptor 雕塑家, painter 畫家 (palette)
公共服務: military officer 軍官 (uniform), postal worker 郵差, customs officer 海關人員, firefighter 消防員 (red helmet) — only if scene requires
服務業: hotel concierge 飯店禮賓, fitness trainer 健身教練, yoga instructor 瑜伽老師, beautician 美容師, tour guide 導遊, babysitter 保母
物流/交通: delivery driver 快遞員 (uniform + package), taxi driver 計程車司機 (yellow sign), truck driver 卡車司機, airline pilot 機師, air traffic controller 塔台管制員
音樂/表演: musician 音樂家 (instrument), singer 歌手 (microphone), actor 演員, circus performer 馬戲團表演者
警政: police officer 警察 (uniform + cap) — only if scene requires
清潔/維護: window cleaner 蜘蛛人 (harness), pool cleaner 泳池清潔, pest control 除蟲師傅, locksmith 鎖匠, housekeeper 居家管家
殯葬: funeral director 禮儀師 (suit)
宗教: monk 僧侶 (kasaya robe), priest 神父 (collar), fortune teller 命理師
出版/文字: writer 作家 (typewriter), editor 編輯, translator 翻譯, librarian 圖書館員, journalist 記者
心理諮商: counselor 諮商師 (couch + notebook), life coach 人生教練
美容/美甲: manicurist 美甲師 (nail polish), hairstylist 髮型設計師 (scissors + cape) — only if scene requires, makeup artist 彩妝師
寵物: pet groomer 寵物美容師, pet trainer 寵物訓練師, veterinarian 獸醫 (stethoscope + animal)
體育: athlete 運動員 (sportswear), sports coach 運動教練, swimming instructor 游泳教練, yoga instructor 瑜伽老師
製造/工廠: factory worker 工廠作業員 (helmet + uniform), quality inspector 品管員 (clipboard), machine operator 機台操作員, welder 焊接師傅 (mask)

CRITICAL RULES (再次強調):
1. HARD DISALLOW (Rule 1): Avoid 廚師/工程帽工人/護理師/西裝上班族/醫師 unless scene EXPLICITLY requires
2. NEVER REPEAT (Rule 2): All 8 occupations MUST NOT be in the seen list
3. NEW 5+ (Rule 3): At least 5 of 8 must be BRAND-NEW occupations
4. 8 DISTINCT CATEGORIES (Rule 4): Each character from a DIFFERENT industry category (no two from same category)
5. SCENE MATCH (Rule 5): Keywords in scene MUST trigger matching occupations

[SCENE]
{scene_desc}

[STYLE]
Modern Japanese anime key-visual — clean line art, saturated cinematic colors, dramatic composition, cinematic lighting. Mature anime adults. 3:2 landscape aspect ratio (1536x1024).

[SAFETY]
NO text, letters, numbers, logos, watermarks, chibi style, baby-face anime youth, schoolboy features, Caucasian/Western faces, Korean faces (NOT Korean V-line, NOT Korean permed hair, NOT Korean porcelain skin, NOT Korean large double eyelid), Japanese faces (NOT Japanese round face, NOT Japanese pale skin, NOT Japanese dyed hair, NOT Japanese round anime eyes). ONLY Taiwanese/Chinese adults.
"""


def generate_panel(idx: int, scene_desc: str, output_filename: str = None, force_retry: bool = False) -> dict:
    """跑一張 v5 風格的 panel

    Args:
        idx: panel 編號 (1-28)
        scene_desc: 場景描述（從 prompts.json 抓出來的 scene_desc 區塊）
        output_filename: 輸出檔名（預設 pXX_narrative_v5.jpg）
        force_retry: 強制重跑（必須有教練明確「retry」指令才能設為 True）

    Returns:
        dict: {'success': bool, 'jpg_path': Path, 'size_bytes': int, 'elapsed_seconds': float}
    """
    if output_filename is None:
        output_filename = f'p{idx:02d}_narrative_v5.jpg'

    out_jpg = DATA_DIR / output_filename

    # 🐛 防呆 3：mtime 檢查（教練 15:05 LK888 額度浪費事故後建立）
    lock_check = _check_mtime_lock(idx, out_jpg, force_retry=force_retry)
    print(f'[p{idx:02d}] 🐛 mtime 防呆檢查: {lock_check["reason"]}', flush=True)

    if not lock_check['allow']:
        # 記錄被擋下的執行（給未來 debug 用）
        _record_run(f'p{idx:02d}', 0, time.time(), lock_check['exec_count'], 'blocked')
        raise SystemExit(lock_check['reason'])

    prompt = build_v5_prompt(scene_desc, idx)

    print(f'[p{idx:02d}] prompt len: {len(prompt)} chars', flush=True)
    t0 = time.time()
    png_bytes = call_lk88_generation(prompt, '1536x1024')
    elapsed = time.time() - t0
    print(f'[p{idx:02d}] 生成: {elapsed:.1f}s, {len(png_bytes)} bytes PNG', flush=True)
    size = png_to_jpeg(png_bytes, out_jpg, 85)
    print(f'[p{idx:02d}] JPEG: {size} bytes', flush=True)

    # 🐛 防呆 2：記錄這次成功執行
    final_mtime = out_jpg.stat().st_mtime
    status = 'forced-retry' if force_retry else 'success'
    _record_run(f'p{idx:02d}', size, final_mtime, lock_check['exec_count'], status)

    return {
        'success': True,
        'jpg_path': out_jpg,
        'size_bytes': size,
        'elapsed_seconds': elapsed,
        'exec_count': lock_check['exec_count'],
        'mtime_check': lock_check['reason'],
    }


# CLI 模式：python3 generate_teamwork_manga_v5_anime_mature.py <idx> [--force-retry]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 generate_teamwork_manga_v5_anime_mature.py <idx 1-28> [--force-retry]')
        sys.exit(1)
    idx = int(sys.argv[1])
    force_retry = '--force-retry' in sys.argv

    if force_retry:
        print('⚠️ --force-retry 模式：允許 60 秒內重跑（教練明確 retry 才用）', flush=True)

    data = json.load(open(DATA_DIR / 'prompts.json'))
    p = next(p for p in data if p['idx'] == idx)
    result = generate_panel(idx, p['scene_desc'], force_retry=force_retry)
    print(f'p{idx:02d} done: {result}')
