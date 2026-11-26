# پایگاه دانش: تحلیل ساختار قالب‌های واقعی آمل نوین

> **تاریخ تحلیل:** ۲۶ نوامبر ۲۰۲۶ · **روش:** دانلود بسته‌های نسخه‌ی نهایی هر قالب و بررسی کد
> **نکته:** ریپوهای گیت‌هاب خصوصی‌اند؛ نسخه‌های ZIP از گوگل درایو تیم تحلیل شد.
> **کاربرد:** مرجع رسمی برای `standards/theme-settings-standard.md` و `standards/fatal-error-prevention.md`.

---

## ۱) فهرست قالب‌های تحلیل‌شده (۸ قالب واقعی)

| # | قالب | نسخه | معماری | پنل تنظیمات |
|---|------|------|--------|-------------|
| ۱ | بابای عینک (`babaye-einak`) | 1.3.45 | کلاسیک + `inc/` | `inc/settings.php` (۲۱۰۳ خط) + `inc/patch-updater.php` |
| ۲ | چوبین دکور (`chobin-decor`) | 1.3.3 | کلاسیک + `inc/` | `inc/patcher.php` |
| ۳ | غوغه (`ghoveh`) | — | Sage با Composer (`app/`, `resources/`) | `tools/make-patch.php` |
| ۴ | پرستار (`parastar`) | 1.0.6 | کلاسیک + `inc/` | `inc/settings-schema.php` + `inc/admin-settings.php` + `inc/customizer.php` |
| ۵ | رامَن انرژی (`raman-energy-sage`) | 1.2.0 | Sage + Composer + کش `app/settings-cache.php` | `app/options.php` (۳۰۵ خط) + `SETTINGS-FA.md` |
| ۶ | رنگ صادقی (`rangesadeghi`) | 2.2.20 | **Sage بدون Composer** (`bootstrap/app.php` + `autoload.php` سفارشی) | `app/Core/Options.php` + `resources/views/admin/settings.blade.php` |
| ۷ | سعدی (`saadi-sage`) | 2.1.7 | Sage/Acorn رسمی + `vendor/` | `app/settings.php` + `app/patch.php` |
| ۸ | سایانا (`sayana`) | 2.1.12 | کلاسیک + `inc/` | `inc/theme-options.php` (۲۱۳۰ خط) + `inc/settings-backup.php` + `inc/theme-updater.php` |

**نکته‌ی کلیدی:** `rangesadeghi` دقیقاً همان فلسفه‌ی تیم ماست — «معماری مدرن Roots Sage (بدون نیاز به Composer)» — و بهترین مرجع داخلی برای موتور و پنل ماست.

---

## ۲) الگوی مشترک پنل تنظیمات (۸ از ۸ قالب)

### الف) ذخیره‌سازی: **یک option با یک کلید** (نه ده‌ها option)
```php
const OPTION_KEY = 'raman_theme_options';   // رامَن
public const OPTION_KEY = 'rangesadeghi_theme_options';  // رنگ صادقی
// خواندن: get_option(OPTION_KEY, []) → آرایه‌ی واحد + ادغام recursive با defaults
```

### ب) **Schema به‌عنوان تنها منبع حقیقت** (Single Source of Truth)
```php
// رامَن: key => [tab, type, label, default, min?, max?]
'header_sticky' => ['header', 'checkbox', 'هدر چسبان هنگام اسکرول', 1],
'color_yellow'  => ['brand',  'color',    'رنگ اصلی / زرد',      '#ffcb04'],

// پرستار: section => ['title'=>..., 'fields'=> id => [type, default, label, desc?]]
// سعدی:  tab    => key => [label, type]
```
- لیبل‌ها، تایپ‌ها، پیش‌فرض‌ها و تب‌ها **همه** از schema می‌آیند؛ هیچ فیلدی خارج از آن نیست.
- sanitize، رندر فیلد، و پیش‌فرض‌ها از **یک** آرایه مشتق می‌شوند.

### ج) تایپ‌های فیلد و پاک‌سازی (جدول مشترک)
| تایپ | sanitize هنگام ذخیره | خروجی |
|---|---|---|
| `checkbox` | `=== '1' ? 1 : 0` | `bool` |
| `number` | `(int)` + `min/max clamp` | عدد |
| `text/textarea` | `sanitize_text_field` / `sanitize_textarea_field` | escape هنگام خروج |
| `url` | `esc_url_raw` با allow-list پروتکل (`http/https/tel/mailto`) | `esc_url` |
| `email` | `sanitize_email` | `esc_html` |
| `phone` | تبدیل رقم فارسی/عربی→لاتین + حذف غیرعدد | `esc_attr` |
| `color` | `sanitize_hex_color` | متغیر CSS |
| `media` | `absint` + `wp_attachment_is_image` | `wp_get_attachment_image` |
| `page` | `absint` + نوع برگه | `get_permalink` |
| `footer_html` | `wp_kses` allow-list (`b,strong,br,a`) + `WP_HTML_Tag_Processor` برای `rel=noopener` | همان |
| `rich_title` | `wp_kses` فقط `br/em/strong` | همان |
| `shortcode` | `sanitize_text_field` | `do_shortcode` فقط برای ادمین؟ خیر — با تأیید |
| **همیشه** | **sanitize هنگام ذخیره + escape/_kses هنگام خروج** (برای مقادیر قدیمی ذخیره‌شده) | |

