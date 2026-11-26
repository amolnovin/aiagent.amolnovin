#!/usr/bin/env python3
"""
validate_theme.py — دروازه‌ی کنترل کیفیت قالب (تیم html-to-wp-sage)

قبل از PASS مرحلهٔ ۱۳ باید سبز شود:

    python3 scripts/validate_theme.py release/{slug}/

بررسی‌ها (细则 در standards/fatal-error-prevention.md §5):
  1. php -l روی همهٔ فایل‌های PHP (صفر خطای syntax؛ نبودِ PHP = FAIL)
  2. style.css + index.php + functions.php + تطابق Text Domain با نام پوشه
  3. وجود پوشهٔ تنظیمات با schema و register_setting
  4. موجود بودن همهٔ مسیرهای require_once استاتیک
  5. گارد ABSPATH در بالای هر فایل PHP
  6. نبودِ تکراری توابع/کلاس‌های سراسری بین فایل‌ها
  7. ممنوعیت‌ها: vendor/ و composer.json؛ require بدون once؛ هوک در functions.php
  8. patches/: manifest با sha256 برای همهٔ فایل‌ها

خروجی: گزارش خط‌به‌خط + exit code (0 = سبز، 1 = قرمز)
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict

MAX_FUNCTIONS_PHP_LINES = 80
ALLOWED_FUNCTIONS_PHP_HOOKS = {"admin_notices"}

FAILS = []
WARNS = []
PASSES = []


def ok(msg: str) -> None:
    PASSES.append(msg)
    print(f"  PASS  {msg}")


def warn(msg: str) -> None:
    WARNS.append(msg)
    print(f"  WARN  {msg}")


def bad(msg: str) -> None:
    FAILS.append(msg)
    print(f"  FAIL  {msg}")


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def php_files(root: str) -> list:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "languages", "vendor")]
        for name in filenames:
            if name.endswith(".php"):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def check_php_balance(files: list) -> None:
    """جایگزین وقتی php در PATH نیست: تعادل آکولاد/آرگومان + رشته‌ها/کامنت‌ها
    (رایج‌ترین خطای تولیدی یعنی برش خوردن فایل را می‌گیرد؛ جایگزین php -l نیست)."""

    def strip_code(text: str) -> str:
        out = []
        i, n = 0, len(text)
        state = None  # None | "'" | '"' | '//' | '/*' | 'html' | 'heredoc'
        heredoc_id = None
        while i < n:
            c = text[i]
            nxt = text[i + 1] if i + 1 < n else ""
            if state is None:
                if c == "?" and nxt == ">":  # خروج به HTML
                    state = "html"
                    i += 2
                    continue
                if c == "<" and text[i : i + 3] == "<<<":  # heredoc/nowdoc
                    j = i + 3
                    quote = ""
                    if j < n and text[j] in ("'", '"'):
                        quote = text[j]
                        j += 1
                    m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", text[j:])
                    if m:
                        heredoc_id = m.group(0)
                        state = "heredoc"
                        i = j + len(heredoc_id)
                        if quote:
                            i += 1
                        continue
                if c == "/" and nxt == "/":
                    state = "//"
                    i += 2
                    continue
                if c == "#":
                    state = "//"
                    i += 1
                    continue
                if c == "/" and nxt == "*":
                    state = "/*"
                    i += 2
                    continue
                if c in ("'", '"'):
                    state = c
                    i += 1
                    continue
                out.append(c)
                i += 1
            elif state in ("'", '"'):
                if c == "\\":
                    i += 2
                    continue
                if c == state:
                    state = None
                i += 1
            elif state == "//":
                if c == "\n":
                    state = None
                    out.append("\n")
                i += 1
            elif state == "/*":
                if c == "*" and nxt == "/":
                    state = None
                    i += 2
                    continue
                i += 1
            elif state == "html":  # بخش HTML بین ?> و <?php — نادیده گرفته می‌شود
                if c == "<" and nxt == "?" and text[i : i + 5] in ("<?php", "<?PHP"):
                    state = None
                    i += 5
                    continue
                if c == "<" and nxt == "=":
                    state = None
                    i += 2
                    continue
                i += 1
            elif state == "heredoc":
                if c == "\n" and heredoc_id:
                    line_match = re.match(
                        rf"[ \t]*{re.escape(heredoc_id)}\s*;?", text[i + 1 :]
                    )
                    if line_match:
                        state = None
                        heredoc_id = None
                        i += 1 + line_match.end()
                        continue
                i += 1
        return "".join(out)

    issues = 0
    for path in files:
        text = read(path)
        if "<?php" not in text[:200] and "<?php" not in text:
            issues += 1
            bad(f"بدون برچسب <?php: {path}")
            continue
        code = strip_code(text)
        for open_c, close_c, name in (("{", "}", "آکولاد {}"), ("(", ")", "پرانتز ()"), ("[", "]", "براکت []")):
            if code.count(open_c) != code.count(close_c):
                issues += 1
                bad(f"تعادل {name} به هم ریخته (احتمال برش خوردگی فایل): {path}")
        # فایل نباید وسط بلاک تمام شود
        if code.rstrip().endswith(("=", "=>", "&&", "||", ".", ",")):
            issues += 1
            bad(f"احتمال ناتمام بودن فایل (آخرین نشانگر عملگر): {path}")
    if not issues:
        ok(f"{len(files)} فایل PHP: تعادل ساختاری سالم (جایگزین موقت php -l)")


def check_php_lint(files: list) -> None:
    print("\n[1] php -l (خطای syntax)")
    php = shutil.which("php")
    if not php:
        warn("php در PATH نیست — lint کامل اجرا نشد؛ QA باید آن را روی میزبان دارای PHP اجرا کند")
        check_php_balance(files)
        return
    errors = 0
    for path in files:
        proc = subprocess.run(
            [php, "-l", path], capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if proc.returncode != 0:
            errors += 1
            bad(f"syntax: {path} — {(proc.stderr or proc.stdout).strip().splitlines()[0][:160]}")
    if errors == 0:
        ok(f"{len(files)} فایل PHP بدون خطای syntax")


def check_structure(root: str, theme_dir: str) -> None:
    print("\n[2] ساختار پایه")
    style = os.path.join(root, "style.css")
    if not os.path.isfile(style):
        bad("style.css وجود ندارد")
        return
    ok("style.css موجود است")
    m = re.search(r"^\s*\*\s*Text Domain:\s*(\S+)", read(style), re.M)
    if not m:
        warn("Text Domain در style.css پیدا نشد")
    elif m.group(1) != theme_dir:
        bad(f"Text Domain ({m.group(1)}) با نام پوشه ({theme_dir}) یکی نیست")
    else:
        ok(f"Text Domain == نام پوشه ({theme_dir})")

    for required in ("index.php", "functions.php"):
        if os.path.isfile(os.path.join(root, required)):
            ok(f"{required} موجود است")
        else:
            bad(f"{required} وجود ندارد")


def check_settings(root: str) -> None:
    print("\n[3] پنل تنظیمات")
    php = php_files(root)
    has_schema = False
    has_register = False
    for path in php:
        try:
            text = read(path)
        except OSError:
            continue
        if re.search(r"function\s+\w*settings_schema\s*\(", text):
            has_schema = True
        if "register_setting(" in text:
            has_register = True
    if has_schema:
        ok("settings_schema() پیدا شد (schema = منبع حقیقت)")
    else:
        bad("settings_schema() هیچ‌جا تعریف نشده — پنل باید schemaمحور باشد (theme-settings-standard §3)")
    if has_register:
        ok("register_setting() موجود است (Settings API)")
    else:
        bad("register_setting() وجود ندارد — ذخیره باید از Settings API انجام شود (theme-settings-standard §5)")


def check_requires(root: str) -> None:
    print("\n[4] مسیرهای require_once")
    missing = 0
    total = 0
    # خط‌های حاوی require_once/include_once و یک مسیر .php داخل نقل‌قول
    line_re = re.compile(
        r"""(?:require_once|include_once)\s*\(?\s*[^'"]*?['"]([^'"]+\.php)['"]"""
    )
    for path in php_files(root):
        rel_file = os.path.relpath(path, root)
        for line in read(path).splitlines():
            if "require_once" not in line and "include_once" not in line:
                continue
            for match in line_re.finditer(line):
                rel = match.group(1)
                if "$" in rel:  # مسیر حاوی متغیر — قابل استخراج نیست
                    continue
                # مسیرهای هستهٔ وردپرس (wp-admin/wp-includes) خارج از قالب‌اند
                if rel.startswith(("wp-admin/", "wp-includes/", "wp-content/")):
                    continue
                total += 1
                base = os.path.dirname(path)
                candidates = [
                    os.path.normpath(os.path.join(base, rel.lstrip("/"))),
                    os.path.normpath(os.path.join(root, rel.lstrip("/"))),
                    os.path.normpath(os.path.join(root, rel)),  # مثل /inc/x.php
                ]
                if not any(os.path.isfile(c) for c in candidates):
                    missing += 1
                    bad(f"require ناموجود: {rel_file} → {rel}")
    if total and not missing:
        ok(f"{total} مسیر require_once استاتیک موجود است")
    elif not total:
        warn("هیچ require_once استاتیکی پیدا نشد (بیلد بدون وابستگی؟)")


