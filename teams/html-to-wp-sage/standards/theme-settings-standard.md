# استاندارد پنل تنظیمات قالب (Theme Settings)

> استخراج‌شده از تحلیل ۸ قالب واقعی آمل نوین (مراجعه: `knowledge/real-themes-survey.md`).
> **مالک اجرا: `WP`** · پشتیبان: `PLUG` (پچ/درون‌ریزی) · بازبینی: `QA` و `ARCH`.
> این سند **مکمل** `sage11-structure.md` §2-c است و در صورت تعارض، حرف اول را می‌زند.

---

## ۱) قوانین طلایی (بدون استثنا)

1. **یک option با یک کلید** — همه‌ی تنظیمات در یک آرایه‌ی واحد:
   ```php
   const SETTINGS_KEY = '{slug}_theme_options';  // مثلا sayana_novin_theme_options
   $all = get_option(SETTINGS_KEY, []);          // همیشه با defaults ادغام recursive
   ```
2. **Schema = تنها منبع حقیقت** — برچسب، تایپ، پیش‌فرض، تب و محدوده‌ی عددی همه از schema می‌آیند؛ sanitize و رندر فیلد هم از همان آرایه مشتق می‌شوند.
3. **sanitize هنگام ذخیره + escape هنگام خروج** — هر دو اجباری (مقادیر قدیمی ذخیره‌شده هم باید امن بمانند).
4. **خالی = پیش‌فرض/محتوای فعلی** — خالی گذاشتن فیلد هرگز به معنای حذف محتوا نیست.
5. **`manage_options` + nonce + confirm** روی هر عملیات ذخیره/بازنشانی/درون‌ریزی.
6. **پاک‌سازی کش با شماره نسخه** بعد از ذخیره (نه فقط mtime).
7. فارسی و RTL در کل پنل؛ `dir="rtl"` روی ریشه‌ی پنل.

---

## ۲) ساختار فایل‌ها

```
inc/settings/                      ← یا app/Settings/ در معماری Sage-شکل
├── schema.php                     ← {slug}_settings_schema(): array (تنها منبع حقیقت)
├── sanitize.php                   ← {slug}_sanitize_settings($input): array (سوییچ تایپ‌به‌تایپ)
├── page.php                       ← رندر صفحه‌ی پنل (تب‌ها، savebar، پچ)
├── fields.php                     ← رندر تک‌تک فیلدها از روی schema
└── io.php                         ← برون‌ریزی/درون‌ریزی JSON (اختیاری اما توصیه‌شده)
resources/styles/admin-settings.css   ← فقط در صفحه‌ی پنل enqueue می‌شود
resources/scripts/admin-settings.js   ← تب‌ها، media picker، هشدار خروج
```

---

## ۳) Schema — قالب استاندارد

```php
function {slug}_settings_schema(): array {
    return [
        // فیلد => [ تب, تایپ, برچسب فارسی, پیش‌فرض, (min, max برای number) ]
        'header_sticky'   => ['header', 'checkbox', 'هدر چسبان هنگام اسکرول', 1],
        'header_cta_text' => ['header', 'text',     'متن دکمه هدر', 'مشاوره رایگان'],
        'footer_copyright'=> ['footer', 'text',     'متن کپی‌رایت', '© ۲۰۲۶ {brand} نوین'],
        'home_hero_image' => ['pages',  'media',    'تصویر هیرو', 0],
        'shop_columns'    => ['store',  'number',   'تعداد ستون محصولات', 4, 2, 6],
        'seo_description' => ['seo',    'textarea', 'توضیح پیش‌فرض سایت', ''],
        'perf_defer_js'   => ['perf',   'checkbox', 'بارگذاری غیرمسدودکننده JS قالب', 1],
    ];
}
```

