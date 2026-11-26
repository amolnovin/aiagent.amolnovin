# استاندارد ساختار قالب — Sage 11 بدون Composer

این استاندارد، **تنها** ساختار مجاز برای خروجی این تیم است. هدف: تجربه‌ی توسعه‌ی Sage 11 (Roots) با صفر وابستگی به Composer — قابل آپلود فقط با یک پوشه.

---

## ۰) الزامات ثابت برند (همه‌ی قالب‌ها)

### الف) نام قالب = نام برند + «نوین»
```
سایانا نوین        → slug: sayana-novin        → text domain: sayana-novin
کلینیک رادین نوین  → slug: radin-novin          → text domain: radin-novin
```
- نام نمایشی در `style.css`، نام پنل تنظیمات، title و text domain همگی از همین قاعده پیروی می‌کنند.
- انتخاب نام برند با `TL` (بریف) و ثبت slug با `ARCH` انجام می‌شود.

### ب) کپی‌رایت فوتر (اجباری — حذف‌نشدنی)
در همه‌ی قالب‌ها، ردیف زیر در فوتر نمایش داده می‌شود (قابل تغییر رنگ/استایل، ولی متن و لینک ثابت):
```html
طراحی و توسعه: <a href="https://amolnovin.ir" rel="nofollow noopener">مجموعه فناوری اطلاعات آمل نوین</a>
```
- متن فارسی دقیق: **«مجموعه فناوری اطلاعات آمل نوین»** — لینک به `https://amolnovin.ir`.
- از `get_theme_mod('footer_credit')` خوانده می‌شود ولی **پیش‌فرض همین متن است** و پاک‌سازی کامل آن ممنوع است.

### ج) فونت رسمی: IranSans
- فونت bundled در `assets/fonts/iransans/` (نگاه کن به `assets/fonts/README.md`) — منبع: گوگل درایو تیم.
- `@font-face` با `font-display: swap`، اولویت `woff2`، وزن‌های استفاده‌شده فقط.
- `--font-sans: 'IRANSans', ...` در `tokens.css`؛ عدد فارسی با نسخه‌ی FaNum.

---

## ۱) درخت فایل‌های استاندارد

