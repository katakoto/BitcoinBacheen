#!/usr/bin/env python3
"""
Regenerate OGP composite images:
- Canvas: 1200x628
- Full canvas: quiz image scaled to fill, center-cropped vertically
"""

import os
from PIL import Image

# Paths
QUIZ_IMG_BASE = r'C:\Users\hiro\claude_work\BitcoinWebsite\Quiz\images'
OUTPUT_DIR    = r'C:\Users\hiro\claude_work\BitcoinWebsite\meme\ogp'

CANVAS_W = 1200
CANVAS_H = 628
IMG_PANEL_W = 1200  # full canvas width (100%)

BG_COLOR     = (10, 10, 10)
ORANGE_COLOR = (245, 166, 35)
WHITE_COLOR  = (255, 255, 255)
GRAY_COLOR   = (120, 120, 120)

STAGES = [
    ('00', 'このクイズとは？'),
    ('01', 'インフレ①'),
    ('02', 'インフレ②'),
    ('03', '通貨膨張'),
    ('04', '通貨発行の仕組み'),
    ('05', '歴史は繰り返す'),
    ('06', '自由市場①'),
    ('07', '自由市場②'),
    ('08', '貨幣と自由市場'),
    ('09', 'サウンドマネー①'),
    ('10', 'サウンドマネー②'),
    ('11', 'ビットコインの現在地'),
    ('12', '自由のテクノロジー①'),
    ('13', '自己主権のテクノロジー'),
    ('14', '自由と国家'),
]

def last_slides(stage_int):
    if stage_int == 0:
        return [4]
    slides = list(range(4, 81, 4))
    slides.append(83)
    return slides

os.makedirs(OUTPUT_DIR, exist_ok=True)

count = 0
for stage_num, stage_title in STAGES:
    stage_int = int(stage_num)
    stage_pad = stage_num.zfill(4)

    for slide in last_slides(stage_int):
        slide_pad = str(slide).zfill(2)
        card_id   = f'{stage_pad}-{slide_pad}'
        out_path  = os.path.join(OUTPUT_DIR, f'{card_id}.png')

        img_path = os.path.join(QUIZ_IMG_BASE, stage_pad, f'{slide}.png')
        if not os.path.exists(img_path):
            print(f'  [SKIP] {img_path} not found')
            continue

        # ── Canvas ──────────────────────────────────────────────
        canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), BG_COLOR)

        # ── Quiz image: fill full canvas ─────────────────────────
        quiz_img = Image.open(img_path).convert('RGB')
        q_w, q_h = quiz_img.size

        scale  = IMG_PANEL_W / q_w
        new_w  = IMG_PANEL_W
        new_h  = int(q_h * scale)

        quiz_scaled = quiz_img.resize((new_w, new_h), Image.LANCZOS)

        # Bottom-biased crop: characters are in the lower portion of quiz images
        if new_h > CANVAS_H:
            crop_y = int((new_h - CANVAS_H) * 0.65)
            quiz_cropped = quiz_scaled.crop((0, crop_y, new_w, crop_y + CANVAS_H))
        else:
            quiz_cropped = Image.new('RGB', (new_w, CANVAS_H), BG_COLOR)
            paste_y = (CANVAS_H - new_h) // 2
            quiz_cropped.paste(quiz_scaled, (0, paste_y))

        canvas.paste(quiz_cropped, (0, 0))

        canvas.save(out_path)
        count += 1

print(f'Generated {count} OGP images')