### تایپ‌ها و sanitize (سوییچ اجباری)
| تایپ | sanitize | یادداشت |
|---|---|---|
| `checkbox` | `'1'→1 ، بقیه→0` | مقدار پنهان `value="0"` قبل از چک‌باکس |
| `number` | `(int)` + clamp به min/max | |
| `text` | `sanitize_text_field` | |
| `textarea` | `sanitize_textarea_field` | |
| `richtext` | `wp_kses($v, ['br','em','strong'])` | فقط برای عنوان/شعار |
| `footer_html` | `wp_kses` allow-list `b,strong,br,a` + `WP_HTML_Tag_Processor` برای افزودن `rel="noopener noreferrer"` به `target="_blank"` | |
| `url` | `esc_url_raw` با allow-list `http,https,tel,mailto` | |
| `email` | `sanitize_email` | |
| `phone` | تبدیل `۰-۹/٠-٩`→لاتین سپس `preg_replace('/[^+0-9]/','')` | |
| `color` | `sanitize_hex_color` | |
| `media` | `absint` + `wp_attachment_is_image` | |
| `page` | `absint` | |
| `select` | `in_array` با choices مجاز | |

---

## ۴) تب‌های اجباری (۷) + تب‌های اختیاری

| # | تب | مثال فیلدها |
|---|---|---|
| ۱ | **هدر** | لوگو، عرض لوگو، نوار بالا، هدر چسبان، مگامنو، دکمه‌ی CTA |
| ۲ | **فوتر** | نمایش فوتر/ستون‌ها، معرفی، عناوین ستون‌ها، **کپی‌رایت آمل نوین (پیش‌فرض غیرقابل حذف)** |
| ۳ | **کنترل فروشگاه** | تعداد محصول/ستون، ویترین خانه، تخفیف‌ها، وضعیت ووکامرس (فقط در حوزه‌ی فروشگاهی) |
| ۴ | **صفحات** | بخش‌های صفحه اصلی (show/order/title/image/button)، انتخاب برگه‌ها، hero، درباره/تماس |
| ۵ | **سئو** | متادیتا و Schema داخلی، OG/Twitter، noindex جست‌وجو/آرشیو، توضیح پیش‌فرض — با پیام «با افزونه‌ی سئو خودکار کنار می‌رود» |
| ۶ | **بهینه‌سازی و سرعت** | حذف ایموجی/embed/version، defer JS، حذف Dashicons برای مهمان، وضعیت کش + دکمه‌ی پاک‌سازی |
| ۷ | **بروزرسانی** | نسخه‌ی فعلی، آپلود/اعمال پچ، تاریخچه و rollback (بخش ۷) |

**تب‌های اختیاری (بر اساس حوزه):** `هویت و رنگ‌ها` (لوگو/رنگ/فونت) · `تماس و شبکه‌ها` (تلفن/ایمیل/شبکه‌های اجتماعی/نقشه) · `پشتیبانی تنظیمات` (برون‌ریزی/درون‌ریزی).

---

## ۵) صفحه‌ی پنل (رندر)

```php
add_action('admin_menu', function () {
    add_menu_page('تنظیمات قالب {brand} نوین', 'تنظیمات قالب', 'manage_options',
        '{slug}-theme-settings', '{slug}_settings_page', 'dashicons-admin-generic', 61);
    add_theme_page('تنظیمات قالب {brand} نوین', 'تنظیمات قالب', 'manage_options',
        '{slug}-theme-settings', '{slug}_settings_page');
});

register_setting('{slug}_settings', SETTINGS_KEY, [
    'type' => 'array', 'default' => [],
    'sanitize_callback' => '{slug}_sanitize_settings',
]);
```

- **یک فرم** با `settings_fields()` که به `options.php` می‌رود (nonce داخلی Settings API).
- تب‌ها: `role="tablist/tab/tabpanel"` + `aria-selected` + `hidden` روی پنل‌های غیرفعال؛ ذخیره **همه‌ی تب‌ها با یک دکمه**.
- savebar ثابت: «ذخیره تنظیمات قالب» + هشدار «خروج با تغییر ذخیره‌نشده» (JS).
- هدر پنل: نام برند + نسخه‌ی قالب + دکمه‌ی «مشاهده سایت ↗» + نمایش آخرین ذخیره.
- enqueue **فقط** در صفحه‌ی پنل: `wp_enqueue_media` + `wp-color-picker` + فایل‌های ادمین با نسخه.
- `if (! current_user_can('manage_options')) return;` در بالای تابع صفحه.

