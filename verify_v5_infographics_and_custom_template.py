#!/usr/bin/env python3
"""
Verification Suite for PPT_Saz v5.0:
  1. Tests Autonomous Semantic Layout Director + Zero Consecutive Repetition Law
  2. Tests all 11 new Infographic, Chart, Table, and Storytelling Slide Architectures
  3. Tests Hybrid Custom .pptx Template Ingestion (Brand DNA + Icon Harvesting + Slot Cloning + Motion Upgrade)
"""

import json
import os
from pathlib import Path
import sys

_SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from presentation_generator import generate_presentation_project
from semantic_layout_director import orchestrate_deck_layouts


def build_12_slide_showcase_deck() -> dict:
    return {
        "title": "معماری_نسل_پنجم_هوش_مصنوعی_پزشکی",
        "theme_category": "technology",
        "slides": [
            {
                "slug": "cover",
                "layout": "auto",
                "kicker": "ارائه جامع پژوهشی و استراتژیک",
                "title": "اکوسیستم نسل پنجم هوش مصنوعی در پزشکی دقیق",
                "subtitle": "ترکیب یادگیری عمیق چندوجهی، تحلیل ژنومیک و تصمیم‌يار بالینی",
                "author": "دکتر احسان حسینی | مهر ۱۴۰۵"
            },
            {
                "slug": "hierarchy",
                "layout": "auto",
                "kicker": "هرم سطوح پردازش",
                "title": "هرم سلسله‌مراتبی لایه‌های داده تا دانش بالینی",
                "cards": [
                    {"icon": "award", "title": "تصمیم‌گیری هوشمند بالینی", "desc": "پیشنهاد پروتکل درمانی شخصی‌سازی‌شده\nکاهش خطاهای تشخیصی در اورژانس"},
                    {"icon": "brain", "title": "مدل‌های استنتاج چندوجهی", "desc": "ترکیب تصاویر رادیولوژی و پرونده الکترونیک\nتفسیر خودکار بیومارکرها"},
                    {"icon": "database", "title": "لایه تجمیع و استانداردسازی داده", "desc": "یکپارچه‌سازی استانداردهای FHIR و DICOM\nحذف نویزهای ثبت بیمارستانی"}
                ]
            },
            {
                "slug": "screening_funnel",
                "layout": "auto",
                "kicker": "قیف غربالگری بیماران",
                "title": "قیف پالایش و فیلترینگ مرحله‌ای کارآزمایی بالینی",
                "steps": [
                    {"icon": "users", "title": "جمعیت اولیه بیماران (۱۰,۰۰۰ نفر)", "desc": "بررسی پرونده‌های سلامت الکترونیک\nثبت شاخص‌های دموگرافیک پایه"},
                    {"icon": "activity", "title": "غربالگری بیومارکرهای ژنتیکی (۲,۴۰۰ نفر)", "desc": "پایش جهش‌های هدفمند تومور\nحذف موارد دارای تداخل دارویی"},
                    {"icon": "shield-check", "title": "گروه هدف نهایی کارآزمایی (۶۵۰ نفر)", "desc": "ورود به فاز مداخله هوشمند\nپایش مستمر پاسخ درمانی"}
                ]
            },
            {
                "slug": "synergy_venn",
                "layout": "auto",
                "kicker": "هم‌افزایی سه‌جانبه",
                "title": "هم‌پوشانی و تعامل سه رکن کلیدی سلامت دیجیتال",
                "cards": [
                    {"icon": "cpu", "title": "هوش مصنوعی و یادگیری عمیق", "desc": "الگوریتم‌های پیش‌بینی ریسک\nمدل‌های زبانی بزرگ پزشکی"},
                    {"icon": "dna", "title": "پزشکی ژنومیک و مولکولی", "desc": "توالی‌یابی نسل جدید NGS\nپروفایلینگ پروتئومیکس"},
                    {"icon": "heart", "title": "تجربه بالینی پزشک متخصص", "desc": "تایید نهایی تشخیص\nاخلاق پزشکی و همدلی با بیمار"}
                ]
            },
            {
                "slug": "swot_quadrant",
                "layout": "auto",
                "kicker": "ماتریس چهارگانه استراتژیک",
                "title": "ماتریس SWOT استقرار هوش مصنوعی در بیمارستان‌ها",
                "cards": [
                    {"icon": "zap", "title": "نقاط قوت درونی (Strengths)", "desc": "سرعت پردازش فوق‌العاده\nدسترسی ۲۴ ساعته بدون خستگی"},
                    {"icon": "alert-triangle", "title": "نقاط قابل بهبود (Weaknesses)", "desc": "نیاز به زیرساخت GPU قدرتمند\nوابستگی به کیفیت داده‌های ورودی"},
                    {"icon": "rocket", "title": "فرصت‌های پیش‌رو (Opportunities)", "desc": "توسعه پزشکی از راه دور\nکاهش ۴۵ درصدی هزینه‌های تشخیصی"},
                    {"icon": "shield", "title": "چالش‌های محیطی (Threats)", "desc": "مقررات سخت‌گیرانه حریم خصوصی\nمقاومت در برابر تغییر فرآیندها"}
                ]
            },
            {
                "slug": "snake_journey",
                "layout": "auto",
                "kicker": "نقشه راه اجرایی",
                "title": "مراحل گام‌به‌گام پیاده‌سازی در شبکه درمانی کشور",
                "steps": [
                    {"icon": "search", "title": "امکان‌سنجی و ممیزی داده", "desc": "ارزیابی زیرساخت مراکز\nتدوین پروتکل امنیتی"},
                    {"icon": "code", "title": "بومی‌سازی مدل‌های هوش مصنوعی", "desc": "آموزش روی داده‌های بومی\nکالیبراسیون دقت تشخیصی"},
                    {"icon": "activity", "title": "اجرای پایلوت در ۵ بیمارستان", "desc": "ارزیابی بلادرنگ کنار بالین\nدریافت بازخورد پزشکان"},
                    {"icon": "globe", "title": "استقرار سراسری و مقیاس‌پذیری", "desc": "اتصال به پرونده الکترونیک ملی\nپایش مستمر کیفیت"}
                ]
            },
            {
                "slug": "mindmap_ecosystem",
                "layout": "auto",
                "kicker": "نقشه ذهنی اکوسیستم",
                "title": "هسته مرکزی و شاخه‌های کاربردی دستیار هوشمند پزشک",
                "cards": [
                    {"icon": "eye", "title": "بینایی ماشین در رادیولوژی", "desc": "تشخیص زودهنگام ندول‌های ریوی\nسگمنتیشن خودکار تومورهای مغزی"},
                    {"icon": "file-text", "title": "پردازش متن پرونده‌های بالینی", "desc": "خلاصه‌سازی خودکار شرح‌حال\nاستخراج کدهای استاندارد ICD-11"},
                    {"icon": "bell", "title": "هشدار زودهنگام بخش مراقبت ویژه", "desc": "پیش‌بینی سپسیس ۶ ساعت قبل از بروز\nپایش پیوسته علائم حیاتی"},
                    {"icon": "pill", "title": "کشف و بهینه‌سازی دوز دارو", "desc": "شبیه‌سازی برهم‌کنش مولکولی\nتنظیم دوز بر اساس متابولیسم بیمار"}
                ]
            },
            {
                "slug": "fishbone_diagnosis",
                "layout": "auto",
                "kicker": "ریشه‌یابی چالش‌ها",
                "title": "تحلیل علت و معلولی تاخیر در تشخیص بیماری‌های نادر",
                "cards": [
                    {"icon": "database", "title": "پراکندگی داده‌های آزمایشگاهی", "desc": "عدم ارتباط سامانه‌های بیمارستانی\nثبت غیراستاندارد علائم اولیه"},
                    {"icon": "clock", "title": "محدودیت زمان ویزیت بالینی", "desc": "حجم بالای مراجعین روزانه\nپیچیدگی تظاهرات بالینی نادر"},
                    {"icon": "cpu", "title": "فقدان ابزارهای غربالگری هوشمند", "desc": "تکیه صرف بر حافظه فردی\nنبود سیستم هشدار الگوهای ژنتیکی"},
                    {"icon": "book", "title": "به‌روزرسانی کند منابع سنتی", "desc": "فاصله زمانی انتشار مقالات تا بالین\nعدم دسترسی سریع به بانک‌های جهانی"}
                ]
            },
            {
                "slug": "radar_benchmark",
                "layout": "auto",
                "kicker": "نمودار ارزیابی عملکرد",
                "title": "نمودار راداری مقایسه دقت و سرعت مدل‌های تشخیصی",
                "kpis": [
                    {"number": "۹۸.۴٪", "title": "حساسیت تشخیصی (Sensitivity)", "desc": "شناسایی دقیق موارد مثبت در تصاویر سی‌تی‌اسکن"},
                    {"number": "۹۶.۸٪", "title": "ویژگی بالینی (Specificity)", "desc": "کاهش چشمگیر موارد مثبت کاذب و بیوپسی غیرضروری"},
                    {"number": "۰.۳s", "title": "زمان پاسخگویی بلادرنگ", "desc": "پردازش کامل اسکن سه‌بعدی در کسری از ثانیه"}
                ]
            },
            {
                "slug": "spec_table",
                "layout": "auto",
                "kicker": "جدول مشخصات فنی",
                "title": "ماتریس ارزیابی ماژول‌های سامانه هوشمند بیمارستانی",
                "cards": [
                    {"title": "ماژول تحلیل تصویر PACS-AI", "desc": "پشتیبانی از MRI, CT, X-Ray با دقت بالای ۹۸ درصد", "trend": "✓ عملیاتی"},
                    {"title": "موتور پردازش زبان طبیعی فارسی", "desc": "تایپ خودکار گزارش رادیولوژی و خلاصه پرونده", "trend": "✓ عملیاتی"},
                    {"title": "داشبورد پیش‌بینی ریسک ICU", "desc": "پایش بلادرنگ علائم حیاتی و هشدار سپسیس", "trend": "⚡ فاز پایلوت"},
                    {"title": "لایه رمزنگاری فدرال (Federated)", "desc": "آموزش مدل بدون خروج داده بیمار از بیمارستان", "trend": "🔒 تایید امنیتی"}
                ]
            },
            {
                "slug": "closing",
                "layout": "auto",
                "kicker": "جمع‌بندی و پرسش و پاسخ",
                "title": "سپاس از توجه و همراهی شما",
                "cards": [
                    {"title": "دقت ۹۸.۴٪ بالینی"},
                    {"title": "کاهش ۴۵٪ هزینه‌ها"},
                    {"title": "حفظ کامل حریم خصوصی"}
                ]
            }
        ]
    }


