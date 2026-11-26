# استاندارد پیشگیری از خطاهای Fatal

> منبع: FIX-1.1.1-FA.md رامَن، `functions.php` سعدی، الگوهای ۸ قالب واقعی
> (`knowledge/real-themes-survey.md` §3).
> **مالک:** `SAGE` (پیاده‌سازی) · `WP` (بخش‌های ادمین) · **دروازه‌ی نهایی: `QA` با `scripts/validate_theme.py`**.

---

## ۱) علل رایج Fatal در خروجی تیم و درمان آن‌ها

| # | علت Fatal | الگوی درست (دیده‌شده در قالب‌های واقعی) |
|---|---|---|
| ۱ | **syntax error** (کپی ناقص، بلاک باز نبسته) | `php -l` روی **همه** فایل‌ها قبل از تحویل — دروازه‌ی اجباری. اگر PHP در دسترس نباشد، `validate_theme.py` بررسی جایگزین تعادل ساختاری را اجرا می‌کند و QA موظف است lint کامل را روی میزبان دارای PHP تکرار کند |
| ۲ | **آپلود/بیلد ناقص** → `require` فایل ناموجود | قبل از هر require استاتیک: `is_file()` → اعلان فارسی → `return` (سعدی) |
| ۳ | **PHP قدیمی‌تر از نسخه‌ی هدف** → `match/enum/readonly/typed properties` ناشناخته | گارد نسخه در بالای `functions.php`: `version_compare(PHP_VERSION, '8.1', '<')` → `admin_notices` → `return` (سعدی با 8.3) |
| ۴ | **بازتعریف تابع/کلاس** (دو بار require، برخورد پیشوند) | فقط `require_once`؛ همه‌ی توابع/کلاس‌ها در فضای نام اختصاصی (`Theme\` یا پیشوند `{slug}_`)؛ کمک‌تابع‌ها هم پیشوند دارند |
| ۵ | **کد وابسته به افزونه بدون گارد** (`extends WooCommerce_*`) | `if (class_exists('WooCommerce')) { require_once ... }` (سایانا) — یا `class_exists` قبل از ارث |
| ۶ | **فراخوانی تابع WP در لودِ فایل** (خارج از هوک، قبل از `after_setup_theme`) | فقط تعریف + هوک‌گذاری در لود؛ اجرا داخل هوک؛ `defined('ABSPATH')||exit` در همه‌ی فایل‌ها |
| ۷ | **نبود `vendor/autoload` یا فایل موتور** بعد از انتقال دستی | چک `is_file` + اعلان «قالب کامل نصب نشده» + `return` — سایت سفید **نمی‌شود**؛ پنل پیام می‌دهد |
| ۸ | **کش کهنه‌ی Blade/کامپایل‌شده** بعد از جایگزینی ZIP | پاک‌سازی کش با **شماره نسخه** در اولین ورود ادمین بعد از بروزرسانی + هنگام ذخیره‌ی تنظیمات (رامَن FIX) |
| ۹ | **نبود اکستنشن `dom`/`libxml`** → پنل بی‌صدا می‌شکند | پردازشگر جایگزین portable بدون DOM + هشدار «کش فعال است، نسخهٔ DOM نیست» (رامَن) |
| ۱۰ | **کامپایل نشدن فایل‌های نو** (تغییرات فقط در پیش‌نویس) | هشدار فایل‌های بدون خط کامپایل (`get_incomplete_files`) — رامَن |

---

## ۲) الگوی اجباری بالای `functions.php`

```php
<?php
/**
 * {Brand} نوین — bootstrap.
 * فقط require_once؛ هیچ هوک/کلاس/تابعی اینجا اجرا نمی‌شود.
 */

if (! defined('ABSPATH')) { exit; }   // دفاع از دسترسی مستقیم

// ۱) گارد نسخه PHP (قبل از هر چیز)
if (version_compare(PHP_VERSION, '8.1', '<')) {
    add_action('admin_notices', function () {
        echo '<div class="notice notice-error"><p><b>{Brand} نوین:</b> '
            . 'این قالب به PHP 8.1 یا بالاتر نیاز دارد — نسخهٔ فعلی: '
            . esc_html(PHP_VERSION) . '</p></div>';
    });
    return;   // ← return، نه exit و نه fatal
}

// ۲) گارد فایل‌های حیاتی (بیلد ناقص را تبدیل به اعلان می‌کند)
foreach ([
    get_template_directory() . '/inc/functions.php',
    // ... بقیه‌ی requireهای سطح بالا
] as $__f) {
    if (! is_file($__f)) {
        add_action('admin_notices', function () {
            echo '<div class="notice notice-error"><p>فایل‌های قالب کامل نیستند؛ '
                . 'لطفاً قالب را دوباره آپلود و استخراج کنید.</p></div>';
        });
        return;
    }
}

// ۳) require_onceهای ترتیبی (یا include_once درون حلقه، هرگز require بدون once)
require_once get_template_directory() . '/inc/functions.php';
// ...
```

**قوانین:**
- `functions.php` فقط bootstrap است: گاردها + `require_once`. هیچ `add_action` اضافه، کلاس، یا منطقی نباید داشته باشد.
- هر فایل PHP: `defined('ABSPATH') || exit;` در خطوط اول (حتی فایل‌هایی که فقط از طریق هوک لود می‌شوند).
- **هرگز** `require` بدون `_once`.
- هرگز در لودِ فایل، تابع WP صدا زده نشود (`esc_html__`، `get_option` و…) — فقط داخل هوک/تابع.

---

## ۳) گاردهای وابستگی

```php
// ووکامرس (الگوی سایانا)
if (class_exists('WooCommerce')) {
    require_once __DIR__ . '/wc-compat.php';
}

// موتور/کش (الگوی سعدی — متفاوت با فلسفهٔ بدون Composer ولی الگوی گارد یکی است)
if (is_file(__DIR__ . '/Engine/autoload.php')) {
    require_once __DIR__ . '/Engine/autoload.php';
} else {
    add_action('admin_notices', fn() => echo '<div class="notice notice-error"><p>موتور قالب یافت نشد.</p></div>');
    return;
}
```

---

## ۴) کش کامپایل (نسخه‌محور، نه زمان‌محور)

**درس بحرانی رامَن:** بعد از آپلود ZIP جدید، ممکن است `mtime` فایل‌های قالب **قدیمی‌تر** از کش کامپایل‌شده باشد → کش کهنه به اجرا درمی‌آید → «تنظیمات اعمال نشد» یا خطای کلاس ناموجود.

- کلید کش شامل **نسخه‌ی قالب** باشد: `theme_view_cache_{slug}_{VERSION}`.
- در اولین ورود ادمین **بعد از بروزرسانی نسخه**، کش ویو یک‌بار پاک شود.
- هنگام ذخیره‌ی تنظیمات: پاک‌سازی کش ویو + کش افزونه‌ها (WP Rocket/W3TC/WP Super Cache/LiteSpeed) — `theme-settings-standard.md` §8.
- فایل‌های کامپایل‌شده‌ی ناقص (`get_incomplete_files`) را قبل از نمایش ادمین پاک کن.

---

## ۵) دروازه‌ی QA — `scripts/validate_theme.py`

اجرای اجباری قبل از PASS:

```bash
python3 scripts/validate_theme.py release/{slug}/
```

بررسی‌ها:
1. `php -l` روی **همه** فایل‌های `.php` (صفر خطای syntax). نبودِ PHP = هشدار صریح + اجرای
   بررسی جایگزین تعادل ساختاری توسط اسکریپت؛ QA موظف است lint کامل را روی میزبان دارای PHP تکرار کند.
2. وجود `style.css` + `index.php` + `functions.php`؛ نام پوشه == `Text Domain` در style.css.
3. وجود `inc/settings/` (یا `app/Settings/`) با schema + صفحه‌ی پنل.
4. همه‌ی مسیرهای `require_once __DIR__/...` استاتیک — فایل‌شان موجود است.
5. `defined('ABSPATH')` در بالای **هر** فایل PHP.
6. **تکراری نبودن** نام توابع/کلاس‌های سراسری بین فایل‌ها (علت شماره‌ی ۴ جدول).
7. ممنوعیت‌ها: `composer.json`/`vendor/` نباشد؛ `require(` بدون `_once` (هشدار)؛ هوک در `functions.php` (FAIL).
8. `patches/` در صورت وجود: پوشه‌ی نسخه + `manifest.json` با `sha256` برای همه‌ی فایل‌ها.

خروجی سبز = تازه فقط دروازه‌ی مرحلهٔ ۱۳ است؛ **اجرای وبسایت** و تست ذخیره‌ی پنل هم باید انجام شود.

---

## ۶) دستورالعمل واکنش هنگام دیدن Fatal (برای `WP`/`QA`)

1. پیام کامل خطا + فایل + خط را بخوان (debug.log / نمایش خطا).
2. `php -l` روی فایل خطا → اگر syntax باشد، بلافاصله اصلاح.
3. اگر «کلاس/تابع ناموجود» است → جست‌وجوی require بدون گارد یا کش کهنه (بخش ۴).
4. اگر «فایل ناموجود» است → فهرست requireها را با `is_file` گارد بزن.
5. بعد از هر اصلاح: `validate_theme.py` + ذخیره‌ی مجدد در پنل واقعی + پاک‌سازی کش + ریلود سایت.
6. علت ریشه‌ای را در `release/{slug}/docs/` ثبت کن تا پچ ترمیمی خورده شود.
