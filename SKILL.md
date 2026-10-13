---
name: ppt-saz
description: >
  AI Presentation Director & Native PowerPoint (PPTX) Generator (v5.0) with 6 distinct art styles
  (Cyber HUD, Swiss Academic, Neo-Brutalism, Apple Bento-Grid, Warm Botanical, Royal Gold Noir), 12 light/dark themes,
  18 specialized slide & infographic diagram layouts (Pyramid, Funnel, Venn, 2x2 Quadrant SWOT, Snake Roadmap, Mind-Map,
  Fishbone, Vector Radar Charts, Smart Tables), Autonomous Semantic Anti-Repetition Layout Director,
  Hybrid Custom .pptx Template & Icon Ingestion (--template-pptx), 5000+ vector icons, single-click Morph transitions,
  continuous looping particle & orbit animations, and native bilingual (Persian RTL with Yekan Bakh / English LTR) typography.
  Use when the user asks to create, design, generate, or beautify PowerPoint presentations (.pptx),
  use a custom .pptx template, turn text/notes into slides, or mentions "پاورپوینت", "اسلاید", "presentation", "PPT", or "PPT_Saz".
---

# اسکیل ساخت خودکار و نیتیو پاورپوینت (`PPT_Saz v5.0` — Next-Gen Infographic & Custom Template Studio)

این اسکیل بر پایه یافته‌های مقالات علمی روز (**PPTAgent** در EMNLP، **AutoPresent** در CVPR و **DOC2PPT** در AAAI) برای تولید ارائه‌های فوق‌حرفه‌ای، مجهز به **۶ معماری بصری کاملاً متمایز**، **۱۸ ساختار دیاگرام و اینفوگرافیک متنوع**، **کارگردان هوشمند ضدتکرار چیدمان**، **قابلیت پذیرش تمپلیت `.pptx` اختصاصی کاربر (Hybrid Custom Template Ingestion)** و **انیمیشن‌های ممتد بدون توقف با ترنزیشن تک‌کلیک Morph** طراحی شده است.

---

## 🎨 ۶ کهن‌الگوی آرت‌استایل و ۱۲ تم رنگی اختصاصی

| # | کهن‌الگو (Art-Style) | تم روشن (Light) | تم تیره (Dark) | معماری فضایی و هندسی منحصربه‌فرد |
|---|---|---|---|---|
| **۱** | **Apple Bento-Grid** | `bento_glass_light` | `bento_glass_dark` | موزاییک نامتقارن (۱ کارت بزرگ Hero + ۲ مینی‌کارت)، شیشه‌ای نرم (`rx=28-32`) و اورب‌های نوری |
| **۲** | **Swiss Academic** | `swiss_academic_light` | `swiss_academic_dark` | گرید علمی میکرومتری، خط لوله چورون مرحله‌ای، جدول کارآزمایی بالینی با `[95% CI]` |
| **۳** | **Neo-Brutalist Pop** | `neo_brutalist_light` | `neo_brutalist_dark` | بلوک‌های ضخیم با بردر ۳.۵px مشکی، سایه سخت ۱۰px آفست مشکی، استیکرهای چرخیده و ستاره انفجاری VS |
| **۴** | **Warm Editorial** | `warm_editorial_light` | `warm_editorial_dark` | قاب‌های قوسی پنجره کلیسایی (`Arched Windows`)، اعداد واتر‌مارک سایز ۱۹۰ کمرنگ، امواج ارگانیک |
| **۵** | **Royal Gold Noir** | `royal_gold_light` | `royal_gold_dark` | پدستال‌های هشت‌ضلعی گوشه‌بریده (`Beveled Octagons`)، خطوط دوبل طلای ۲۴ عیار و مدال‌های الماسی `◆` |
| **۶** | **Cyber HUD** | `cyber_light` | `cyber_aurora` | کنسول‌های تله‌متری چمفر ۴۵ درجه، رینگ‌های راداری چرخان، گیج‌های کالیبراسیون و ذرات کهکشانی |

---

## 🧩 ۱۸ ساختار چیدمان، دیاگرام اینفوگرافیک، چارت و جدول (`layout: "auto"`)