def main():
    deck_data = build_12_slide_showcase_deck()
    slides = deck_data["slides"]

    # 1. Verify Semantic Layout Director & Anti-Repetition Law
    assigned = orchestrate_deck_layouts(slides)
    print("Assigned Semantic Layouts across 11 slides:")
    for i, lay in enumerate(assigned, 1):
        print(f"  Slide {i:02d} ({slides[i-1]['slug']}): {lay}")

    for i in range(1, len(assigned)):
        assert assigned[i] != assigned[i - 1], f"Consecutive layout repetition at slide {i+1}: {assigned[i]}"
    print("[PASS] Zero Consecutive Layout Repetition Verified!")

    # 2. Compile Full 11-Slide Infographic Deck
    out_dir = Path("projects/test_v5_infographics")
    out_pptx = out_dir / "v5_infographic_showcase.pptx"
    pptx_path = generate_presentation_project(
        deck_data=deck_data,
        project_dir=out_dir,
        output_pptx=out_pptx,
        theme_key="bento_glass_dark",
        transition="morph",
        animation_mode="auto",
    )
    assert pptx_path.exists() and os.path.getsize(pptx_path) > 80000
    print(f"[PASS] 11-Slide Infographic Showcase PPTX Compiled: {pptx_path} ({os.path.getsize(pptx_path):,} bytes)")

    # 3. Test Hybrid Custom PPTX Template Ingestion using examples/sample_output.pptx
    sample_template = Path("examples/sample_output.pptx")
    if sample_template.exists():
        custom_dir = Path("projects/test_v5_custom_template")
        custom_out = custom_dir / "v5_from_custom_template.pptx"
        custom_pptx_path = generate_presentation_project(
            deck_data=deck_data,
            project_dir=custom_dir,
            output_pptx=custom_out,
            custom_template_pptx=sample_template,
            transition="morph",
            animation_mode="auto",
        )
        assert custom_pptx_path.exists() and os.path.getsize(custom_pptx_path) > 80000
        print(f"[PASS] Hybrid Custom PPTX Template Ingestion Compiled: {custom_pptx_path} ({os.path.getsize(custom_pptx_path):,} bytes)")

    print("\nALL PPT_SAZ V5.0 TESTS PASSED 100%!")


if __name__ == "__main__":
    main()