def check_abspath(root: str) -> None:
    print("\n[5] گارد ABSPATH")
    missing = []
    files = php_files(root)
    for path in files:
        head = "\n".join(read(path).splitlines()[:20])
        if "ABSPATH" not in head:
            missing.append(os.path.relpath(path, root))
    if missing:
        for rel in missing[:10]:
            bad(f"بدون گارد ABSPATH: {rel}")
        if len(missing) > 10:
            bad(f"… و {len(missing) - 10} فایل دیگر")
    else:
        ok(f"هر {len(files)} فایل PHP گارد ABSPATH دارد")


def check_duplicates(root: str) -> None:
    print("\n[6] تکراری نبودن توابع/کلاس‌های سراسری")
    func_re = re.compile(r"^function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)
    class_re = re.compile(
        r"^\s*(?:final\s+|abstract\s+)*(?:class|interface|trait)\s+([A-Za-z_][A-Za-z0-9_]*)",
        re.M,
    )
    funcs = defaultdict(list)
    classes = defaultdict(list)
    for path in php_files(root):
        text = read(path)
        rel = os.path.relpath(path, root)
        for name in func_re.findall(text):
            funcs[name].append(rel)
        for name in class_re.findall(text):
            classes[name].append(rel)
    dup_f = {k: v for k, v in funcs.items() if len(v) > 1}
    dup_c = {k: v for k, v in classes.items() if len(v) > 1}
    for name, where in dup_f.items():
        bad(f"تابع سراسری تکراری '{name}' در: {', '.join(where)} → بازتعریف = fatal")
    for name, where in dup_c.items():
        bad(f"کلاس/اینترفیس تکراری '{name}' در: {', '.join(where)}")
    if not dup_f and not dup_c:
        ok(f"{len(funcs)} تابع و {len(classes)} کلاس سراسری — بدون تکراری")


def check_forbidden(root: str, theme_dir: str) -> None:
    print("\n[7] ممنوعیت‌ها")
    if os.path.isdir(os.path.join(root, "vendor")):
        bad("پوشهٔ vendor/ وجود دارد — تیم بدون Composer کار می‌کند (باید حذف شود)")
    else:
        ok("بدون vendor/")
    if os.path.isfile(os.path.join(root, "composer.json")):
        bad("composer.json وجود دارد — ممنوع (استاندارد بدون Composer)")
    else:
        ok("بدون composer.json")

    # require بدون once
    bare = re.compile(r"(?<!include_once)(?<!require_once)\brequire\s*\(")
    for path in php_files(root):
        rel = os.path.relpath(path, root)
        if rel in ("functions.php",):
            continue
        for i, line in enumerate(read(path).splitlines(), 1):
            if bare.search(line) and "require_once" not in line:
                warn(f"require بدون _once: {rel}:{i}")

    # functions.php: فقط bootstrap
    fpath = os.path.join(root, "functions.php")
    if os.path.isfile(fpath):
        text = read(fpath)
        lines = text.splitlines()
        if len(lines) > MAX_FUNCTIONS_PHP_LINES:
            warn(f"functions.php {len(lines)} خط است (سقف نرم {MAX_FUNCTIONS_PHP_LINES}) — فقط bootstrap باشد")
        if re.search(r"^\s*function\s+\w+\s*\(", text, re.M):
            bad("functions.php تعریف تابع دارد — فقط گارد + require_once (fatal-error-prevention §2)")
        if re.search(r"^\s*(final\s+|abstract\s+)?class\s+\w+", text, re.M):
            bad("functions.php تعریف کلاس دارد — فقط bootstrap باشد")
        hooks = set(re.findall(r"add_action\(\s*['\"]([^'\"]+)['\"]", text)) | set(
            re.findall(r"add_filter\(\s*['\"]([^'\"]+)['\"]", text)
        )
        extra = hooks - ALLOWED_FUNCTIONS_PHP_HOOKS
        if extra:
            bad(f"هوک غیرمجاز در functions.php: {', '.join(sorted(extra))} — فقط admin_notices مجاز است")
        if not extra:
            ok("functions.php فقط bootstrap است (بدون هوک اضافه)")
        # گارد نسخه PHP و ABSPATH
        if "version_compare(PHP_VERSION" not in text:
            warn("گارد نسخهٔ PHP در functions.php نیست (fatal-error-prevention §2)")
        if "ABSPATH" not in text:
            bad("functions.php گارد ABSPATH ندارد")


def check_patches(root: str) -> None:
    print("\n[8] patches/ (در صورت وجود)")
    pdir = os.path.join(root, "patches")
    if not os.path.isdir(pdir):
        warn("patches/ وجود ندارد — بخش «بروزرسانی» پنل به آن نیاز دارد (theme-settings-standard §7)")
        return
    manifests = []
    root_manifest = os.path.join(pdir, "manifest.json")
    if os.path.isfile(root_manifest):
        manifests.append(root_manifest)
    for name in sorted(os.listdir(pdir)):
        candidate = os.path.join(pdir, name, "manifest.json")
        if os.path.isfile(candidate):
            manifests.append(candidate)
    if not manifests:
        bad("patches/ بدون manifest.json — هر نسخه باید manifest با sha256 داشته باشد")
        return
    for mpath in manifests:
        try:
            data = json.loads(read(mpath))
        except json.JSONDecodeError as exc:
            bad(f"manifest نامعتبر: {mpath} — {exc}")
            continue
        files = data.get("files")
        if not isinstance(files, list) or not files:
            bad(f"manifest بدون آرایهٔ files: {os.path.relpath(mpath, root)}")
            continue
        base = os.path.dirname(mpath)
        bad_hash = 0
        missing = 0
        for entry in files:
            rel = entry.get("path") if isinstance(entry, dict) else None
            if not rel:
                bad_hash += 1
                continue
            fpath = os.path.normpath(os.path.join(base, rel))
            fpath2 = os.path.normpath(os.path.join(root, rel))
            target = fpath if os.path.isfile(fpath) else (fpath2 if os.path.isfile(fpath2) else None)
            if target is None:
                missing += 1
            elif isinstance(entry, dict) and entry.get("sha256"):
                digest = hashlib.sha256(open(target, "rb").read()).hexdigest()
                if digest.lower() != str(entry["sha256"]).lower():
                    bad_hash += 1
        rel_m = os.path.relpath(mpath, root)
        if missing:
            bad(f"{rel_m}: {missing} فایل از manifest موجود نیست")
        if bad_hash:
            bad(f"{rel_m}: {bad_hash} هش sha256 نادرست/غایب")
        if not missing and not bad_hash:
            ok(f"{rel_m}: {len(files)} فایل، هش‌ها تطابق دارد")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = os.path.abspath(sys.argv[1].rstrip("/"))
    if not os.path.isdir(root):
        print(f"پوشه وجود ندارد: {root}")
        return 2
    theme_dir = os.path.basename(root)
    print(f"validate_theme — {theme_dir}")
    print("=" * 60)

    files = php_files(root)
    if not files:
        bad("هیچ فایل PHP پیدا نشد — این پوشه قالب نیست")
    else:
        check_php_lint(files)
        check_structure(root, theme_dir)
        check_settings(root)
        check_requires(root)
        check_abspath(root)
        check_duplicates(root)
        check_forbidden(root, theme_dir)
        check_patches(root)

    print("=" * 60)
    print(f"نتیجه: {len(PASSES)} PASS · {len(WARNS)} WARN · {len(FAILS)} FAIL")
    if FAILS:
        print("🔴 قرمز — قبل از تحویل، همهٔ FAILها باید صفر شوند.")
        return 1
    print("🟢 سبز — دروازهٔ validate_theme گذشت (اجرای وبسایت و تست پنل همچنان لازم است).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
