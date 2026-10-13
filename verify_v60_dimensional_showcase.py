#!/usr/bin/env python3
"""
Verification & Showcase Suite for PPT_Saz v6.0 — Multi-Dimensional Visual Engine
(2.5D Isometric, 3D Volumetric Claymorphism, Photorealistic Textured Art, and 2D Technical)

Generates:
  1. `output/PPT_Saz_v60_Dimensional_Master_Showcase.pptx` (A master 6-slide deck showing all 4 paradigms)
  2. `output/Paradigm_1_Isometric_25D_World.pptx`
  3. `output/Paradigm_2_Volumetric_3D_Claymorphism.pptx`
  4. `output/Paradigm_3_Photorealistic_Textured_Art.pptx`
  5. `output/Paradigm_4_Technical_2D_Blueprint.pptx`
"""

from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from presentation_generator import SlideRenderer, load_themes, generate_presentation_project, generate_deck_animations_config
from infographic_layouts import InfographicLayoutRenderer
from svg_to_pptx import main as svg_main


MASTER_PARADIGM_SLIDES = [
    {
        "layout": "title_hero",
        "theme_key": "cyber_aurora",
        "kicker": "انقلاب بعد و رندرینگ در PPT_Saz v6.0",
        "title": "فراتر از تغییر رنگ: معماری ۴ پارادایم چندبُعدی",
        "subtitle": "خروج کامل از اشکال فلت دو بعدی با معرفی: ۲.۵ بعدی ایزومتریک، ۳ بعدی حجمی کلی‌مورفیسم، متریال فوتورئالیستیک و ۲ بعدی مهندسی\nحفظ ۱۰۰٪ متون و نمودارها با انیمیشن ممتد و ترنزیشن Morph",
        "author": "طراحی و توسعه: اسکیل PPT_Saz v6.0",
    },
    {
        "layout": "pyramid_hierarchy",
        "theme_key": "cyber_aurora",
        "kicker": "پارادایم ۱: ۲.۵ بعدی ایزومتریک",
        "title": "هرم ایزومتریک چندسطحی با دیواره‌های ضخامت و سایه کف",
        "cards": [
            {"title": "وجه بالایی روشن (+۲۲٪ Luminance)", "desc": "سطح افقی بستر قرارگیری متون و آیکون‌ها با نور مستقیم\nمحاسبه دقیق زوایای ۳۰ درجه آگزونومتریک", "icon": "layers"},
            {"title": "دیواره ضخامت راست (-۳۸٪ سایه)", "desc": "نمایش عمق واقعی بلوک در فضا با تیرگی مهندسی\nایجاد بعد واقعی بدون استفاده از عکس", "icon": "box"},
            {"title": "سایه‌افکنی مورب بر بستر زمین", "desc": "چندضلعی سایه نیمه‌شفاف در زیر هر بلوک و سکو\nحس شناوری و وزن فیزیکی المان‌ها در فضا", "icon": "compass"},
            {"title": "شبکه کف ۳۰ درجه و مکعب‌های شناور", "desc": "خطوط شبکه آگزونومتریک محیطی در ترکیب با آیکون‌های مکعبی\nتمایز آنی نسبت به اسلایدهای سنتی", "icon": "cpu"},
        ],
    },
    {
        "layout": "funnel_pipeline",
        "theme_key": "bento_glass_dark",
        "kicker": "پارادایم ۲: ۳ بعدی حجمی و کلی‌مورفیسم",
        "title": "قیف استوانه‌ای حجم‌دار با دهانه‌های بیضوی و نور استودیویی",
        "cards": [
            {"title": "بدنه نرم با گرادینت چندمرحله‌ای فنگ", "desc": "شبیه‌سازی انحنای واقعی استوانه با طیف نوری ملایم\nحذف کامل رنگ‌های یکنواخت و تخت", "icon": "sparkles"},
            {"title": "دهانه منحنی بیضوی (Mouth Depth)", "desc": "ترکیب دو بیضی تودرتو برای نمایش لب‌های استوانه و عمق ورودی\nایجاد حس سه‌بعدی پلاستیک و خاک‌رس مات", "icon": "layers"},
            {"title": "خط بازتاب نور مستقیم (Specular Rim)", "desc": "نوار بازتاب نور سافت‌باکس استودیو در راستای طولی قیف\nحس متریال صیقلی مدرن اپل", "icon": "eye"},
            {"title": "کره‌های ۳ بعدی شناور با هایلایت خارج از مرکز", "desc": "قاب آیکون‌ها و المان‌های پس‌زمینه به شکل کره‌های سه‌بعدی حقیقی\nنقطه کانونی نور در مختصات (0.35, 0.35)", "icon": "award"},
        ],
    },
    {
        "layout": "venn_synergy",
        "theme_key": "bento_glass_dark",
        "kicker": "پارادایم ۲: هم‌افزایی ۳ بعدی",
        "title": "حلقه‌های متقاطع شیشه‌ای حجم‌دار با سایه‌های نرم عمیق",
        "cards": [
            {"title": "حلقه اول: طراحی چندبُعدی", "desc": "استفاده از گرادینت‌های سه‌بعدی و سایه‌های ملایم ۲۴ پیکسلی برای عمق بصری", "icon": "box"},
            {"title": "حلقه دوم: حفظ ۱۰۰٪ محتوا", "desc": "عدم تغییر یک کلمه از متون کاربر و نمایش دقیق ساختار در دیاگرام‌ها", "icon": "check"},
            {"title": "حلقه سوم: پویایی ممتد", "desc": "حرکت پیوسته حلقه‌ها و ترنزیشن Morph بدون وقفه بین اسلایدها", "icon": "compass"},
        ],
    },
    {
        "layout": "quadrant_matrix_2x2",
        "theme_key": "royal_gold_dark",
        "kicker": "پارادایم ۳: فوتورئالیستیک و متریال واقعی",
        "title": "ماتریس استراتژیک روی سنگ مرمر نرو مارکینا با رگه‌های طلا",
        "cards": [
            {"title": "متریال بافت واقعی (Procedural Texture)", "desc": "تزریق بافت مرمر طبیعی و رگه‌های طلایی ارگانیک در پس‌زمینه\nخروج از پس‌زمینه‌های مصنوعی و رنگ‌های تک‌پیکسل", "icon": "award"},
            {"title": "کادرهای شمش طلای لبه‌دار (Beveled Gold)", "desc": "کادرهای هشت‌ضلعی چندلایه با حاشیه متالیک براق و سایه سنگین\nحس لوکس، رسمی و مدیریتی سطح یک", "icon": "shield"},
            {"title": "شیشه‌مورفیسم دودی مات (Frosted Glass)", "desc": "کارت‌های نیمه‌شفاف با اوپاسیتی ۸۵٪ روی بافت سنگین مرمر\nعمق فوکوس سینمایی و نورپردازی کیاروسکورو", "icon": "eye"},
            {"title": "مدال‌های مرواریدی و جواهرات سه‌بعدی", "desc": "قاب آیکون‌ها به شکل سکه‌های برجسته و گل‌میخ‌های نگین‌دار طلا\nهمنشینی با تایپوگرافی رسمی یکان باخ", "icon": "star"},
        ],
    },
    {
        "layout": "closing_thankyou",
        "theme_key": "blueprint_cad_dark",
        "kicker": "پارادایم ۴: خطوط مهندسی و بلوپرینت ۲ بعدی",
        "title": "کنتراست آگاهانه: دقت میکرومتری نقشه معماری و CAD",
        "subtitle": "برای اینکه بُعدهای ۲.۵ بعدی و ۳ بعدی جلوه کنند، سبک بلوپرینت با خطوط برداری تیز، کولیس اندازه‌گیری و بدون faux-3D طراحی شده است.\nپایان ارائه و آغاز نشست پرسش و پاسخ تخصصی",
    },
]


