# راه‌انداز سریع — تیم تبدیل HTML به قالب وردپرس Sage (بدون Composer)

۱۰ ایجنت، یک خط تولید: از فایل‌های HTML تا قالب وردپرس استاندارد با Performance ≥ ۹۰ و سئوی حرفه‌ای.

---

## ۱) در همین چت

کافی است بریف یا فایل‌های HTML را بدهید:

> «این ۶ فایل HTML را برای حوزه‌ی پزشکی (نوبت‌دهی) به قالب وردپرس Sage 11 بدون Composer تبدیل کنید؛ RTL، ریسپانسیو، Lighthouse بالای ۹۰ و سئوی محلی حرفه‌ای لازم دارم.»

یا با دستورات سریع:

| دستور | نتیجه |
|-------|-------|
| `/all <توضیح>` | کل ۱۰ ایجنت به‌ترتیب مراحل `TEAM.md` را اجرا می‌کنند |
| `/brief` | فقط `TL` بریف را می‌گیرد و Decision Log می‌سازد |
| `/arch <لینک/فایل HTML>` | ممیزی + قرارداد تبدیل |
| `/blade` | ساخت اسکلت بدون-Composer (`SAGE`) |
| `/convert` | تبدیل بخش‌ها به Blade (`CONV`) |
| `/css` | توکن‌ها + ریسپانسیو + RTL (`CSS`) |
| `/js` | کامپوننت‌ها + Vite/no-build (`JS`) |
| `/wp` | هوک‌ها، enqueue، امنیت (`WP`) |
| `/seo` | متا + Schema حوزه (`SEO`) |
| `/perf` | بنچمارک و بهینه‌سازی ≥ ۹۰ (`PERF`) |
| `/qa` | تست، باگ، دروازه‌ی انتشار (`QA`) |
| `/ship` | بسته‌ی نهایی + docs + استاندارد حوزه |
| `/review <فایل یا لینک>` | ۱۰ دیدگاه روی یک خروجی |

---

## ۲) در Claude / ChatGPT / Gemini / Cursor

1. فایل‌های `agents/*.md` هر ایجنت را باز کنید.
2. بخش **System Prompt (کپی‌شدنی)** همان ایجنت را به‌عنوان System Prompt / Custom Instruction پنجره‌ی چت آن ایجنت بگذارید (یک چت برای هر کدام، یا یک چت با همه‌ی پرامپت‌ها).
3. `TEAM.md` و `standards/*` را هم به کانتکست اضافه کنید تا قواعد مشترک بماند.
4. بریف را از `templates/PROJECT_BRIEF.md` پر کنید و بفرستید.

---

## ۳) مثال سناریوی کامل

```
TL    → بریف: قالب «رستوران سنتی»، ۵ صفحه HTML، فارسی RTL
ARCH  → ممیزی + قرارداد: hero، منوی غذا (CPT)، گالری، رزرو، تماس
SAGE  → اسکلت: bootstrap + مینی-Blade + config + routes (بدون composer)
CONV  → viewهای pages/* + components/menu-item + forms/booking
CSS   → tokens + menu grid + RTL + ۳۶۰/۷۶۸/۱۴۴۰
JS    → nav drawer + lightbox سبک + Vite build + fallback
WP    → CPT منوی غذا، enqueue هش‌دار، nonce رزرو، theme.json
SEO   → Restaurant + Menu + LocalBusiness + متاها
PERF  → preload فونت، WebP، critical CSS → موبایل ۹۵
QA    → ماتریس کامل + رگرسیون با منبع → PASS
SHIP  → بسته + docs/01..06 + «استاندارد حوزه رستوران»
```

---

## ۴) قوانین کوتاه تیم

1. بدون قرارداد `ARCH`، کدی نوشته نمی‌شود.
2. بدون Composer / vendor — فقط آپلود پوشه‌ی قالب.
3. Performance ≥ ۹۰ و سئوی حرفه‌ای خط قرمز است.
4. RTL-first، دسترس‌پذیری WCAG 2.2 AA، امنیت nonce+escape.
5. هر تحویل با سربرگ Handoff و چک‌لیست تمام می‌شود.
6. فقط `QA` با PASS اجازه‌ی SHIP می‌دهد.

---

*نسخه ۱.۰ — تیم ۱۰ نفره‌ی `html-to-wp-sage`*