```
{brand}-novin/                  ← نام فولدر = slug برند + novin (مثلا sayana-novin)
├── style.css                    ← فقط متادیتای وردپرس (Name: {brand} نوین, Version, Text Domain)
├── functions.php                ← فقط: گارد ABSPATH + گارد نسخهٔ PHP + گارد is_file
│                                   + require_onceهای bootstrap/init.php (بدون تعریف/هوک اضافه)
├── theme.json                   ← رنگ/فونت/layout هم‌گام با tokens.css
├── index.php                    ← fallback وردپرس (اجباری)
├── screenshot.png               ← ۱۲۴۰×۹۶۰
│
├── bootstrap/
│   ├── init.php                 ← ترتیب راه‌اندازی: autoloader → config → providers → hooks
│   ├── autoloader.php           ← spl_autoload_register برای App\ → app/ (PSR-4 مانند)
│   └── providers.php            ← فهرست Service Providerها
│
├── app/
│   ├── helpers.php              ← view(), config(), asset(), e(), dd()
│   ├── Engine/                  ← ★ موتور پردازش قوی قالب (بخش ۲)
│   │   ├── Compiler.php         ← کامپایل templateها با cache
│   │   ├── Container.php        ← سرویس‌های سبک (singleton/factory)
│   │   └── Pipeline.php         ← زنجیره‌ی middleware پردازش request/response
│   ├── View/Engine.php          ← لایه‌ی نمای موتور (بلوک‌های Blade)
│   ├── Providers/               ← ThemeServiceProvider, SettingsServiceProvider,
│   │                               AssetServiceProvider, SeoServiceProvider, UpdaterServiceProvider
│   ├── Support/                 ← کلاس‌های سبک (بدون illuminate — بازنویسی ساده)
│   └── Controllers/             ← کنترلرهای سبک صفحات (اختیاری)
│
├── config/                      ← آرایه‌های PHP، بدون .env
│   ├── theme.php                ← نام قالب، textdomain، image sizes، منوها، footer credit
│   ├── assets.php               ← entryها، نسخه‌سازی، no-build
│   ├── seo.php                  ← قالب متا، Schema پیش‌فرض حوزه
│   └── settings.php             ← بخش‌های پنل تنظیمات (بخش ۳)
│
├── inc/
│   └── settings/                ← ★ پنل تنظیمات قالب (بخش ۳)
│       ├── class-settings-page.php    ← منوی پنل + تب‌ها
│       ├── sections/header.php
│       ├── sections/footer.php        ← شامل کپی‌رایت آمل نوین
│       ├── sections/store.php         ← کنترل فروشگاه (در صورت حوزه)
│       ├── sections/pages.php
│       ├── sections/seo.php
│       ├── sections/performance.php   ← بهینه‌سازی و سرعت
│       └── sections/updates.php       ← بروزرسانی قالب از طریق patch
│
├── routes/
│   └── web.php                  ← مسیریابی ساده‌ی صفحات سفارشی
│
├── resources/
│   ├── views/
│   │   ├── layout/
│   │   │   ├── app.blade.php    ← اسکلت کلی (head, body, wp_head, wp_footer)
│   │   │   └── partials/        ← head.blade.php
│   │   ├── pages/               ← front-page, page, single, archive, search, 404
│   │   ├── partials/            ← nav, footer (با کپی‌رایت)، hero, cta, breadcrumbs
│   │   │   ├── blocks/          ← بخش‌های قابل استفاده (services, testimonials, faq...)
│   │   │   └── forms/           ← contact, booking, newsletter (nonce‌دار)
│   │   └── components/          ← card, badge, button, section-title...
│   ├── styles/
│   │   ├── fonts.css            ← @font-face اجباری IranSans (swap + woff2 اول)
│   │   ├── tokens.css           ← متغیرها (رنگ، فونت=IRANSans، فاصله) — تنها منبع مقادیر
│   │   ├── base.css             ← reset + عناصر پایه (RTL-safe)
│   │   ├── layout.css           ← ساختار + breakpointها
│   │   ├── components.css
│   │   └── main.css             ← ورودی build (import به ترتیب)
│   ├── scripts/
│   │   ├── main.js              ← ورودی build
│   │   └── components/          ← nav, accordion, form...
│   └── images/
│
├── assets/                      ← خروجی build — قابل commit (میزبان بدون Node هم کار می‌کند)
│   ├── build/                   ← main.[hash].js / main.[hash].css + manifest.json
│   ├── js/                      ← نسخه‌ی no-build (fallback)
│   ├── fonts/
│   │   └── iransans/            ← فونت رسمی bundled (نگاه کن assets/fonts/README.md)
│   └── images/
│
├── patches/                     ← ★ فایل‌های بروزرسانی patch قالب
│   └── manifest.json            ← نسخه‌ها، هش فایل‌ها، دستور apply
│
├── languages/                   ← {slug}-fa_IR.po / .mo
├── vendor-free notes:            ← هیچ composer.json، vendor/ یا package manager سمت PHP مجاز نیست
├── docs/                        ← ۸ فایل تحویل (به TEAM.md §7)
│
├── package.json                 ← فقط برای build دارایی‌ها (npm: vite ...) — اجباری نیست روی میزبان
├── vite.config.js
└── README.md                    ← راهنمای نصب/توسعه‌ی قالب
```

---

## ۲) قوانین ثابت