---

## ۶) بازنشانی، برون‌ریزی/درون‌ریزی

### بازگردانی پیش‌فرض‌ها
```php
// admin_post با: current_user_can + check_admin_referer + چک‌باکس confirm اجباری
delete_option(SETTINGS_KEY);  // فقط option همین پنل — محتوا/رسانه/منو دست‌نخورده
```

### JSON (الگوی رنگ صادقی)
```json
{ "format": "{slug}-theme-settings", "format_version": 1,
  "theme_version": "1.0.0", "exported_at": "ISO-8601", "options": { ... } }
```
- درون‌ریزی: اعتبارسنجی `format` + شکل آرایه نسبت به defaults (عدم تطابق = رد، بدون نوشتن) + سقف ۲MB.
- درون‌ریزی فقط برای کاربر با `unfiltered_html`.

---

## ۷) بروزرسانی از طریق Patch (مال `PLUG` — الگوی سایانا)

```
{slug}-patch-1.0.0-to-1.0.1.zip
├── {slug}-patch.json        ← { format, from, to, files: [{path, sha256, action}] }
└── (فایل‌های تغییریافته با همان مسیر نسبی قالب)
```
- **staging:** `uploads/{slug}-patches/` (نه داخل پوشه‌ی قالب).
- **سقف:** ۲۰MB حجم، ۴۰۰ فایل (الگوی سایانا).
- ترتیب اعمال: capability (`update_themes`) + nonce → تأیید `sha256` همه‌ی فایل‌ها → **پشتیبان از فایل‌های فعلی** → apply → لاگ → دکمه‌ی rollback.
- ناهماهنگی هش = توقف کامل با پیام فارسی (هیچ فایلی نوشته نمی‌شود).
- بخش «بروزرسانی» خودِ پنل تنظیمات + زیرمنوی مستقل.
- نکته: پچ ترمیمی (`chobin-patch-repair.zip`) هم باید پشتیبانی شود — فایل‌های خراب از روی نسخه‌ی سالم.

---

## ۸) کش هنگام ذخیره (بعد از هر save/reset/apply پچ)

1. پاک‌سازی کش ویوی قالب با **شماره نسخه** (کلید کش شامل `theme version` باشد؛ در اولین ورود ادمین بعد از بروزرسانی هم یک بار پاک شود).
2. درخواست پاک‌سازی افزونه‌های کش: WP Rocket، W3 Total Cache، WP Super Cache، Cache Enabler، رویداد LiteSpeed.
3. دکمه‌ی «پاک‌سازی کش قالب» در پنل + نمایش آخرین زمان.
4. پیام راهنما: کش سرور/CDN باید از پنل همان سرویس پاک شود.

---

## ۹) چک‌لیست پذیرش پنل (توسط `QA`)

- [ ] یک option واحد + schema به‌عنوان تنها منبع حقیقت
- [ ] ۷ تب اجباری موجود و فارسی/RTL با `role`های درست
- [ ] هر فیلد sanitize مخصوص تایپ خودش دارد؛ خروجی‌ها escape شده
- [ ] خالی گذاشتن = پیش‌فرض/محتوای فعلی (آزمون عملی: فیلد را خالی کن، ذخیره کن، محتوا پابرجاست)
- [ ] ذخیره با یک دکمه‌ی واحد + هشدار خروج ذخیره‌نشده
- [ ] بازنشانی با nonce + confirm و فقط option پنل
- [ ] (در صورت وجود JSON) رد درون‌ریزی نامعتبر بدون نوشتن
- [ ] پچ: هش‌چک، پشتیبان، لاگ، rollback — با یک پچ آزمایشی واقعی
- [ ] بعد از ذخیره، کش ویو و کش افزونه‌ها پاک می‌شود (شواهد در گزارش)
- [ ] کاربر بدون `manage_options` به فرم/اکشن دسترسی ندارد (آزمون با کاربر Subscriber)
- [ ] صفر `php -l` و صفر fatal (`scripts/validate_theme.py` سبز)
