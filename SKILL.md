---
name: ppt-saz
description: >
  AI Presentation Director & Native PowerPoint (PPTX) Generator with intelligent layout design,
  automated AI image sourcing, cinematic transitions (Morph, Fade, Push), staggered element animations,
  and full native bilingual (Persian RTL / English LTR) typography.
  Use when the user asks to create, design, generate, or beautify PowerPoint presentations (.pptx),
  turn text/notes into slides, or mentions "پاورپوینت", "اسلاید", "presentation", "PPT", or "PPT_Saz".
---

# اسکیل ساخت خودکار و نیتیو پاورپوینت (PPT_Saz)

این اسکیل برای تولید ارائه‌های فوق‌العاده زیبا، مدرن و **۱۰۰٪ نیتیو و قابل ویرایش در مایکروسافت پاورپوینت (.pptx)** طراحی شده است. بر خلاف ابزارهای سنتی که اسلایدهای خشک تولید می‌کنند یا ابزارهایی که فقط عکس اسلاید را می‌گذارند، `PPT_Saz` اسلایدها را به صورت برداری (DrawingML) با انیمیشن‌های ورود گام‌به‌گام و ترنزیشن‌های حرکتی معنادار می‌سازد.

---

## 🎯 فرآیند اجرایی هوش مصنوعی (AI Execution Workflow)

هنگامی که کاربر متن، یادداشت‌ها یا موضوع ارائه را به شما می‌دهد، این ۵ گام را به ترتیب طی کنید:

### گام ۱: کارگردانی محتوا و استوری‌بورد (Storyboarding)
متن کاربر را تحلیل کرده و به اسلایدهای ساختاریافته تبدیل کنید. برای هر اسلاید یکی از چیدمان‌های بهینه‌شده زیر را انتخاب نمایید:
1. `title_hero`: اسلاید عنوان جذاب + زیرعنوان + نام ارائه‌دهنده + تصویر شاخص
2. `content_cards`: ۲ تا ۴ کارت مدرن با آیکون/بج، تیترهای برجسته و توضیحات
3. `split_image`: ترکیب متن تحلیلی/بولت‌های گام‌به‌گام در یک سمت و تصویر باکیفیت در سمت دیگر
4. `stats_kpi`: اعداد و شاخص‌های کلیدی آماری (KPIs) با توضیحات شفاف
5. `comparison`: مقایسه دو دیدگاه یا وضعیت قبل و بعد

### گام ۲: انتخاب تم و پالت رنگی (Theme Selection)
بر اساس موضوع ارائه، یکی از پالت‌های حرفه‌ای `presets/themes.json` را انتخاب کنید:
- `corporate_blue`: رسمی، شرکتی، فناوری و گزارش‌های مدیریتی (سرمه‌ای و فیروزه‌ای)
- `modern_dark_indigo`: استارتاپی، مدرن، وب۳ و هوش مصنوعی (تم تیره نئونی)
- `clean_academic`: دانشگاهی، مقالات، پزشکی و محیط‌های علمی (روشن و تمیز)
- `emerald_tech`: زیست‌فناوری، انرژی، مالی و نوآوری سبز (سبز زمردی)
- `warm_terracotta`: هنر، خلاقیت، معماری و علوم انسانی (آجری و کرم گرم)

### گام ۳: تأمین تصویر برای هر اسلاید (Image Acquisition)
برای هر اسلاید که نیاز به تصویر دارد:
- یک عبارت جستجوی دقیق انگلیسی (`image_prompt`) مانند:
  - `futuristic artificial intelligence neural network glowing cyber blue`
  - `clinical doctor reviewing medical research data hospital laboratory`
- سیستم خودکار تصاویر را از آرشیو باکیفیت دانلود کرده یا جایگزین‌های مناسب گرافیکی قرار می‌دهد. همچنین در صورت فعال بودن ابزار تولید عکس هوش مصنوعی (`generate_image`)، می‌توانید تصویر را مستقیماً بسازید و در `images/` ذخیره کنید.

### گام ۴: کارگردانی حرکتی (Transitions & Animations)
- **ترنزیشن بین اسلایدها:**
  - `fade`: محو و ظاهر شدن نرم (عالی برای جابجایی بین بخش‌ها)
  - `push` یا `wipe`: جهت‌دار و پویا (مناسب برای فرآیندهای متوالی)
  - `morph`: برای ارتباط مفهومی عمیق بین دو اسلاید مرتبط
- **انیمیشن المان‌ها:**
  - المان‌ها به صورت پیش‌فرض با حالت `after-previous` و با تأخیر استگر (0.35 ثانیه) ظاهر می‌شوند:
    - ابتدا تیتر و کادر اصلی (`entrance_fade`)
    - سپس کارت‌ها یا بولت‌ها یکی‌یکی (`entrance_fly` یا `entrance_wipe`)
    - و در نهایت تصاویر شاخص

### گام ۵: اجرای اسکریپت تولید و تحویل فایل
اطلاعات استوری‌بورد را در قالب یک فایل موقت JSON ذخیره کرده و دستور زیر را اجرا کنید:

```powershell
python scripts/presentation_generator.py input_deck.json -p project_run -o final_presentation.pptx --theme corporate_blue -t fade -a auto
```

---

## 📋 ساختار داده ورودی JSON (Input Deck Format)

```json
{
  "title": "هوش_مصنوعی_و_آینده_یادگیری_ماشین",
  "theme_category": "technology",
  "slides": [
    {
      "slug": "cover",
      "layout": "title_hero",
      "title": "عنوان اسلاید اول",
      "subtitle": "زیرعنوان توضیحی ارائه",
      "author": "ارائه‌دهنده: نام شما",
      "image_prompt": "modern technology concept high resolution",
      "notes": "یادداشت‌های ارائه سخنران برای اسلاید اول"
    },
    {
      "slug": "features",
      "layout": "content_cards",
      "kicker": "ویژگی‌های اصلی",
      "title": "سه مزیت کلیدی سیستم",
      "cards": [
        { "title": "قابلیت ۱", "desc": "توضیح کامل مورد اول\nنکته دوم" },
        { "title": "قابلیت ۲", "desc": "توضیح کامل مورد دوم\nنکته دوم" },
        { "title": "قابلیت ۳", "desc": "توضیح کامل مورد سوم\nنکته دوم" }
      ],
      "notes": "متن یادداشت سخنران برای این اسلاید"
    },
    {
      "slug": "deep_dive",
      "layout": "split_image",
      "kicker": "بررسی موردی",
      "title": "تحلیل عملکرد و پیاده‌سازی",
      "bullets": [
        "افزایش ۴۰ درصدی سرعت پردازش داده‌ها",
        "کاهش هزینه‌های زیرساختی و مصرف منابع",
        "همگام‌سازی بی‌درنگ با پروتکل‌های ابری"
      ],
      "image_prompt": "cloud servers infrastructure data analytics",
      "notes": "یادداشت‌های نهایی"
    }
  ]
}
```

---

## 🛠️ دستورات خط فرمان مستقیم (CLI Usage)

```bash
# ساخت پاورپوینت کامل از فایل JSON:
python scripts/presentation_generator.py deck.json -o my_slides.pptx

# تغییر تم و ترنزیشن:
python scripts/presentation_generator.py deck.json -o my_slides.pptx --theme modern_dark_indigo -t push -a auto

# کامپایل مستقیم یک پوشه از اسلایدهای SVG به PPTX:
python scripts/svg_to_pptx.py my_project_dir -o output.pptx -t fade -a auto
```