### بدون Composer
1. هیچ `composer.json`، `composer.lock`، `vendor/` یا `require vendor/...` در قالب نیست.
2. بارگذاری کلاس فقط از `bootstrap/autoloader.php` (نام‌فضای `App\` ← `app/`).
3. وابستگی‌های Laravel/Illuminate به معادل سبک داخلی منتقل می‌شوند (`app/Support`) — یا حذف.
4. `package.json` فقط برای Vite/Tailwind در توسعه است؛ **خروجی build باید commit شود** تا میزبان به Node نیاز نداشته باشد.

### مینی-Blade (حداقل پشتیبانی اجباری)
```
@extends / @section / @yield
@include('path', [vars])
@if / @elseif / @else / @endif
@foreach / @endforeach
{{ expression }}          ← escape خروجی
{!! expression !!}        ← فقط با دلیل مکتوب و داده‌ی قبلاً sanitize‌شده (wp_kses_post)
@php / @endphp            ← ممنوع در تحویل، مگر استثنا تأییدشده
```
- کامپایل‌ها در production در `assets/cache/views/` کش می‌شوند؛ در development بدون کش.
- کش با `filemtime`/هش تغییرات باطل می‌شود.

### نقطه‌ی اتصال با وردپرس
```php
// functions.php — فقط این (الگوی کامل: fatal-error-prevention.md §2):
<?php
defined('ABSPATH') || exit;

if (version_compare(PHP_VERSION, '8.1', '<')) {   // گارد PHP قدیمی → اعلان + return
    add_action('admin_notices', /* پیام فارسی */);
    return;
}
if (! is_file(__DIR__ . '/bootstrap/init.php')) { // گارد بیلد ناقص → اعلان + return
    add_action('admin_notices', /* «فایل‌های قالب کامل نیستند» */);
    return;
}
require_once __DIR__ . '/bootstrap/init.php';     // هرگز require بدون _once
```
- منطق enqueue، هوک‌ها و Settings API در `app/Providers/*` ثبت می‌شوند، نه در `functions.php`
  (تنها استثنا: هوک‌های `admin_notices` برای گاردهای بالا).
- خروجی `assets/build/manifest.json` توسط `AssetServiceProvider` خوانده می‌شود؛ در نبود manifest از `assets/js` fallback استفاده می‌شود.
- دروازه‌ی کنترل: `python3 scripts/validate_theme.py release/{slug}/` باید سبز باشد.

### نام‌گذاری
| چیز | قاعده | مثال |
|---|---|---|
| فایل‌های view | kebab-case + `.blade.php` | `service-card.blade.php` |
| کلاس‌ها | PSR-4، PascalCase | `App\View\Compiler` |
| متغیرهای CSS | kebab با پیشوند `--` | `--color-primary` |
| optionهای قالب | `theme_{group}_{field}` | `theme_hero_title` |
| text domain | نام folder قالب | `theme-name` |

### امنیت (مال `WP`، اجرا در همه‌ی لایه‌ها)
- `defined('ABSPATH') || exit;` در بالای هر فایل PHP.
- escape سه‌لایه: `esc_html` / `esc_attr` / `esc_url` / `wp_kses_post`.
- nonce روی هر فرم + بررسی سمت سرور (`check_ajax_referer` / `wp_verify_nonce`).

---

## ۲-ب) موتور پردازش قوی قالب (مال `SAGE`)

قالب باید یک **موتور پردازش (Processing Engine)** قوی داشته باشد — نه صرفاً چند تابع کمکی. حداقل اجزا:

```
app/Engine/
├── Compiler.php     ← کامپایل templateها: parse → PHP + کش file-based با invalidation هش/فایل‌زمان
│                      خطاهای کامپایل با پیام فایل/خطی و fallback به نسخه‌ی قبلی در production
├── Container.php    ← کانتینر سرویس: singleton(), factory(), bind() با lazy-loading
│                      ثبت سرویس‌ها در providers و واکشی در هنگام نیاز (بدون new پراکنده)
├── Pipeline.php     ← زنجیره‌ی middleware پردازش: request → [middleware...] → response
│                      middlewareهای نمونه: locale/RTL، settings loader، SEO headers، cache view
└── Events.php       ← dispatch/listen سبک (جایگزین do_action سطح بالا داخل قالب)
```

**قواعد موتور:**
1. هر request از یک مسیر واحد عبور می‌کند: `bootstrap → Container → Pipeline → Compiler → view`.
2. کامپایل‌ها در production کش می‌شوند؛ در `WP_DEBUG` بدون کش + پیام خطای شفاف.
3. هیچ منطق پردازشی در `functions.php` یا داخل viewها نیست — فقط فراخوانی موتور.
4. خروجی `view('pages.x', $data)` همیشه از موتور رد می‌شود (بدون echo دستی).
5. عملکرد موتور اندازه‌گیری می‌شود: سربار کامپایل ≤ ۵ms در warm cache (گزارش به `PERF`).

---

## ۲-ج) پنل تنظیمات قالب (مال `WP` + `PLUG`)

> **سند مرجع کامل و جزئیات پیاده‌سازی: [`theme-settings-standard.md`](theme-settings-standard.md)**
> (استخراج‌شده از ۸ قالب واقعی تیم — `knowledge/real-themes-survey.md`). در صورت تعارض، آن سند حرف اول را می‌زند.

هر قالب یک **تنظیمات قالب (Theme Settings)** در پیشخوان وردپرس دارد — زیرمنوی «تنظیمات قالب {brand} نوین» با تب‌های زیر (ساختار: `inc/settings/` + Settings API):

| تب | کلید option | محتوا |
|---|---|---|
| **هدر** | `theme_header_*` | لوگو/ارتفاع/چسبندگی، منو، نوار اطلاعیه، CTA سربرگ |
| **فوتر** | `theme_footer_*` | ستون‌ها، شبکه‌های اجتماعی، **کپی‌رایت آمل نوین (غیرقابل حذف)** |
| **کنترل فروشگاه** | `theme_store_*` | (در حوزه‌ی فروشگاهی) نمایش محصولات، سبد، بنر فروش، وضعیت ووکامرس |
| **صفحات** | `theme_pages_*` | انتخاب صفحه‌ی خانه/تماس/خدمات، متن‌های hero، CTAهای ثابت |
| **سئو** | `theme_seo_*` | عنوان/توضیح پیش‌فرض، Schema فعال، ربات‌ها، اتصال به افزونه‌ی سئو |
| **بهینه‌سازی و سرعت** | `theme_perf_*` | lazy images، critical CSS، حذف اموجی/رداکشن، وضعیت کش، نمایش معیارها |
| **بروزرسانی** | `theme_updates_*` | نسخه‌ی فعلی، **بروزرسانی از طریق patch** (بخش زیر) |

**قواعد پنل:**
1. **یک option واحد** `{slug}_theme_options` + **schema به‌عنوان تنها منبع حقیقت** (`settings_schema()`)؛ همه‌ی فیلدها با `register_setting` + sanitize callback تایپ‌به‌تایپ.
2. فیلدها در قالب از طریق helper (خواندن از همان option ادغام‌شده با defaults) می‌آیند؛ بدون `get_option` پراکنده در view.
3. **خالی گذاشتن فیلد = پیش‌فرض/محتوای فعلی** — هرگز حذف محتوا.
4. فوتر کپی‌رایت: فیلد `theme_footer_credit` پیش‌فرضش متن اجباری آمل نوین است؛ خالی‌کردنش یا حذفش مجاز نیست.
5. تب «بروزرسانی» وضعیت patch را نشان می‌دهد و دکمه‌ی apply را فقط به administrator می‌دهد.
6. **بعد از هر ذخیره/بازنشانی:** پاک‌سازی کش ویو با شمارهٔ نسخه + درخواست پاک‌سازی کش افزونه‌ها (جزئیات: `theme-settings-standard.md` §8).

### بروزرسانی قالب از طریق Patch (مال `PLUG`)
```
patches/
├── manifest.json          ← { version, files: [{path, sha256, action: replace|add|delete}], min_theme_version }
└── 1.0.1-to-1.0.2/        ← فایل‌های patch (کپی تغییریافته‌ی فایل‌ها)
```
- مکانیزم: درون‌برنامه‌ای — `UpdaterServiceProvider` فایل‌های مسیرشده در `manifest.json` را با تأیید `capability` + `nonce` و **پشتیبان گرفتن قبل از apply** جایگزین می‌کند.
- هش `sha256` هر فایل قبل از جایگزینی تطبیق داده می‌شود؛ ناهماهنگی = توقف کامل با پیام خطا (هیچ فایلی نوشته نمی‌شود).
- اعمال patch روی هاست بدون SSH و بدون Composer کار می‌کند.
- **سقف‌ها و بازگشت (الگوی سایانا):** حجم پچ ≤ ۲۰MB، تعداد فایل ≤ ۴۰۰؛ staging در `uploads/{slug}-patches/`؛ لاگ اعمال + **دکمه‌ی rollback** به نسخهٔ قبل. پچ ترمیمی (فایل خراب از روی نسخهٔ سالم) هم پشتیبانی می‌شود.

---

## ۲-د) فونت رسمی IranSans

- فایل‌ها bundled: `assets/fonts/iransans/` (راهنما: `assets/fonts/README.md`؛ منبع: گوگل درایو تیم).
- اجباری در `resources/styles/fonts.css`:
```css
@font-face {
  font-family: 'IRANSans';
  src: url('../assets/fonts/iransans/woff2/IRANSansWeb(FaNum).woff2') format('woff2');
  font-weight: 400; font-style: normal; font-display: swap;
}
/* وزن‌های مورد استفاده: Light(300) Medium(500) Bold(700) — فقط لیست شده‌ها */
```
- `--font-sans: 'IRANSans', system-ui, sans-serif;` در `tokens.css`.
- preload زیرمجموعه‌ی فارسی + حذف وزن‌های بلااستفاده = رعایت بودجه‌ی فونت (≤ ۱۰۰KB).
- اعداد فارسی با نسخه‌ی FaNum همین فونت نمایش داده می‌شوند.

---

## ۳) بودجه‌ی عملکرد (مال `PERF`)

```
Lighthouse (موبایل و دسکتاپ) ≥ ۹۰  → دروازه‌ی انتشار
LCP ≤ ۲.۵s | INP ≤ ۲۰۰ms | CLS ≤ ۰.۱
HTML ≤ ۵۰KB | CSS ≤ ۳۰KB gzip | JS ≤ ۵۰KB gzip
فونت فارسی subset ≤ ۱۰۰KB با font-display: swap + preload
تعداد درخواست ≤ ۱۵
```

---

## ۴) چک‌لیست پذیرش ساختار (توسط `ARCH` و `QA`)

- [ ] بدون `composer.json` / `vendor/`
- [ ] `functions.php` فقط گاردها + `require_once` (بدون تعریف تابع/کلاس؛ فقط هوک `admin_notices`)
- [ ] درخت فایل‌ها با این سند یکی است
- [ ] نام قالب = برند + «نوین» (نمایشی) و `{brand}-novin` (slug/text domain)
- [ ] **موتور پردازش:** `app/Engine/` با Compiler + Container + Pipeline + Events و کش کامپایل فعال است
- [ ] **پنل تنظیمات:** ۷ تب (هدر، فوتر، فروشگاه، صفحات، سئو، بهینه‌سازی، بروزرسانی) با Settings API،
      یک option واحد، schemaمحور و «خالی = پیش‌فرض» — مطابق `theme-settings-standard.md`
- [ ] **بروزرسانی patch:** `patches/manifest.json` + اعمال با هش/پشتیبان/nonce + staging و rollback کار می‌کند
- [ ] **دروازه‌ی fatal:** `python3 scripts/validate_theme.py release/{slug}/` سبز است
- [ ] **فونت IranSans:** `fonts.css` با swap، `--font-sans` از IRANSans، وزن‌های غیراستفاده حذف‌اند
- [ ] **کپی‌رایت فوتر:** «مجموعه فناوری اطلاعات آمل نوین» + لینک amolnovin.ir در همه‌ی الگوها
- [ ] هر view با موتور مینی-Blade کامپایل می‌شود (بدون خطا)
- [ ] manifest Vite خوانده می‌شود؛ fallback no-build هم کارا است
- [ ] `theme.json` با `tokens.css` هم‌خوان است
- [ ] اسکریپت build بدون Composer اجرا می‌شود (`npm ci && npm run build`)
