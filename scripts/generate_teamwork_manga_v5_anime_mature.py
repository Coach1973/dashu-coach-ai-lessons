"""v5 模板 - 日本動漫成熟版（Mature Adult Anime）

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
"""

from pathlib import Path
import time
import sys

# Import 工具函數
sys.path.insert(0, str(Path(__file__).parent))
from generate_teamwork_manga_narrative import call_lk88_generation, png_to_jpeg

DATA_DIR = Path('claude-brain/data/comic_source_20260926_teamwork_manga')


def build_v5_prompt(scene_desc: str, idx: int = 0) -> str:
    """v5 模板 — 只換 [SCENE] 區塊，其他區塊一字不變

    Args:
        scene_desc: 場景描述（從 prompts.json 抓出來的 scene_desc 區塊）
        idx: panel 編號（p28 例外：保留 Coach 引用 + 帶 reference 圖鎖臉）

    Returns:
        完整 prompt 字串
    """
    # p28 是邀請你加入團隊 — 保留 Coach 引用 + 鎖臉
    # 其他 27 張 — 自動清洗 Coach / 教練 引用，避免教練本人出現
    if idx != 28:
        scene_desc_clean = scene_desc
        scene_desc_clean = scene_desc_clean.replace("the Coach", "a mature Taiwanese professional")
        scene_desc_clean = scene_desc_clean.replace("Coach", "a mature Taiwanese professional")
        scene_desc_clean = scene_desc_clean.replace("教練", "一位成熟台灣專業人士")
        scene_desc = scene_desc_clean

    return f"""A wide cinematic composition, MODERN JAPANESE ANIME KEY-VISUAL STYLE — clean confident line art, saturated cinematic colors, dramatic lighting, anime aesthetics. MATURE ADULT ANIME (think Japanese business drama like 課長島耕作, NOT high school romance, NOT slice-of-life cute, NOT kawaii).

[CRITICAL: TEAM OF 8 TOTAL — DIVERSE MATURE TAIWANESE/CHINESE — NOT 20s, NOT KOREAN, NOT JAPANESE]
EXACTLY 8 characters TOTAL in the ENTIRE scene. If 1 man alone appears, the team has 7 (1+7=8). If just a team, team has 8. ALL 40-50 years old mature TAIWANESE/CHINESE (台灣人/華人).

[TAIWANESE/CHINESE FACIAL FEATURES — 100% FORBIDDEN ELSE]
100% FORBIDDEN: Korean V-line face, Korean permed hair, Korean porcelain white skin, Korean large double eyelid, Korean idol-style features
100% FORBIDDEN: Japanese round face, Japanese pale white skin, Japanese dyed hair, Japanese round anime eyes, Japanese kawaii features
MUST HAVE: oval-to-square face shape, almond-shaped eyes (single eyelid or inner double eyelid), warmer yellow skin tone, defined mature jawline

[MATURE CHARACTER DETAILS]
Visible thin smile lines at outer eye corners (1-2 subtle lines)
Mature solid face structure (NOT pointy childish chin)
Short natural black hair, simple adult hairstyle (NOT spiky, NOT flowing, NOT permed, NOT dyed)
Calm composed steady gaze (NOT sparkling cute anime eyes)
Solid mature body build, broader shoulders

[8 OCCUPATIONS — 百工百業 100+ DYNAMIC, MUST MATCH SCENE, NEVER REPEAT]
Pick 8 occupations from this 100+ pool. The occupations MUST match [SCENE] content. NEVER use the same 8-occupation combination across panels.

SCENE-MATCH RULES (HIGHEST PRIORITY):
- If [SCENE] mentions water/electricity/plumbing → MUST include 水電工 (plumber/electrician with tool belt + wrench)
- If [SCENE] mentions music/instruments/sound → MUST include 音樂家 (musician with violin/piano/guitar)
- If [SCENE] mentions cars/auto/vehicle → MUST include 汽車銷售 (car salesperson with showroom/car)
- If [SCENE] mentions houses/property/real estate → MUST include 房地產銷售 (real estate agent with property photos)
- If [SCENE] mentions food/cooking/restaurant → MUST include chef
- If [SCENE] mentions hair/salon/barber → MUST include 髮型設計師 (hair designer with scissors + cape)
- If [SCENE] mentions clothing/fashion/apparel → MUST include 服裝設計師 (fashion designer)
- If [SCENE] mentions interior/home decoration → MUST include 室內設計師 (interior designer)
- At least 3-5 of the 8 occupations MUST match the [SCENE] content.

OCCUPATION POOL (100+, pick 8 that match [SCENE]):
餐飲: chef (whites + tall chef hat), sous chef, baker, bartender, barista, waiter, sommelier
醫療: doctor (white coat + stethoscope), nurse (scrubs + cap), pharmacist, dentist, veterinarian, paramedic, midwife
工程/營造: civil engineer (hard hat + blueprints), mechanical engineer, electrical engineer, architect (rolled blueprints + glasses), construction worker, plumber/electrician 水電工 (tool belt + wrench), carpenter, painter, welder, HVAC technician, crane operator
設計: interior designer 室內設計師 (fabric swatches + mood board), graphic designer, fashion designer 服裝設計師 (sketch + fabric), industrial designer, UI/UX designer, hair designer 髮型設計師 (scissors + cape), makeup artist
銷售/商業: businessman (navy suit + tie), businesswoman (blazer), real estate agent 房地產銷售 (property photos), car salesperson 汽車銷售 (showroom), insurance agent, retail salesperson, marketing manager
法律/金融: lawyer (briefcase + law book), accountant (ledger), financial advisor, banker, tax consultant
教育: university professor, high school teacher, elementary teacher, music teacher
農業: farmer (straw hat + rolled sleeves), fisherman (net), rancher, gardener, beekeeper, florist
科技: software engineer (laptop), data scientist, AI researcher, cybersecurity specialist
藝術/媒體: photographer (camera), video editor, journalist (notepad), filmmaker (clapperboard), musician 音樂家 (violin/piano/guitar), DJ (headphones), dancer, painter (palette)
公共服務: police officer (uniform + cap), firefighter (red helmet), military officer, postal worker, customs officer
服務業: hairdresser (scissors + cape), beautician, manicurist, tour guide, hotel concierge, fitness trainer, yoga instructor, driving instructor
物流/交通: delivery driver, warehouse worker, taxi driver (yellow sign), truck driver, ship captain, airline pilot, air traffic controller
水電木工 (trades — MUST show tools): 水電工 plumber/electrician (tool belt + wrench), 木工 carpenter (hammer + wood), 油漆工 painter (paint roller), 防水師傅 (sealant gun), 抓漏師傅 (detection equipment)

CRITICAL RULES:
1. SCENE MATCH (HIGHEST PRIORITY): At least 3-5 of 8 occupations MUST match [SCENE] content.
2. MIX: At least 2 white-collar + 2 blue-collar/trades + 1 creative + 1 service. NO all-suits panel.
3. VARIED: NEVER use the same 8-occupation combination as previous panels.
4. VISUAL CLARITY: Each occupation has CLEAR VISUAL ATTIRE (chef hat, hard hat, scissors, tool belt, camera, instrument, stethoscope). NO two characters wear the same uniform.
5. COMPOSITION: All 8 distinct professionals visible with tools/attire.

[SCENE]
{scene_desc}

[STYLE]
Modern Japanese anime key-visual — clean line art, saturated cinematic colors, dramatic composition, cinematic lighting. Mature anime adults. 3:2 landscape aspect ratio (1536x1024).

[SAFETY]
NO text, letters, numbers, logos, watermarks, chibi style, baby-face anime youth, schoolboy features, Caucasian/Western faces, Korean faces (NOT Korean V-line, NOT Korean permed hair, NOT Korean porcelain skin, NOT Korean large double eyelid), Japanese faces (NOT Japanese round face, NOT Japanese pale skin, NOT Japanese dyed hair, NOT Japanese round anime eyes). ONLY Taiwanese/Chinese adults.
"""


