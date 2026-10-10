---
name: ppt-saz
description: >
  AI Presentation Director & Native PowerPoint (PPTX) Generator with Slidesgo-grade creative layouts,
  5000+ vector icons, automated AI image sourcing, cinematic transitions (Morph, Fade, Push),
  staggered element animations, and native bilingual (Persian RTL with Yekan Bakh / English LTR) typography.
  Use when the user asks to create, design, generate, or beautify PowerPoint presentations (.pptx),
  turn text/notes into slides, or mentions "پاورپوینت", "اسلاید", "presentation", "PPT", or "PPT_Saz".
---

# اسکیل ساخت خودکار و نیتیو پاورپوینت (PPT_Saz v2.0 - Slidesgo Grade)

این اسکیل برای تولید ارائه‌های فوق‌العاده چشم‌نواز، گرافیکی، متنوع و **۱۰۰٪ نیتیو و قابل ویرایش در مایکروسافت پاورپوینت (.pptx)** طراحی شده است. 

این نسخه با الهام از استانداردهای دیزاین **Slidesgo و Pitch** ارتقا یافته است:
- **تنوع چیدمان بدون کشیدگی متون:** ۶ الگوی اسلاید مدرن (کاور سینماتیک، فرآیند گام‌به‌گام متصل، آمار و ارقام بزرگ KPI، مقایسه دوراهی، کارت‌های آیکون‌دار و نمایش دوتکه).
- **آرشیو ۵۰۰۰+ آیکون وکتور محلی:** تطبیق خودکار هوشمند موضوع کارت‌ها با آیکون‌های وکتور برداری (Tabler Icons).
- **المان‌های گرافیکی و هندسی ظریف:** پترن‌های شبکه‌ای نقطه‌ای مات (Dot Matrix Grid) و فرم‌های کپسولی معلق.
- **تایپوگرافی رسمی فونت «یکان‌بخ» (Yekan Bakh):** نصب‌شده در سیستم و فعال در تمام اسلایدهای فارسی به همراه فونت‌های انگلیسی مدرن (Inter, Segoe UI).
- **انیمیشن و ترنزیشن نیتیو:** ۴۸ ترنزیشن پاورپوینت (Morph, Fade, Push و ...) و ۲۰۳ پریست انیمیشن ورود آبجکت‌ها.

---

## 🎯 فرآیند اجرایی هوش مصنوعی (AI Execution Workflow)

هنگامی که کاربر متن، یادداشت‌ها یا موضوع ارائه را به شما می‌دهد، این ۵ گام را به ترتیب طی کنید:

### گام ۱: کارگردانی محتوا و انتخاب الگوهای متنوع Slidesgo
متن را بر اساس سناریو به اسلایدهای کوتاه، فشرده و جذاب با چیدمان‌های متنوع تبدیل کنید:
1. `title_hero`: کاور با برچسب کپسولی موضوع (`kicker`)، عنوان درشت، زیرعنوان، مشخصات سخنران و تصویر شاخص قاب‌دار.
2. `content_cards`: ۲ تا ۴ کارت افقی گرد شده با آیکون وکتور در بج رنگی، خطوط تفکیک و نکات کلیدی.
3. `process_steps`: فرآیند ۳ یا ۴ مرحله‌ای با خطوط اتصال، شماره گام‌ها (۰۱، ۰۲، ۰۳)، آیکون اختصاصی و توضیحات مرحله.
4. `stats_kpi`: کارت‌های نمایش اعداد بسیار درشت شاخص‌ها (`+۸۵٪`، `۴.۲x`) همراه با بج ترند (`↑ رشد دوبرابری`) و عکس زمینه یا سایدبار.
5. `comparison`: مقایسه دوراهی بین وضعیت سنتی و مدرن با آیکون‌های ضربدر و تیک.
6. `split_image`: ترکیب هوشمند متن‌های دارای آیکون چک‌مارک در یک سو و تصویر باکیفیت در سوی دیگر.

### گام ۲: انتخاب تم و پالت رنگی (Theme Selection)
- `corporate_blue`: رسمی، شرکتی، فناوری و گزارش‌های تحلیلی (سرمه‌ای، فیروزه‌ای و کهربایی)
- `modern_dark_indigo`: استارتاپی، مدرن، وب۳ و هوش مصنوعی (تم تیره نئونی و بنفش)
- `clean_academic`: دانشگاهی، مقالات، پزشکی و محیط‌های علمی (روشن، سفید و سرمه‌ای)
- `emerald_tech`: زیست‌فناوری، انرژی، مالی و نوآوری سبز (سبز زمردی)
- `warm_terracotta`: هنر، خلاقیت، معماری و علوم انسانی (آجری و کرم گرم)