کارگردان هوشمند معنایی ([`scripts/semantic_layout_director.py`](file:///g:/دانشگاه/اسکیل%20تولید%20پاورپوینت/scripts/semantic_layout_director.py)) بر اساس معنای متن هر اسلاید و با رعایت **قانون اکید عدم تکرار چیدمان در دو اسلاید متوالی**، به صورت ۱۰۰٪ خودکار بهترین ساختار را از بین ۱۸ الگوی زیر انتخاب می‌کند:

1. `title_hero` — کاور سینماتیک با برچسب کپسولی موضوع (`kicker`)، عنوان اصلی، زیرعنوان و قاب تصویر.
2. `content_cards` — ستون‌ها و کارت‌های اختصاصی هر آرکتایپ (موزاییک بنتو / پدستال سلطنتی / طاق ژورنالی / کارت پاپ).
3. `process_steps` — فرآیند گام‌به‌گام افقی متناسب با معماری هر تم.
4. `stats_kpi` — شاخص‌های کلیدی عملکرد و اعداد آماری درشت به همراه برچسب ترند.
5. `comparison` — مقایسه دو رویکرد متضاد با نشان مرکزی `VS`.
6. `circular_orbit` — هسته مرکزی خورشیدی با پادهای دایره‌ای مداری معلق در اطراف.
7. `split_image` — چیدمان دوتکه متنی آیکون‌دار در یک سو و قاب تصویر در سوی دیگر.
8. `pyramid_hierarchy` — **هرم سلسله‌مراتبی ۳ تا ۴ لایه** با هاله چرخان قله و کارت‌های توضیحی متصل.
9. `funnel_pipeline` — **قیف پالایش و غربالگری مرحله‌ای** با حلقه ورودی چرخان و جزئیات هر فاز.
10. `venn_synergy` — **دیاگرام ون (۳ دایره متقاطع شفاف)** برای نمایش هم‌پوشانی و هم‌افزایی مفاهیم.
11. `quadrant_matrix_2x2` — **ماتریس ۴ خانه‌ای استراتژیک (SWOT / 2x2)** با قطب‌نمای چرخان مرکزی.
12. `snake_roadmap` — **نقشه راه موجی و زیگزاگ (S-Curve Serpentine)** با نودهای چرخان.
13. `mind_map_hub` — **نقشه ذهنی شعاعی (Mind-Map)** با هسته مرکزی و شاخه‌های منحنی بزیه.
14. `fishbone_cause_effect` — **دیاگرام استخوان ماهی (Ishikawa)** برای ریشه‌یابی علل و معلول‌ها.
15. `data_chart_showcase` — **نمودار برداری راداری / عنکبوتی (Native Vector Radar Chart)** با رنگ‌بندی خودکار تم و کارت‌های تحلیلی.
16. `smart_table_matrix` — **جدول ماتریسی چندستونه هوشمند** با هدر رنگی و بج وضعیت.
17. `hero_callout_quote` — **اسلاید بیانیه / نقل‌قول کلیدی برجسته** با هاله چرخان پس‌زمینه.
18. `closing_thankyou` — **اسلاید پایانی و جمع‌بندی باشکوه** با مدال چرخان افتخار و خلاصه دستاوردها.

---

## 📂 قابلیت ورود تمپلیت پاورپوینت اختصاصی کاربر (`--template-pptx`)

اگر کاربر یک فایل `.pptx` اختصاصی ارائه دهد، موتور [`scripts/custom_template_ingestor.py`](file:///g:/دانشگاه/اسکیل%20تولید%20پاورپوینت/scripts/custom_template_ingestor.py) به صورت **ترکیبی هوشمند (Hybrid Smart Mode)** عمل می‌کند:
1. **استخراج DNA بصری (`extract_pptx_brand_dna`):** رنگ‌های اصلی، پس‌زمینه، کنتراست تیره/روشن و فونت‌های فایل `.pptx` کاربر را از XML استخراج می‌کند.
2. **شکار آیکون‌ها و اشکال برداری (`harvested_icons`):** تمام مسیرهای وکتور، آیکون‌ها و تصاویر داخل فایل پاورپوینت کاربر را استخراج می‌کند.
3. **کلونینگ اسلاید + تولید دیاگرام‌های جدید:** هم می‌تواند اسلایدهای خود تمپلیت را با حفظ گرافیک کپی و با متن جدید پر کند (`clone_template_slide`) و هم برای اسلایدهایی که نیاز به دیاگرام جدید (هرم، قیف، ون، نقشه راه، نمودار) دارند، دیاگرام‌ها را با رنگ، پس‌زمینه و آیکون‌های همان فایل `.pptx` می‌سازد و ترنزیشن تک‌کلیک `Morph` و انیمیشن‌های چرخان ممتد را روی آن اعمال می‌کند!

---

## 🎯 گردش کار اجرایی هوش مصنوعی (Step-by-Step AI Workflow)

1. **گیت انتخاب سبک (Grill-Me Style Gate):** اگر کاربر فایل `.pptx` نداده بود، جدول ۶ سبک را با `ask_question` بپرسید. اگر فایل `.pptx` داده بود، آن را با `--template-pptx` به ژنراتور بدهید.
2. **قفل کامل متن (Strict Verbatim Text Gate):** تیترها و متن‌های کاربر را بدون تغییر حتی یک کلمه در ساختار JSON قرار دهید (می‌توانید `"layout": "auto"` بگذارید تا کارگردان هوشمند معنایی بهترین دیاگرام ضدتکرار را انتخاب کند).
3. **اجرای دستور کامپایل:**

```powershell
# حالت ۱: استفاده از ۶ سبک و ۱۸ دیاگرام داخلی
& "C:\Users\Hill\.local\bin\uv.exe" run --with python-pptx --with lxml python scripts/presentation_generator.py deck.json -p project_run -o output_deck.pptx --theme <theme_key> -t morph -a auto

# حالت ۲: ساخت پاورپوینت با استفاده از فایل تمپلیت اختصاصی کاربر (.pptx)
& "C:\Users\Hill\.local\bin\uv.exe" run --with python-pptx --with lxml python scripts/presentation_generator.py deck.json -p project_run -o output_deck.pptx --template-pptx "path/to/user_template.pptx" -t morph -a auto
```

