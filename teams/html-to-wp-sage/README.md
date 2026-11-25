# تیم ۱۰ نفره‌ی تبدیل HTML به قالب وردپرس — Sage 11 بدون Composer
**HTML-to-Sage WordPress Theme Squad — 10 AI Agents**

یک تیم ۱۰ نفره‌ی هوش مصنوعی که **قالب‌های HTML استاتیک** را به **قالب وردپرس استاندارد** با معماری **Sage 11 بدون Composer** تبدیل می‌کند: برای هر حوزه‌ی کاری، یک قالب ریسپانسیو با **Performance بالای ۹۰** و **سئوی حرفه‌ای**.

---

## اعضا

| # | کد | ایجنت | تخصص اصلی | فایل پروفایل |
|---|----|-------|-----------|--------------|
| ۱ | `TL` | **کاوه — سرپرست گروه** | بریف، تعریف حوزه، تقسیم کار، Decision Log، تحویل نهایی | `agents/01-team-lead.md` |
| ۲ | `ARCH` | **آراد — معمار قالب** | ممیزی HTML، قرارداد تبدیل، نقشه‌ی فایل‌ها و template hierarchy | `agents/02-theme-architect.md` |
| ۳ | `SAGE` | **ساغر — مهندس هسته‌ی Sage/Blade** | bootstrap بدون Composer، autoloader، موتور مینی-Blade، helpers | `agents/03-sage-blade-engineer.md` |
| ۴ | `CONV` | **نوید — مهندس تبدیل HTML** | HTML → Blade: layout، partials، components، لوپ‌ها، فرم‌ها | `agents/04-html-converter.md` |
| ۵ | `CSS` | **نگین — مهندس CSS و ریسپانسیو** | توکن‌ها، ۳۶۰/۷۶۸/۱۴۴۰، RTL با logical properties، WCAG | `agents/05-css-responsive-engineer.md` |
| ۶ | `JS` | **سامیار — مهندس JS و Build** | جاوااسکریپت بدون jQuery، Vite با npm، حالت no-build | `agents/06-js-build-engineer.md` |
| ۷ | `WP` | **مهرداد — یکپارچه‌ساز وردپرس** | هوک‌ها، enqueue، theme.json، Settings API، امنیت، i18n | `agents/07-wordpress-integrator.md` |
| ۸ | `SEO` | **سپیده — متخصص سئو** | متاتگ‌ها، Schema حوزه، سلسله‌مراتب عنوان، سئوی فارسی | `agents/08-seo-specialist.md` |
| ۹ | `PERF` | **آوین — متخصص عملکرد** | Core Web Vitals، بودجه‌ی عملکرد، اثبات Lighthouse ≥ ۹۰ | `agents/09-performance-engineer.md` |
| ۱۰ | `QA` | **ژینا — مدیر تست و خطایابی** | تست، ریشه‌یابی باگ، رگرسیون با منبع، دروازه‌ی انتشار | `agents/10-qa-debug-lead.md` |

**رهبر تیم (Orchestrator):** در چت، `TL` بریف را می‌گیرد، کار را بین ۹ ایجنت توزیع می‌کند، خروجی‌ها را یکپارچه می‌کند و نهایتاً با `QA` بسته‌ی تحویل را می‌بندد.

---

## فایل‌های این بسته

| فایل | کاربرد |
|------|--------|
| `README.md` | همین راهنما |
| `TEAM.md` | پروتکل همکاری: جریان ۱۰ مرحله‌ای، قرارداد تبدیل، Handoff، DoD، مسیریابی |
| `config.json` | مانیفست تیم: ۱۰ ایجنت + الزامات سخت + pipeline (قابل ایمپورت) |
| `agents/01-…-10-…` | پروفایل هر ایجنت + **System Prompt کپی‌شدنی** (انگلیسی) |
| `standards/sage11-structure.md` | استاندارد ساختار قالب Sage 11 بدون Composer |
| `standards/conversion-checklist.md` | جدول نگاشت اجباری HTML → وردپرس + چک‌لیست پذیرش CONVERT |
| `templates/PROJECT_BRIEF.md` | فرم بریف پروژه (پر کن، بده به `TL`) |
| `templates/CONVERSION_REPORT.md` | قالب گزارش تبدیل ۱:۱ |
| `prompts/QUICKSTART.md` | دستورات راه‌انداز سریع |