def build_deck(deck_name: str, slides_data: list, single_theme_key: str | None = None) -> Path:
    out_dir = ROOT / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = ROOT / "temp_build" / deck_name
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    svgs_dir = temp_dir / "svg_output"
    svgs_dir.mkdir(parents=True, exist_ok=True)

    themes = load_themes()

    print(f"\n========================================================")
    print(f"Building Deck: {deck_name} ({len(slides_data)} slides)")
    print(f"========================================================")

    for idx, slide in enumerate(slides_data, start=1):
        th_key = single_theme_key or slide.get("theme_key", "cyber_aurora")
        theme = themes[th_key]
        renderer = SlideRenderer(theme)
        layout = slide.get("layout", "content_cards")

        if layout == "title_hero":
            svg_content = renderer.render_title_slide(slide)
        elif layout == "pyramid_hierarchy":
            svg_content = InfographicLayoutRenderer.render_pyramid_hierarchy(renderer, slide, slide_idx=idx)
        elif layout == "funnel_pipeline":
            svg_content = InfographicLayoutRenderer.render_funnel_pipeline(renderer, slide, slide_idx=idx)
        elif layout == "venn_synergy":
            svg_content = InfographicLayoutRenderer.render_venn_synergy(renderer, slide, slide_idx=idx)
        elif layout == "quadrant_matrix_2x2":
            svg_content = InfographicLayoutRenderer.render_quadrant_matrix_2x2(renderer, slide, slide_idx=idx)
        elif layout == "closing_thankyou":
            svg_content = InfographicLayoutRenderer.render_closing_thankyou(renderer, slide, slide_idx=idx)
        else:
            svg_content = renderer.render_content_cards_slide(slide, slide_idx=idx)

        svg_path = svgs_dir / f"slide_{idx:02d}.svg"
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"  -> Generated Slide {idx:02d} [{layout}] in theme [{th_key}] (SVG: {len(svg_content)} chars)")

    # Build animations config
    anim_config = generate_deck_animations_config(temp_dir, transition="morph", animation_mode="auto")
    anim_path = temp_dir / "animations.json"
    with open(anim_path, "w", encoding="utf-8") as f:
        import json
        json.dump(anim_config, f, indent=2, ensure_ascii=False)

    out_pptx = out_dir / f"{deck_name}.pptx"
    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "svg_to_pptx",
            str(temp_dir),
            "-o", str(out_pptx),
            "-t", "morph",
            "-a", "auto",
            "--animation-trigger", "after-previous",
            "--animation-stagger", "0.35",
        ]
        svg_main()
    finally:
        sys.argv = old_argv

    print(f"  [SUCCESS] Created Native PPTX: {out_pptx} ({out_pptx.stat().st_size:,} bytes)")
    return out_pptx


