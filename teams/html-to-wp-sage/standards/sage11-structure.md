# استاندارد ساختار قالب — Sage 11 بدون Composer

این استاندارد، **تنها** ساختار مجاز برای خروجی این تیم است. هدف: تجربه‌ی توسعه‌ی Sage 11 (Roots) با صفر وابستگی به Composer — قابل آپلود فقط با یک پوشه.

---

## ۱) درخت فایل‌های استاندارد

```
theme-name/
├── style.css                    ← فقط متادیتای وردپرس (Name, Version, Requires, Text Domain)
├── functions.php                ← فقط: defined('ABSPATH') + require bootstrap/init.php (زیر ۱۰ خط)
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
│   ├── View/
│   │   ├── Engine.php           ← موتور مینی-Blade (بلوک‌های @extends/@section/@include/@foreach/@if)
│   │   └── Compiler.php         ← کامپایل به PHP + کش در assets/cache/views/
│   ├── Providers/               ← ThemeServiceProvider, AssetServiceProvider, SeoServiceProvider...
│   ├── Support/                 ← کلاس‌های سبک (بدون illuminate — بازنویسی ساده)
│   └── Controllers/             ← کنترلرهای سبک صفحات (اختیاری)
│
├── config/                      ← آرایه‌های PHP، بدون .env
│   ├── theme.php                ← textdomain، image sizes، منوها
│   ├── assets.php               ← entryها، نسخه‌سازی، no-build
│   └── seo.php                  ← قالب متا، Schema پیش‌فرض حوزه
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
│   │   ├── partials/            ← nav, footer, hero, cta, breadcrumbs
│   │   │   ├── blocks/          ← بخش‌های قابل استفاده (services, testimonials, faq...)
│   │   │   └── forms/           ← contact, booking, newsletter (nonce‌دار)
│   │   └── components/          ← card, badge, button, section-title...
│   ├── styles/
│   │   ├── tokens.css           ← متغیرها (رنگ، فونت، فاصله) — تنها منبع مقادیر
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
│   ├── fonts/                   ← فونت subset‌شده فارسی
│   └── images/
│
├── languages/                   ← theme-name-fa_IR.po / .mo
├── vendor-free notes:            ← هیچ composer.json، vendor/ یا package manager سمت PHP مجاز نیست
├── docs/                        ← ۶ فایل تحویل (به TEAM.md §7)
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
// functions.php — فقط این:
<?php
defined('ABSPATH') || exit;
require get_template_directory() . '/bootstrap/init.php';
```
- منطق enqueue، هوک‌ها و Settings API در `app/Providers/*` ثبت می‌شوند، نه در `functions.php`.
- خروجی `assets/build/manifest.json` توسط `AssetServiceProvider` خوانده می‌شود؛ در نبود manifest از `assets/js` fallback استفاده می‌شود.

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
- [ ] `functions.php` زیر ۱۰ خط و فقط bootstrap است
- [ ] درخت فایل‌ها با این سند یکی است
- [ ] هر view با موتور مینی-Blade کامپایل می‌شود (بدون خطا)
- [ ] manifest Vite خوانده می‌شود؛ fallback no-build هم کارا است
- [ ] `theme.json` با `tokens.css` هم‌خوان است
- [ ] اسکریپت build بدون Composer اجرا می‌شود (`npm ci && npm run build`)
