#!/usr/bin/env python3
"""
Verification & Showcase Suite for PPT_Saz v5.5 — 9 Polymorphic Art-Style Visual Skins

Generates:
  1. `output/PPT_Saz_v55_9_ArtStyles_Master_Showcase.pptx` (9 slides, each in a different Art Style!)
  2. Individual multi-slide showcase decks for the signature Art Styles:
     - `output/ArtStyle_1_NeoBrutalist_RetroOS.pptx`
     - `output/ArtStyle_2_Bauhaus_Weimar1923.pptx`
     - `output/ArtStyle_3_PaperCutout_MemphisPop.pptx`
     - `output/ArtStyle_4_Blueprint_CAD_Schematic.pptx`
     - `output/ArtStyle_5_CyberHUD_SciFi.pptx`
     - `output/ArtStyle_6_RoyalGold_ArtDeco.pptx`
     - `output/ArtStyle_7_WarmEditorial_RomanArch.pptx`
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


SAMPLE_DECK_SLIDES = [
    {
        "layout": "title_hero",
        "kicker": "نسخه ۵.۵ — موتور چندریختی آرت‌استایل",
        "title": "تحول بنیادین زبان بصری و آرت‌استایل‌ها",
        "subtitle": "تغییر کامل شکل کادرها، هدرها، قاب آیکون‌ها و بوم پس‌زمینه در ۹ مکتب هنری\nحفظ ۱۰۰٪ متن کاربر + انیمیشن چرخشی ممتد + ترنزیشن Morph",
        "author": "طراحی و مهندسی: اسکیل PPT_Saz v5.5",
    },
    {
        "layout": "pyramid_hierarchy",
        "kicker": "هرم سلسله‌مراتبی",
        "title": "سطوح چهارگانه معماری بصری در اسکیل جدید",
        "cards": [
            {"title": "سطح ۱: هندسه کادرها (Silhouette)", "desc": "تغییر از مستطیل ساده به پنجره رترو، طاق رومی و چندضلعی\nحذف یکنواختی در تمام اسلایدها", "icon": "layers"},
            {"title": "سطح ۲: هدر و سرصفحه اختصاصی", "desc": "برچسب کج نئوبروتالیسم، مهر مهندسی CAD و بال‌های سلطنتی\nهماهنگی کامل با روح هر آرت‌استایل", "icon": "award"},
            {"title": "سطح ۳: قاب آیکون چندریختی", "desc": "شش‌ضلعی سایبری، ستاره ۸ پر طلایی، کلاژ کاغذی و نشان باهاوس\nتغییر خودکار در دل تمام ۱۱ نمودار", "icon": "sparkles"},
            {"title": "سطح ۴: بوم پس‌زمینه و المان چرخان", "desc": "چرخ‌دنده کولیس مهندسی، فرفره کاغذی، موبایل باهاوس و رادار\nحرکت ممتد بدون توقف بین اسلایدها", "icon": "compass"},
        ],
    },
    {
        "layout": "quadrant_matrix_2x2",
        "kicker": "ماتریس استراتژیک ۲×۲",
        "title": "تحلیل چهارگانه تمایز بصری و تجربه مخاطب",
        "cards": [
            {"title": "تمایز در نگاه اول", "desc": "تشخیص فوری سبک هنری در کمتر از ۱ ثانیه\nایجاد حس شگفتی در ارائه", "icon": "eye"},
            {"title": "خوانایی و تایپوگرافی یکان باخ", "desc": "حفظ کامل سلسله‌مراتب دیداری و راست‌چین فارسی\nکنتراست استاندارد در تم‌های تیره و روشن", "icon": "check"},
            {"title": "تنوع ۱۸ ساختار و نمودار", "desc": "ترکیب ۹ آرت‌استایل با ۱۸ نوع دیاگرام (۱۶۲ حالت منحصربه‌فرد)\nقانون عدم تکرار ساختار در اسلایدهای متوالی", "icon": "cpu"},
            {"title": "سازگاری ۱۰۰٪ با پاورپوینت", "desc": "تبدیل مستقیم به اشکال بومی DrawingML\nبدون نیاز به اینترنت یا فونت خارجی در زمان پخش", "icon": "shield"},
        ],
    },
    {
        "layout": "snake_roadmap",
        "kicker": "نقشه راه موجی",
        "title": "فرآیند گام‌به‌گام تولید ارائه با آرت‌استایل اختصاصی",
        "steps": [
            {"title": "گام اول: دریافت متن", "desc": "دریافت دقیق تیتر و متن هر اسلاید\nقفل ۱۰۰٪ متن بدون تغییر یا خلاصه‌سازی", "icon": "file-text"},
            {"title": "گام دوم: انتخاب آرت‌استایل", "desc": "انتخاب از بین ۹ مکتب هنری متمایز\nپیشنهاد هوشمند بر اساس موضوع ارائه", "icon": "palette"},
            {"title": "گام سوم: کارگردانی چیدمان", "desc": "تخصیص خودکار هرم، قیف، ون، ماتریس و جدول\nجلوگیری از تکرار چیدمان در اسلایدهای پشت‌سرهم", "icon": "sliders"},
            {"title": "گام چهارم: کامپایل بومی PPTX", "desc": "تزریق انیمیشن‌های چرخشی ممتد و ترنزیشن مورف\nخروجی آماده ارائه با یک کلیک", "icon": "rocket"},
        ],
    },
    {
        "layout": "smart_table_matrix",
        "kicker": "جدول مقایسه‌ای هوشمند",
        "title": "مقایسه مشخصات فنی ۹ آرت‌استایل در نسخه ۵.۵",
        "cards": [
            {"title": "Neo-Brutalist & Paper Cutout", "desc": "پنجره سیستم‌عامل رترو با دکمه‌های رنگی / کلاژ کاغذی با چسب نواری", "trend": "★ پاپ و خلاقانه"},
            {"title": "Bauhaus 1923 & Swiss Grid", "desc": "بلوک‌های هندسی قرمز/آبی/زرد باهاوس / شبکه خط‌کشیده مهندسی سوئیسی", "trend": "■ مدرن و علمی"},
            {"title": "Blueprint CAD & Cyber HUD", "desc": "نقشه سیانوتایپ مهندسی با خطوط امتدادیافته / کاکپیت علمی-تخیلی ۴۵ درجه", "trend": "⊕ فنی و تکنولوژیک"},
            {"title": "Royal Gold, Editorial & Bento", "desc": "هشت‌ضلعی جواهری سلطنتی / طاق معماری رومی / اسکوئیرکل شیشه‌ای اپل", "trend": "◆ لوکس و ژورنالی"},
        ],
    },
]


def build_master_9_art_styles_comparison(themes: dict, out_dir: Path) -> Path:
    """Builds a 9-slide PPTX where each slide renders one of the 9 distinct Art-Style Archetypes."""
    work_dir = out_dir / "_work_master_9_styles"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    svg_dir = work_dir / "svg_output"
    svg_dir.mkdir(parents=True, exist_ok=True)

    nine_style_configs = [
        ("neo_brutalist_light", "content_cards", "۱. استایل Neo-Brutalist — پنجره رترو و سایه سخت"),
        ("bauhaus_weimar_light", "pyramid_hierarchy", "۲. استایل Bauhaus 1923 — بلوک‌های هندسی رنگ‌های اصلی"),
        ("paper_cutout_pop", "snake_roadmap", "۳. استایل Paper Cutout — کلاژ کاغذی و چسب نواری ممفیس"),
        ("blueprint_cad_dark", "quadrant_matrix_2x2", "۴. استایل Blueprint CAD — نقشه مهندسی و خطوط امتدادیافته"),
        ("cyber_aurora", "mind_map_hub", "۵. استایل Cyber HUD — چندضلعی برش‌خورده و رادار فضایی"),
        ("royal_gold_dark", "venn_synergy", "۶. استایل Royal Gold — هشت‌ضلعی جواهری و بال‌های سلطنتی"),
        ("warm_editorial_light", "funnel_pipeline", "۷. استایل Warm Editorial — طاق رومی و سرصفحه مجله‌ای"),
        ("swiss_academic_light", "smart_table_matrix", "۸. استایل Swiss Academic — شبکه خط‌کشیده و چهارراه ثبت"),
        ("bento_glass_dark", "data_chart_showcase", "۹. استایل Apple Bento — اسکوئیرکل شیشه‌ای و داینامیک آیلند"),
    ]

    for idx, (theme_key, layout_type, custom_title) in enumerate(nine_style_configs, start=1):
        theme = themes[theme_key]
        renderer = SlideRenderer(theme)
        base_slide = dict(SAMPLE_DECK_SLIDES[(idx % (len(SAMPLE_DECK_SLIDES) - 1)) + 1])
        base_slide["title"] = custom_title
        base_slide["kicker"] = theme["name"]

        if layout_type == "content_cards":
            svg_str = renderer.render_content_cards_slide(base_slide, slide_idx=idx)
        elif layout_type == "pyramid_hierarchy":
            svg_str = InfographicLayoutRenderer.render_pyramid_hierarchy(renderer, base_slide, slide_idx=idx)
        elif layout_type == "snake_roadmap":
            svg_str = InfographicLayoutRenderer.render_snake_roadmap(renderer, base_slide, slide_idx=idx)
        elif layout_type == "quadrant_matrix_2x2":
            svg_str = InfographicLayoutRenderer.render_quadrant_matrix_2x2(renderer, base_slide, slide_idx=idx)
        elif layout_type == "mind_map_hub":
            svg_str = InfographicLayoutRenderer.render_mind_map_hub(renderer, base_slide, slide_idx=idx)
        elif layout_type == "venn_synergy":
            svg_str = InfographicLayoutRenderer.render_venn_synergy(renderer, base_slide, slide_idx=idx)
        elif layout_type == "funnel_pipeline":
            svg_str = InfographicLayoutRenderer.render_funnel_pipeline(renderer, base_slide, slide_idx=idx)
        elif layout_type == "smart_table_matrix":
            svg_str = InfographicLayoutRenderer.render_smart_table_matrix(renderer, base_slide, slide_idx=idx)
        else:
            svg_str = InfographicLayoutRenderer.render_data_chart_showcase(renderer, base_slide, slide_idx=idx)

        svg_path = svg_dir / f"slide_{idx:02d}.svg"
        svg_path.write_text(svg_str, encoding="utf-8")

    import json
    anim_cfg = generate_deck_animations_config(work_dir, transition="morph", animation_mode="auto")
    (work_dir / "animations.json").write_text(json.dumps(anim_cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    master_pptx = out_dir / "PPT_Saz_v55_9_ArtStyles_Master_Showcase.pptx"
    orig_argv = sys.argv[:]
    try:
        sys.argv = [
            "svg_to_pptx",
            str(work_dir),
            "-o", str(master_pptx),
            "-t", "morph",
            "-a", "auto",
            "--animation-trigger", "after-previous",
            "--animation-stagger", "0.35",
        ]
        svg_main()
    finally:
        sys.argv = orig_argv
    return master_pptx


def main() -> None:
    out_dir = ROOT / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    themes = load_themes()

    print(f"Loaded {len(themes)} themes across 9 Art-Style Archetypes.")
    master_pptx = build_master_9_art_styles_comparison(themes, out_dir)
    print(f"[OK] Built Master 9-Art-Style Comparison Deck: {master_pptx}")

    individual_decks = [
        ("neo_brutalist_light", "ArtStyle_1_NeoBrutalist_RetroOS.pptx"),
        ("bauhaus_weimar_light", "ArtStyle_2_Bauhaus_Weimar1923.pptx"),
        ("paper_cutout_pop", "ArtStyle_3_PaperCutout_MemphisPop.pptx"),
        ("blueprint_cad_dark", "ArtStyle_4_Blueprint_CAD_Schematic.pptx"),
        ("cyber_aurora", "ArtStyle_5_CyberHUD_SciFi.pptx"),
        ("royal_gold_dark", "ArtStyle_6_RoyalGold_ArtDeco.pptx"),
        ("warm_editorial_light", "ArtStyle_7_WarmEditorial_RomanArch.pptx"),
    ]

    for theme_key, filename in individual_decks:
        out_file = out_dir / filename
        deck_data = {
            "title": filename.replace(".pptx", ""),
            "theme": theme_key,
            "slides": [dict(s) for s in SAMPLE_DECK_SLIDES],
        }
        generate_presentation_project(
            deck_data=deck_data,
            project_dir=out_dir / f"_work_{theme_key}",
            output_pptx=out_file,
            theme_key=theme_key,
            transition="morph",
            animation_mode="auto",
        )
        assert out_file.exists() and out_file.stat().st_size > 20000
        with zipfile.ZipFile(out_file, "r") as zf:
            slide_xmls = [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            assert len(slide_xmls) == 5, f"Expected 5 slides in {filename}, got {len(slide_xmls)}"
        print(f"[OK] Verified 5-slide deck for {theme_key}: {out_file.name} ({out_file.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