---

## چطور در همین چت استفاده کنی

فایل‌های HTML و حوزه‌ی کاری را بنویسید. مثال:

> «این ۵ فایل HTML را برای حوزه‌ی پزشکی به قالب وردپرس Sage 11 بدون Composer تبدیل کنید؛ RTL، نوبت‌دهی، Lighthouse بالای ۹۰ و سئوی محلی.»

خط تولید این‌طور جواب می‌دهد:

```
TL    → بریف + حوزه کاری + بودجه عملکرد
ARCH  → ممیزی HTML + قرارداد تبدیل + نقشه فایل‌ها
SAGE  → اسکلت بدون Composer (autoloader + مینی-Blade + config)
CONV  → viewهای Blade وفادار به HTML منبع
CSS   → توکن‌ها + ریسپانسیو + RTL
JS    → کامپوننت‌ها + build (Vite/npm) + no-build
WP    → هوک‌ها + enqueue + theme.json + امنیت
SEO   → متا + Schema حوزه + سلسله‌مراتب
PERF  → بهینه‌سازی + اثبات ≥ ۹۰
QA    → تست/خطایابی + PASS/FAIL
SHIP  → قالب نهایی + docs/01..06 + استاندارد حوزه
```

### دستورات سریع

| دستور | نتیجه |
|-------|-------|
| `/all <توضیح>` | کل ۱۰ ایجنت، کل pipeline |
| `/brief` | فقط بریف و Decision Log |
| `/arch <فایل HTML>` | ممیزی + قرارداد |
| `/blade` | اسکلت بدون Composer |
| `/convert` | تبدیل HTML به Blade |
| `/css` | استایل + ریسپانسیو + RTL |
| `/js` | اسکریپت‌ها + build |
| `/wp` | یکپارچه‌سازی وردپرس |
| `/seo` | سئوی حرفه‌ای |
| `/perf` | بنچمارک و بهینه‌سازی |
| `/qa` | تست و خطایابی |
| `/ship` | بسته‌ی نهایی |
| `/review <کد>` | دیدگاه هر ۱۰ ایجنت |

---

## الزامات سخت (خط قرمز تیم)

1. **بدون Composer:** هیچ `composer.json`/`vendor/` — قالب فقط با آپلود پوشه کار می‌کند (Sage 11 style، `package.json` فقط برای build دارایی‌ها).
2. **Performance ≥ ۹۰:** Lighthouse موبایل **و** دسکتاپ؛ LCP ≤ 2.5s، INP ≤ 200ms، CLS ≤ 0.1 — با شاهد مکتوب در `docs/04-performance-report.md`.
3. **سئوی حرفه‌ای:** متاتگ‌ها، Schema متناسب با حوزه، یک H1، alt واقعی، سئوی فارسی بدون stuffing.
4. **ریسپانسیو:** 360 / 768 / 1024 / 1440 بدون اسکرول افقی + RTL-first با logical properties.
5. **استاندارد هر حوزه:** هر پروژه یک `docs/06-domain-standard.md` تولید می‌کند تا نوبت بعدی همان حوزه از صفر شروع نشود.
6. **امنیت:** nonce روی همه‌ی فرم‌ها + escape سه‌لایه + `ABSPATH` guard.
7. **بدون قرارداد `ARCH` کدی نوشته نمی‌شود** و بدون PASS از `QA` چیزی تحویل داده نمی‌شود.

---

## چرا «Sage 11 بدون Composer»؟

Sage 11 (Roots) معماری مدرنی دارد: `app/`، `bootstrap/`، `resources/views`، `config/`، `routes/`، Blade و Vite — اما معمولاً با Composer نصب می‌شود. این تیم همان تجربه را **بدون Composer** می‌سازد:

- بارگذار کننده‌ی سفارشی PSR-4 مانند به‌جای autoload ساز Composer
- موتور **مینی-Blade** داخلی به‌جای illuminate/view
- `config()` با آرایه‌های PHP به‌جای dotenv/illuminate/config
- **Vite با npm** برای دارایی‌ها (npm مجاز است، Composer ممنوع) + خروجی build commit‌شده + حالت no-build

---

*نسخه ۱.۰ — ساخته‌شده برای مخزن تیم‌های ایجنت آمل نوین*
