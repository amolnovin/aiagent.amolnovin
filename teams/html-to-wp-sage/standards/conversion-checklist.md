# چک‌لیست استاندارد تبدیل HTML به وردپرس

مال `CONV` برای اجرا، `ARCH` برای قرارداد، `QA` برای رگرسیون. هر آیتم قبل از عبور از مرحله‌ی CONVERT باید پر باشد.

---

## ۱) جدول نگاشت اجباری (HTML → وردپرس)

| HTML منبع | مقصد در قالب | معادل وردپرس / یادداشت |
|---|---|---|
| `<head>` سفارشی | `layout/partials/head.blade.php` | `wp_head()` — متاتگ با `SEO` |
| `<body>` سراسری | `layout/app.blade.php` | `body_class()`، `wp_body_open()` |
| `<header class="navbar">` | `partials/nav.blade.php` | `wp_nav_menu` با fallback سفارشی |
| لوگوی `<img>` | `partials/nav.blade.php` | `custom-logo` / `the_custom_logo()` |
| `<nav>` فوتر/مobil | `layout/footer.blade.php` | `register_nav_menus` (footer) |
| `<section id="hero">` | `partials/blocks/hero.blade.php` | theme mod + تنظیمات قالب |
| کارت‌های تکرارشونده | `components/card.blade.php` | لوپ CPT/ووکامرس/تنظیمات |
| لیست خدمات/مقالات | `partials/blobs/services...` → pages/* | `have_posts()` / `the_post()` |
| `<img src=...>` | همان جای DOM | `wp_get_attachment_image` با `srcset/sizes` |
| `<form id="contact">` | `partials/forms/contact.blade.php` | `wp_nonce_field` + admin-ajax/POST + `esc_*` |
| `<input type="text">` | همان فرم | `name/id` استاندارد + `required` حفظ شود |
| `<a href="#">` داخلی | همان | `home_url()` / `get_permalink()` با `esc_url` |
| `<a href="tel:/mailto:">` | همان | از تنظیمات قالب، `esc_attr` |
| `<h1>`…`<h6>` | همان سلسله‌مراتب | یک `H1` در هر الگو؛ ترتیب بدون پرش |
| `<img alt>` | همان | `alt` واقعی از داده‌ی تصویر/محتوا |
| `<span class="badge">` | `components/badge.blade.php` | داده‌ی پویا |
| بخش نظرات | `partials/blocks/testimonials.blade.php` | CPT یا ووکامرس reviews |
| `<footer>` | `layout/footer.blade.php` | ویجت + تنظیمات شبکه‌های اجتماعی |
| اسکریپت ثالث | تصمیم `ARCH` | نگهداری/حذف/بازنویسی + enqueue از `JS` |
| فونت (`@font-face`) | `assets/fonts/` | subset فارسی + preload + `swap` |
| `<section>` فروشگاه/گرید محصول | `woocommerce/archive-product.php` + `content-product.php` | **override ووکامرس** (`woocommerce-integration.md`) |
| صفحهٔ تک‌محصول | `woocommerce/single-product.php` + `content-single-product.php` | دادهٔ واقعی WC (قیمت/موجودی/گالری) |
| سبد خرید / تسویه / سفارش | `woocommerce/cart/*` + `woocommerce/checkout/*` | **هرگز قالب پیش‌فرض WC** |
| لوپ محصول/مقاله با دادهٔ نمونه | Seeder (`inc/seed/` یا `content/seed.xml`) | `content-seeding.md` — داده از HTML منبع ساخته می‌شود |

---

## ۲) قواعد تبدیل

1. **وفاداری اول:** ساختار DOM، کلاس‌ها و ترتیب بصری حفظ می‌شود؛ تغییر ظاهر کار `CSS` است.
2. **قانون داده‌ی زنده (استاتیک ممنوع):** هر متن/لینک/تصویری که کارفرما باید بعداً عوض کند، به theme mod /
   تنظیمات قالب / محتوای وردپرس وصل می‌شود. **هیچ پاراگراف/متن فارسیِ بلند (≥ ۴۰ نویسه) در فایل‌های view
   هاردکد نمی‌شود** — اگر متنی در HTML هست، یا به داده‌ی وردپرس (برگه/نوشته/محصول/تنظیمات) وصل می‌شود یا
   برچسب UI کوتاه با `__()`. لیست «منبع هر متن» در `docs/content-manifest.md` ثبت و به `WP` برای
   بذرگذاری (`content-seeding.md`) تحویل داده می‌شود. آزمون QA: تغییر مقدار در ادمین → تغییر فوری در front.
3. **escape اجباری:** `{{ }}` یا `esc_*` برای هر خروجی پویا؛ `{!! !!}` فقط با `wp_kses_post` و دلیل مکتوب.
4. **فرم امن:** `wp_nonce_field` + بررسی سمت سرور + پیام خطای فارسی + حالت loading/success.
5. **لوپ تمیز:** بدون کوئری اضافه در هر تکرار (هماهنگ با `PERF` برای transient).
6. **i18n:** همه‌ی رشته‌های قالب با `__()`/`esc_html__()` و text domain ثابت — تا `languages/` کار کند.
7. **RTL-first:** چیدمان با logical properties سازگار باشد؛ `dir` از `layout` مدیریت شود.
8. **بدون اختراع:** هر بلوکِ خارج از قرارداد = سؤال به `ARCH`، نه کد حدسی.

---

## ۳) صفحات حداقلی هر قالب استاندارد

هر حوزه‌ی کاری با این مجموعه‌ی حداقلی تحویل می‌شود (بقیه بر اساس بریف):

```
front-page (خانه)      page (درباره، تماس، خدمات...)
single (مقاله/محصول)   archive (دسته/برچسب/فهرست)
search                 404
├─ partials: nav, footer, hero, cta, breadcrumbs
├─ components: card, button, badge, section-title
└─ forms: contact (همیشه) + booking|newsletter (طبق حوزه)

حوزهٔ فروشگاهی (علاوه بر موارد بالا — مرجع: woocommerce-integration.md):
woocommerce/ archive-product + single-product + cart/ + checkout/ (شامل thankyou)
```

**همه‌ی این صفحات بعد از بذرگذاری (`content-seeding.md`) با داده‌ی واقعی پر می‌شوند — تحویل «قالب خالی» نداریم.**

---

## ۴) چک‌لیست پذیرش مرحله‌ی CONVERT (امضای `CONV` + تأیید `ARCH`)

- [ ] جدول نگاشت بالا کامل شده؛ هیچ `<section>` جا نمانده
- [ ] یک `H1` در هر الگو؛ ترتیب هدینگ بدون پرش
- [ ] همه‌ی تصاویر `alt` واقعی + آماده‌ی `srcset` دارند
- [ ] همه‌ی فرم‌ها nonce + escape + پیام خطای فارسی
- [ ] هیچ href/#، متن لورم‌ایپسوم یا دامنه‌ی نمونه باقی نمانده
- [ ] **صفر متن فارسی بلند (≥ ۴۰ نویسه) هاردکد در viewها** — همه به داده/تنظیمات/`__()` وصل‌اند
- [ ] **`docs/content-manifest.md`** برای تحویل به `WP` (بذرگذاری) کامل است
- [ ] خروجی در WP_DEBUG بدون notice و بدون خطای کنسول
- [ ] رگرسیون چشمی با HTML منبع: هر ۳ عرض ۳۶۰/۷۶۸/۱۴۴۰
