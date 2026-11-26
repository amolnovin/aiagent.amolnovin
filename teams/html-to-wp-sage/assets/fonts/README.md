# فونت IranSans (Web + FaNum) — فونت رسمی قالب‌های این تیم

این فونت **اجباری** برای همه‌ی قالب‌های ساخته‌شده توسط تیم `html-to-wp-sage` است.

## منبع

- **دانلود از گوگل درایو:** [IRANSans(FaNum).zip](https://drive.google.com/file/d/1cQ2MIU0TAorvxxEYVjrTsFK2H6SHiyE3/view?usp=sharing)
- نسخه‌ی استخراج‌شده در همین پوشه (نسخه‌ی مرجع ZIP در همان لینک بالا).

## محتوا

6 وزن × 4 فرمت (eot / ttf / woff / **woff2**) — با پشتیبانی **اعداد فارسی (FaNum)**:

| فایل | وزن |
|---|---|
| `IRANSansWeb(FaNum)_UltraLight` | ۱۰۰ (UltraLight) |
| `IRANSansWeb(FaNum)_Light` | ۳۰۰ (Light) |
| `IRANSansWeb(FaNum)` | ۴۰۰ (Regular) |
| `IRANSansWeb(FaNum)_Medium` | ۵۰۰ (Medium) |
| `IRANSansWeb(FaNum)_Bold` | ۷۰۰ (Bold) |
| `IRANSansWeb(FaNum)_Black` | ۹۰۰ (Black) |

## استفاده در قالب

1. پوشه‌ی `iransans/` را در `assets/fonts/` قالب کپی کن.
2. `@font-face` را در `resources/styles/` با `font-display: swap` ثبت کن (نمونه‌ی کامل در `standards/sage11-structure.md` §فونت).
3. در `tokens.css`:
   ```css
   :root { --font-sans: 'IRANSans', system-ui, sans-serif; }
   ```
4. وزن‌های غیراستفاده را از لیست `@font-face` حذف کن (بودجه‌ی فونت ≤ ۱۰۰KB پس از subset).

## قواعد

- اولویت فرمت: `woff2` → `woff` → `ttf` → `eot` (فقط fallback مرورگرهای قدیمی).
- حتماً `font-display: swap` و `preload` زیرمجموعه‌ی فارسی (هم‌کاری با `MEDIA` و `PERF`).
- اعداد فارسی در متن فارسی با همین نسخه‌ی FaNum نمایش داده می‌شوند.