### د) صفحه‌ی ادمین
- `add_menu_page` + `add_theme_page` با `manage_options`، آیکون `dashicons`، جایگاه ~۵۹-۶۱.
- تب‌های فارسی با `dir="rtl"`، `role="tablist/tab/tabpanel"`، `aria-selected`، کلید جهت/Home/End.
- **یک فرم** به `options.php` با `settings_fields()` (Settings API — nonce داخلی) یا `admin_post` با `wp_nonce_field` — هر دو دیده شده؛ **استاندارد تیم: Settings API**.
- savebar ثابت زیر فرم؛ هشدار خروج با تغییر ذخیره‌نشده؛ نمایش نسخه‌ی قالب و آخرین ذخیره.
- دارایی‌ها فقط در صفحه‌ی پنل: `wp_enqueue_media` + `wp-color-picker` + `admin.css/js` با نسخه.
- **خالی گذاشتن فیلد = استفاده از محتوای فعلی برگه/پیش‌فرض** — هرگز «خالی = حذف محتوا».

### هـ) بازنشانی و پشتیبان
- **بازگردانی پیش‌فرض‌ها:** فقط option خود پنل حذف/بازنویسی می‌شود؛ `wp_nonce` + چک‌باکس `confirm` صریح؛ محتوا/رسانه/منو دست‌نخورده.
- **برون‌ریزی/درون‌ریزی JSON** (رنگ صادقی): پاکت با `format` + `format_version` + `theme_version`؛ اعتبارسنجی شکل آرایه قبل از نوشتن؛ **درون‌ریزی فقط با `unfiltered_html`**؛ محدودیت حجم (۲MB).

### و) کش هنگام ذخیره (درس FIX-1.1.1 رامَن)
1. پاک‌سازی **کش Blade/ویوی قالب** — با **شماره نسخه**، نه فقط `mtime` (mtime فایل ZIP قدیمی‌تر از کش → کش کهنه می‌ماند!).
2. درخواست پاک‌سازی کش افزونه‌ها: WP Rocket، W3 Total Cache، WP Super Cache، Cache Enabler، رویداد LiteSpeed.
3. دکمه‌ی «پاک‌سازی کش قالب» در پنل + نمایش آخرین زمان پاک‌سازی.
4. کش سرور/CDN از داخل وردپرس قابل پاک‌سازی نیست — پیام راهنما در پنل.

### ز) بخش «بروزرسانی با پچ» داخل خود پنل (۸ از ۸)
- همه‌ی قالب‌ها patch updater دارند: `inc/patch-updater.php`، `app/patch.php`، `app/Updater/`، `inc/theme-updater.php`، `inc/patcher.php`، `tools/make-patch.py`.
- الگوی سایانا (کامل‌ترین): ZIP پچ شامل `sayana-patch.json` + فایل‌های تغییریافته؛ **staging در `uploads/{theme}-patches/`**؛ سقف حجم (۲۰MB) و تعداد فایل (۴۰۰)؛ **پشتیبان قبل از apply + لاگ + rollback** از همان صفحه.
- پچ‌های واقعی در درایو: `baba-theme-patch-1.3.44-to-1.3.45.zip` + `.sha256`، `saadi-sage-patch-2.1.10-to-2.1.11.zip`، `rangesadeghi-patch-2.2.20.zip`، `chobin-patch-repair.zip` (پچ ترمیمی!).

---

## ۳) درس‌های خطای Fatal (از FIX-1.1.1-FA.md و functions.php ها)

| درس | الگوی درست (دیده‌شده در قالب‌های واقعی) |
|---|---|
| PHP قدیمی → fatal روی `match`/`enum`/`readonly` | **گارد نسخه PHP** در بالای `functions.php`: `version_compare` → `admin_notices` + `return` (نه exit، نه fatal) — سعدی |
| آپلود ناقص → `require` فایل ناموجود → **fatal** | **`is_file()` قبل از هر require** → notice فارسی «فایل‌های قالب کامل نیستند» + `return` — سعدی |
| نبود `vendor/autoload` → fatal | چک `is_file($autoload)` → notice + `return` — سعدی/رامَن |
| نبود `DOMDocument` در سرور → بی‌صدای از کار افتادن تنظیمات | **پردازشگر جایگزین portable** بدون DOM — رامَن |
| کش Blade کهنه بعد از جایگزینی فایل‌ها | پاک‌سازی کش با **شماره نسخه** هنگام اولین ورود ادمین بعد از بروزرسانی — رامَن |
| فعال نبودن ووکامرس → fatal روی `class extends Woo...` | `if ( class_exists('WooCommerce') ) { require_once ... }` — سایانا |
| تداخل تابع/کلاس سراسری (دو بار require) | `require_once` + فضای نام/پیشوند اختصاصی هر تابع (`raman_*`، `parastar_*`، `sayana_*`) |
| خطای syntax → سفید شدن کامل سایت | `php -l` روی همه‌ی فایل‌ها قبل از تحویل (دروازه‌ی جدید تیم) |

---

## ۴) نگاشت الگوها به ایجنت‌های تیم

| الگو | ایجنت مسئول | استاندارد |
|---|---|---|
| Schema + پنل + Settings API + بازنشانی/درون‌ریزی | `WP` | `theme-settings-standard.md` |
| موتور بدون Composer (`bootstrap/autoload` سفارشی مثل رنگ صادقی) | `SAGE` | `sage11-structure.md` §2-b |
| Patch updater با staging/پشتیبان/rollback | `PLUG` | `theme-settings-standard.md` §پچ |
| کش‌زدایی هنگام ذخیره (Blade + افزونه‌ها) | `WP` + `PERF` | `theme-settings-standard.md` §کش |
| گاردهای fatal (نسخه PHP، is_file، class_exists) | `SAGE` (ساخت) + `QA` (دروازه) | `fatal-error-prevention.md` + `scripts/validate_theme.py` |
| خالی=پیش‌فرض/محتوای فعلی، فارسیسازی، عدد فارسی | `CONV` + `UXR` | همین سند |
