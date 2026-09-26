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


def build_v5_prompt(scene_desc: str) -> str:
    """v5 模板 — 只換 [SCENE] 區塊，其他區塊一字不變

    Args:
        scene_desc: 場景描述（從 prompts.json 抓出來的 scene_desc 區塊）

    Returns:
        完整 prompt 字串
    """
    return f"""A wide cinematic composition, MODERN JAPANESE ANIME KEY-VISUAL STYLE — clean confident line art, saturated cinematic colors, dramatic lighting, anime aesthetics. MATURE ADULT ANIME (think Japanese business drama like 課長島耕作, NOT high school romance, NOT slice-of-life cute, NOT kawaii).

[CRITICAL: TEAM OF 8 DIVERSE MATURE EAST ASIAN ADULTS — NOT 20-SOMETHINGS]
EXACTLY 8 characters, no more no less, arranged as a cohesive team in the scene. ALL 8 characters are 40 to 50 years old East Asian (Chinese/Taiwanese/Japanese/Korean) mature adults in anime style. To force mature anime characters:
- Longer angular face structure (NOT round kawaii face, NOT pointy childish chin)
- Visible thin mature smile lines at outer eye corners (1-2 subtle lines, NOT smooth porcelain)
- Visible mature jawline, broader facial structure
- Short natural black hair, simple adult hairstyle (NOT spiky anime protagonist hair, NOT flowing hair, NOT bangs)
- Calm composed steady gaze (NOT sparkling cute anime eyes)
- Solid mature body build, broader shoulders (NOT slender youth body)

[8 DIVERSE OCCUPATIONS — 百工百業 TEAM OF 8]
The 8 characters represent diverse occupations from the Hundred Trades (百工百業). Pick 8 from this list, each one visually distinct and clearly identifiable by their work attire:
1. 廚師 — chef in whites with tall white chef hat
2. 醫師 — doctor in white coat with stethoscope around neck
3. 工程師 — engineer with yellow hard hat and blueprints
4. 律師/商人 — businessman in tailored navy suit with blue tie
5. 農夫 — farmer with straw hat and rolled sleeves
6. 建築師 — architect with rolled blueprints and glasses
7. 護理師 — nurse in scrubs with cap
8. 消防員 — firefighter with red helmet
9. 廚師助手 — sous-chef in whites
10. 音樂家 — musician with instrument (violin/piano)
11. 教師 — teacher/educator with glasses and formal attire
12. 技工 — mechanic in overalls with wrench
13. 警察 — police officer in uniform with cap
14. 設計師 — designer with stylish creative attire
15. 會計師 — accountant in formal suit with ledger
16. 攝影師 — photographer with camera

Each of the 8 characters must have visibly different profession attire — NO two characters wear the same uniform. The composition must clearly show all 8 distinct professionals.

[SCENE]
{scene_desc}

[STYLE]
Modern Japanese anime key-visual — clean line art, saturated cinematic colors, dramatic composition, cinematic lighting. Mature anime adults. 3:2 landscape aspect ratio (1536x1024).

[SAFETY]
NO text, letters, numbers, logos, watermarks, chibi style, baby-face anime youth, schoolboy features, Caucasian/Western faces.
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
    prompt = build_v5_prompt(scene_desc)

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