### گام ۳: تأمین تصویر برای هر اسلاید (Image Acquisition)
برای هر اسلاید که نیاز به تصویر دارد، یک پرامپت انگلیسی توصیفی (`image_prompt`) بنویسید (مثلاً `futuristic ai brain glowing data network`). سیستم خودکار تصویر باکیفیت دانلود می‌کند یا در صورت فراخوانی ابزار `generate_image` از رندرهای هوش مصنوعی استفاده می‌نماید.

### گام ۴: کارگردانی حرکتی (Transitions & Animations)
- ترنزیشن‌ها: `fade` (نرم و شیک)، `push` (جهت‌دار برای مراحل متوالی)، `morph` (تغییر تدریجی).
- انیمیشن ورود المان‌ها: پیش‌فرض روی `-a auto` تنظیم است که کارت‌ها، آیکون‌ها و تصاویر را با تأخیر استگر (0.35s) پشت سر هم وارد می‌کند.

### گام ۵: اجرای اسکریپت تولید و تحویل فایل
استوری‌بورد را در قالب یک فایل JSON ذخیره کرده و دستور زیر را اجرا کنید:

```powershell
python scripts/presentation_generator.py input_deck.json -p project_run -o final_presentation.pptx --theme corporate_blue -t fade -a auto
```

---

## 📋 ساختار داده ورودی JSON (Input Deck Format)

```json
{
  "title": "عنوان_ارائه",
  "theme_category": "technology",
  "slides": [
    {
      "slug": "cover",
      "layout": "title_hero",
      "kicker": "ارائه تخصصی فناوری",
      "title": "هوش مصنوعی و یادگیری ماشین",
      "subtitle": "تحول بنیادین در صنایع نوین",
      "author": "ارائه‌دهنده: نام شما",
      "image_prompt": "futuristic artificial intelligence neural network"
    },
    {
      "slug": "features",
      "layout": "content_cards",
      "kicker": "ستون‌های اصلی",
      "title": "سه ستون محوری معماری",
      "cards": [
        { "icon": "brain", "title": "یادگیری عمیق", "desc": "مدل‌های زبانی بزرگ\nپردازش صوت و تصویر" },
        { "icon": "cpu", "title": "زیرساخت ابری", "desc": "کلاسترهای پردازش گرافیکی\nمقیاس‌پذیری آنی" },
        { "icon": "shield-check", "title": "امنیت و انطباق", "desc": "رمزنگاری کامل داده‌ها\nحفظ حریم خصوصی" }
      ]
    },
    {
      "slug": "roadmap",
      "layout": "process_steps",
      "kicker": "نقشه راه",
      "title": "مراحل گام‌به‌گام پیاده‌سازی",
      "steps": [
        { "icon": "database", "title": "یکپارچگی داده", "desc": "پاک‌سازی و ورود اطلاعات" },
        { "icon": "rocket", "title": "آموزش مدل", "desc": "تنظیم دقیق و بهینه‌سازی" },
        { "icon": "gauge", "title": "پایش بلادرنگ", "desc": "نظارت بر کارایی و تاخیر" }
      ]
    },
    {
      "slug": "impact",
      "layout": "stats_kpi",
      "kicker": "شاخص‌های کلیدی",
      "title": "جهش بهره‌وری سازمانی",
      "image_prompt": "modern business growth analytics",
      "kpis": [
        { "number": "+۸۵٪", "trend": "↑ رشد بهره‌وری", "title": "افزایش سرعت تصمیم‌گیری", "desc": "کاهش زمان تحلیل فرآیندها" },
        { "number": "۴.۲x", "trend": "↑ نرخ بازگشت", "title": "ارزش‌آفرینی تجاری", "desc": "کاهش ۶۰٪ هزینه‌های عملیاتی" }
      ]
    },
    {
      "slug": "comparison",
      "layout": "comparison",
      "kicker": "تحلیل تطبیقی",
      "title": "مقایسه روش‌های سنتی با سامانه هوشمند",
      "col_a": {
        "title": "روش‌های سنتی",
        "items": ["سرعت کند پردازش دستی", "خطای بالای انسانی", "هزینه‌های نگهداری سنگین"]
      },
      "col_b": {
        "title": "سامانه هوشمند",
        "items": ["پردازش آنی میلیون‌ها رکورد", "دقت بالای ۹۹.۲ درصد", "کاهش ۶۰ درصدی هزینه‌ها"]
      }
    }
  ]
}
```