def generate_panel(idx: int, scene_desc: str, output_filename: str = None) -> dict:
    """跑一張 v5 風格的 panel

    Args:
        idx: panel 編號 (1-28)
        scene_desc: 場景描述（從 prompts.json 抓出來的 scene_desc 區塊）
        output_filename: 輸出檔名（預設 pXX_narrative_v5.jpg）

    Returns:
        dict: {'success': bool, 'jpg_path': Path, 'size_bytes': int, 'elapsed_seconds': float}
    """
    if output_filename is None:
        output_filename = f'p{idx:02d}_narrative_v5.jpg'

    out_jpg = DATA_DIR / output_filename
    prompt = build_v5_prompt(scene_desc, idx)

    print(f'[p{idx:02d}] prompt len: {len(prompt)} chars', flush=True)
    t0 = time.time()
    png_bytes = call_lk88_generation(prompt, '1536x1024')
    elapsed = time.time() - t0
    print(f'[p{idx:02d}] 生成: {elapsed:.1f}s, {len(png_bytes)} bytes PNG', flush=True)
    size = png_to_jpeg(png_bytes, out_jpg, 85)
    print(f'[p{idx:02d}] JPEG: {size} bytes', flush=True)
    return {
        'success': True,
        'jpg_path': out_jpg,
        'size_bytes': size,
        'elapsed_seconds': elapsed,
    }


# CLI 模式：python3 generate_teamwork_manga_v5_anime_mature.py <idx>
if __name__ == '__main__':
    import json
    if len(sys.argv) < 2:
        print('Usage: python3 generate_teamwork_manga_v5_anime_mature.py <idx 1-28>')
        sys.exit(1)
    idx = int(sys.argv[1])
    data = json.load(open(DATA_DIR / 'prompts.json'))
    p = next(p for p in data if p['idx'] == idx)
    result = generate_panel(idx, p['scene_desc'])
    print(f'p{idx:02d} done: {result}')