def main():
    print("=== PPT_Saz v6.0: Multi-Dimensional Rendering Engine Verification ===")
    
    # 1. Master Showcase (All 4 Paradigms Side-by-Side)
    build_deck("PPT_Saz_v60_Dimensional_Master_Showcase", MASTER_PARADIGM_SLIDES)

    # 2. Individual Paradigm Demos
    # Paradigm 1: 2.5D Isometric World
    iso_slides = [s for s in MASTER_PARADIGM_SLIDES if s["layout"] in ("title_hero", "pyramid_hierarchy")]
    build_deck("Paradigm_1_Isometric_25D_World", iso_slides, single_theme_key="cyber_aurora")

    # Paradigm 2: 3D Volumetric Claymorphism Studio
    clay_slides = [s for s in MASTER_PARADIGM_SLIDES if s["layout"] in ("title_hero", "funnel_pipeline", "venn_synergy")]
    build_deck("Paradigm_2_Volumetric_3D_Claymorphism", clay_slides, single_theme_key="bento_glass_dark")

    # Paradigm 3: Photorealistic Textured Art (Marble & Gold)
    photo_slides = [s for s in MASTER_PARADIGM_SLIDES if s["layout"] in ("title_hero", "quadrant_matrix_2x2")]
    build_deck("Paradigm_3_Photorealistic_Textured_Art", photo_slides, single_theme_key="royal_gold_dark")

    # Paradigm 4: 2D Blueprint Schematic
    cad_slides = [s for s in MASTER_PARADIGM_SLIDES if s["layout"] in ("title_hero", "closing_thankyou")]
    build_deck("Paradigm_4_Technical_2D_Blueprint", cad_slides, single_theme_key="blueprint_cad_dark")

    print("\n[ALL 5 SHOWCASE DECKS GENERATED SUCCESSFULLY!]")


if __name__ == "__main__":
    main()
