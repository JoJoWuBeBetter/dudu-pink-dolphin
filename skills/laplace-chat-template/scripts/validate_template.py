#!/usr/bin/env python3
"""LAPLACE Chat 模版静态校验器。

用法:
    python3 validate_template.py TEMPLATE.css [--mode auto|remote|editor] [--strict] [--json]

退出码:
    0  通过（可能有警告）
    1  存在阻断性问题
    2  用法错误 / 文件不可读

检查项见 SKILL.md「硬性规则」与 references/delivery-and-metadata.md 的交付清单。
仅用标准库，无第三方依赖。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024  # 1024 KB
BASELINE_CHROMIUM = 111  # SCAS 色盘基线：Chromium > 111 / OBS > 31
LAYER_ORDER = ("template", "remote-css", "custom-css")

SEVERITY_ORDER = {"error": 0, "warn": 1, "info": 2}


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------
def strip_comments(css: str) -> str:
    """把注释替换成等长空白，保留字符串内容（用于 URL 检查）。"""
    out = []
    i, n = 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(" " * (j - i))
            i = j
        else:
            out.append(css[i])
            i += 1
    return "".join(out)


def strip_comments_and_strings(css: str) -> str:
    """注释和字符串都替换成空白（用于括号配对与选择器解析）。"""
    out = []
    i, n = 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(" " * (j - i))
            i = j
        elif css[i] in "\"'":
            quote = css[i]
            j = i + 1
            while j < n:
                if css[j] == "\\":
                    j += 2
                    continue
                if css[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(" " * (j - i))
            i = j
        else:
            out.append(css[i])
            i += 1
    return "".join(out)


def match_brace(code: str, open_idx: int) -> int:
    """返回与 open_idx 处 '{' 配对的 '}' 下标；找不到返回 len(code)-1。"""
    depth = 0
    for i in range(open_idx, len(code)):
        if code[i] == "{":
            depth += 1
        elif code[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return len(code) - 1


def scan_top_level(code: str):
    """扫描顶层结构，返回有序 item 列表。

    item = {"kind": "block"|"stmt", "header": str, "start": int, "end": int,
            "body_start": int}   # body_start 仅 block 有：'{' 之后的下标
    嵌套块整体跳过，因此这里只看到顶层。
    """
    items = []
    i, n, start = 0, len(code), 0
    while i < n:
        ch = code[i]
        if ch == "{":
            header = code[start:i].strip()
            close = match_brace(code, i)
            items.append(
                {
                    "kind": "block",
                    "header": header,
                    "start": start,
                    "end": close + 1,
                    "body_start": i + 1,
                }
            )
            i = close + 1
            start = i
            continue
        if ch == ";":
            stmt = code[start : i + 1].strip()
            if stmt:
                items.append({"kind": "stmt", "header": stmt, "start": start, "end": i + 1})
            i += 1
            start = i
            continue
        i += 1
    tail = code[start:].strip()
    if tail:
        items.append({"kind": "tail", "header": tail, "start": start, "end": n})
    return items


def layer_name(header: str) -> str:
    """从 '@layer a.b, c {' 这类 header 里取出层名（取第一个）。"""
    body = header[len("@layer") :].strip()
    body = body.split("{")[0].strip()
    if not body:
        return ""
    return body.split(",")[0].strip()


def is_at_rule(header: str, name: str) -> bool:
    return re.match(r"^@" + re.escape(name) + r"\b", header, re.I) is not None


# --------------------------------------------------------------------------
# 校验
# --------------------------------------------------------------------------
class Report:
    def __init__(self) -> None:
        self.issues: list[dict] = []

    def add(self, severity: str, code: str, message: str, hint: str = "") -> None:
        self.issues.append(
            {"severity": severity, "code": code, "message": message, "hint": hint}
        )

    @property
    def errors(self) -> list[dict]:
        return [i for i in self.issues if i["severity"] == "error"]

    @property
    def warnings(self) -> list[dict]:
        return [i for i in self.issues if i["severity"] == "warn"]


METADATA_KEYS = ("title", "author", "description", "updated", "version", "thumbnail", "features")


def parse_metadata(css: str):
    """解析文件最上方的 /* ... */ 元数据块；不含 @key 行则视为普通注释。"""
    m = re.match(r"\s*/\*(.*?)\*/", css, re.S)
    if not m:
        return None, None
    block = m.group(1)
    meta = {}
    for line in block.splitlines():
        mm = re.match(r"\s*@([A-Za-z_-]+)\s+(.*?)\s*$", line)
        if mm:
            meta[mm.group(1).lower()] = mm.group(2).strip()
    if not meta:
        return None, block
    return meta, block


def check_layer_body(body: str, layer: str, report: Report, path: str) -> None:
    """递归检查某个容器（层 / @media 等）内部是否有裸规则。"""
    for item in scan_top_level(body):
        if item["kind"] == "stmt":
            if item["header"].lower().startswith("@import"):
                report.add(
                    "error",
                    "import-in-layer",
                    f"@import 嵌套在 @layer {layer or '?'} 内",
                    "把 @import 移到文件顶部、所有 @layer 之外。",
                )
            continue
        if item["kind"] == "tail":
            if item["header"]:
                report.add(
                    "error",
                    "syntax-tail",
                    f"文件末尾有无法解析的内容：{item['header'][:60]}",
                    "检查括号是否配对、是否有漏掉的分号。",
                )
            continue

        header = item["header"]
        inner_body = body[item["body_start"] : item["end"] - 1]
        if header.lower().startswith("@layer"):
            inner = layer_name(header)
            check_layer_body(inner_body, inner, report, path)
            continue
        if re.match(r"^@(media|supports|container)\b", header, re.I):
            check_layer_body(inner_body, layer, report, path)
            continue
        if re.match(r"^@(keyframes|-webkit-keyframes|font-face|property|counter-style)\b", header, re.I):
            if not layer:
                report.add(
                    "warn",
                    "at-rule-outside-layer",
                    f"{header.split('{')[0].strip()[:40]} 位于所有 @layer 之外",
                    "放进模版层内，避免优先级被其它层盖过。",
                )
            continue

        # 普通选择器规则
        if not layer:
            report.add(
                "error",
                "naked-rule",
                f"裸规则（不在任何 @layer 内）：{header[:70]}",
                "远程模版放进 @layer remote-css，编辑器自定义 CSS 放进 @layer custom-css。",
            )


def validate(path: Path, mode: str, strict: bool) -> tuple[Report, dict]:
    report = Report()
    raw = path.read_bytes()
    size = len(raw)
    css = raw.decode("utf-8", errors="replace")

    # ---- 体积 ----
    if size > MAX_BYTES:
        report.add(
            "error",
            "size",
            f"文件 {size / 1024:.0f} KB，超过 1024 KB 上限",
            "压缩/内联素材，或把图片改为外链 HTTPS 地址。",
        )

    # ---- 括号配对 ----
    code = strip_comments_and_strings(css)
    if code.count("{") != code.count("}"):
        report.add(
            "error",
            "braces",
            f"花括号不配对：{code.count('{')} 个 '{{'，{code.count('}')} 个 '}}'",
            "补全或删除多余的括号。",
        )

    # ---- 元数据 ----
    meta, meta_block = parse_metadata(css)
    if meta is None:
        report.add(
            "error" if mode == "remote" else "info",
            "metadata-missing",
            "缺少模版元数据注释块",
            "远程模版必填；编辑器自定义 CSS 可选。在文件最上方加 /* @title ... @author ... */。",
        )
        meta = {}
    else:
        for key in ("title", "author"):
            if not meta.get(key):
                report.add(
                    "error" if mode == "remote" else "info",
                    f"metadata-{key}",
                    f"元数据缺少 @{key}",
                    "远程模版 @title 与 @author 必填。",
                )
        soft = "warn" if mode == "remote" else "info"
        if not meta.get("version"):
            report.add(soft, "metadata-version", "元数据缺少 @version", "建议用 semver，例如 1.0.0。")
        elif not re.match(r"^\d+\.\d+\.\d+", meta["version"]):
            report.add(soft, "metadata-semver", f"@version 不像 semver：{meta['version']}", "例如 1.0.0。")
        if meta.get("thumbnail") and not meta["thumbnail"].startswith("https://"):
            report.add(soft, "metadata-thumbnail", "@thumbnail 不是 HTTPS 链接", "用完整 HTTPS 地址，建议 240×192 的倍数。")
        if not meta.get("updated"):
            report.add(soft, "metadata-updated", "元数据缺少 @updated", "建议填写，便于用户判断模版新旧。")
        unknown = [k for k in meta if k not in METADATA_KEYS]
        if unknown:
            report.add("info", "metadata-unknown", f"未知元数据字段：{', '.join(sorted(unknown))}", "非标准字段会被忽略。")

    # ---- 顶层结构 ----
    items = scan_top_level(code)
    first_block_idx = next((i for i, it in enumerate(items) if it["kind"] == "block"), None)
    layers_seen: list[str] = []

    for idx, item in enumerate(items):
        if item["kind"] == "stmt":
            header = item["header"]
            low = header.lower()
            if low.startswith("@import"):
                if first_block_idx is not None and idx > first_block_idx:
                    report.add(
                        "error",
                        "import-order",
                        "@import 出现在规则之后，浏览器会忽略它",
                        "把 @import 移到文件顶部（元数据注释之后、@layer 之前）。",
                    )
            elif low.startswith("@layer") and "{" not in header:
                for name in header[len("@layer") :].rstrip(";").split(","):
                    name = name.strip()
                    if name:
                        layers_seen.append(name)
            elif low.startswith(("@charset", "@namespace")):
                pass
            else:
                report.add("warn", "top-level-stmt", f"顶层语句：{header[:60]}", "确认这是有意为之。")
            continue

        if item["kind"] == "tail":
            if item["header"]:
                report.add("error", "syntax-tail", f"文件末尾有无法解析的内容：{item['header'][:60]}", "检查括号与分号。")
            continue

        header = item["header"]
        inner_body = code[item["body_start"] : item["end"] - 1]
        if header.lower().startswith("@layer"):
            name = layer_name(header)
            if name:
                layers_seen.append(name)
            else:
                report.add("warn", "anonymous-layer", "匿名 @layer，优先级不可控", "给层起名（remote-css / custom-css）。")
            check_layer_body(inner_body, name, report, path)
            continue
        if re.match(r"^@(media|supports|container)\b", header, re.I):
            check_layer_body(inner_body, "", report, path)
            continue
        if re.match(r"^@(keyframes|-webkit-keyframes|font-face|property|counter-style)\b", header, re.I):
            report.add(
                "warn",
                "at-rule-outside-layer",
                f"{header.split('{')[0].strip()[:40]} 位于所有 @layer 之外",
                "放进模版层内。",
            )
            continue
        report.add(
            "error",
            "naked-rule",
            f"裸规则（不在任何 @layer 内）：{header[:70]}",
            "远程模版放进 @layer remote-css，编辑器自定义 CSS 放进 @layer custom-css。",
        )

    # ---- 层名是否匹配形态 ----
    expected = {"remote": "remote-css", "editor": "custom-css"}.get(mode)
    if expected and expected not in layers_seen:
        report.add(
            "error",
            "layer-missing",
            f"没有找到 @layer {expected}（发现：{', '.join(layers_seen) or '无'}）",
            f"{'远程模版' if mode == 'remote' else '编辑器自定义 CSS'} 必须写在 @layer {expected} 内。",
        )
    wrong = [n for n in layers_seen if n in LAYER_ORDER and expected and n != expected and n != "template"]
    if wrong:
        report.add(
            "warn",
            "layer-mismatch",
            f"出现非本形态的层：{', '.join(sorted(set(wrong)))}",
            "远程模版用 remote-css；编辑器自定义用 custom-css。",
        )

    # ---- URL / 素材 ----
    nocmt = strip_comments(css)
    for m in re.finditer(r"https?://[^\s'\"()]+", nocmt):
        if m.group(0).startswith("http://"):
            report.add("error", "insecure-url", f"存在 http:// 地址：{m.group(0)[:60]}", "远程模版与素材必须 HTTPS。")
    relative_assets = []
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)", nocmt, re.I):
        target = m.group(1).strip()
        if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.\-]*:", target, re.I):
            continue  # 片段引用 / 绝对 URL / data: / blob:
        if target not in relative_assets:
            relative_assets.append(target)
    if relative_assets:
        listed = "、".join(relative_assets[:5]) + ("…" if len(relative_assets) > 5 else "")
        if mode == "remote":
            report.add(
                "error",
                "relative-asset",
                f"远程模版里有 {len(relative_assets)} 个相对路径素材：{listed}",
                "改成 HTTPS 绝对地址，并放行弹幕机的 CORS 请求。",
            )
        else:
            report.add(
                "info",
                "relative-asset",
                f"{len(relative_assets)} 个相对路径素材：{listed}",
                "仅当 CSS 与 assets 同源托管时有效；分享给别人要一起部署。",
            )

    # ---- OBS 透明背景 ----
    if not re.search(r"body\s*\{[^}]*background[^}]*(transparent|rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*\))", nocmt, re.I | re.S):
        report.add(
            "warn",
            "transparent-body",
            "没有检测到 body 透明背景声明",
            "OBS 浏览器源通常需要 body { background-color: rgba(0,0,0,0); }。",
        )

    # ---- 深浅色模式写法 ----
    if re.search(r"prefers-color-scheme", nocmt, re.I):
        report.add(
            "warn",
            "color-scheme-media",
            "使用了 @media (prefers-color-scheme: dark)",
            "平台用 [data-theme=\"dark\"] 选择器切换配色，请改用它。",
        )
    if re.search(r"\[data-theme\s*=\s*[\"']?dark", nocmt, re.I):
        report.add("info", "dark-mode", "已包含 [data-theme=\"dark\"] 深色模式样式", "")

    # ---- 动效 ----
    has_motion = re.search(r"\.can-motion\b", nocmt) is not None
    has_animation = re.search(r"(^|[^-\w])animation\s*:", nocmt, re.M) is not None
    if has_animation and not has_motion:
        report.add(
            "error",
            "motion-unguarded",
            "存在 animation 但没有 .can-motion 条件类名",
            "把动画包进 .can-motion & 选择器，避免弹幕密集时动画堆积、内容不可读。",
        )
    if has_motion:
        report.add("info", "motion", "已使用 .can-motion 控制动效", "")

    # ---- 新特性兼容性（启发式） ----
    features = [
        (r"text-wrap\s*:\s*pretty", "text-wrap: pretty", 117),
        (r"@scope\b", "@scope", 118),
        (r"\blight-dark\s*\(", "light-dark()", 123),
        (r"(?<![\w-])anchor(?:-size)?\s*\(", "anchor() / anchor-size()", 125),
        (r"@starting-style\b", "@starting-style", 117),
        (r"(?<![\w-])if\s*\(", "CSS if()", 137),
        (r"oklch\s*\(", "oklch()", 111),
        (r"color-mix\s*\(", "color-mix()", 111),
        (r":has\s*\(", ":has()", 105),
    ]
    for pattern, label, version in features:
        if re.search(pattern, nocmt, re.I):
            if version > BASELINE_CHROMIUM:
                report.add(
                    "warn",
                    "feature-new",
                    f"使用了 {label}（需要 Chromium ≥ {version}）",
                    f"平台基线是 Chromium > {BASELINE_CHROMIUM} / OBS > 31，低版本会失效；提供回退或换写法。",
                )
            else:
                report.add(
                    "info",
                    "feature-baseline",
                    f"使用了 {label}（基线内）",
                    "",
                )

    # ---- 其它统计 ----
    important = len(re.findall(r"!important", nocmt, re.I))
    if important > 80:
        report.add(
            "warn",
            "important-count",
            f"!important 出现 {important} 次，偏多",
            "确认选择器是否足够精确；平台样式优先级高，但过多 !important 会让后续维护变难。",
        )
    else:
        report.add("info", "important-count", f"!important 出现 {important} 次", "")

    hover = len(re.findall(r":hover\b", nocmt))
    if hover:
        report.add(
            "warn",
            "hover",
            f"使用了 {hover} 处 :hover",
            "OBS 浏览器源没有鼠标指针，hover 效果不会触发。",
        )

    stats = {
        "file": str(path),
        "bytes": size,
        "mode": mode,
        "layers": sorted(set(layers_seen)),
        "important": important,
        "metadata": meta or {},
        "errors": len(report.errors),
        "warnings": len(report.warnings),
    }
    return report, stats


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def detect_mode(css: str) -> str:
    if re.search(r"@layer\s+remote-css\b", css):
        return "remote"
    if re.search(r"@layer\s+custom-css\b", css):
        return "editor"
    return "remote"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="LAPLACE Chat 模版静态校验器")
    parser.add_argument("path", help="待校验的 CSS 文件")
    parser.add_argument("--mode", choices=("auto", "remote", "editor"), default="auto")
    parser.add_argument("--strict", action="store_true", help="把警告也视为失败")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"找不到文件：{path}", file=sys.stderr)
        return 2

    css = path.read_text(encoding="utf-8", errors="replace")
    mode = detect_mode(css) if args.mode == "auto" else args.mode
    report, stats = validate(path, mode, args.strict)

    failed = bool(report.errors) or (args.strict and bool(report.warnings))

    if args.json:
        print(json.dumps({"stats": stats, "issues": report.issues, "ok": not failed}, ensure_ascii=False, indent=2))
    else:
        icon = {"error": "❌", "warn": "⚠️ ", "info": "ℹ️ "}
        print(f"文件：{path}")
        print(f"形态：{mode}    体积：{stats['bytes'] / 1024:.1f} KB    层：{', '.join(stats['layers']) or '无'}")
        meta = stats["metadata"]
        if meta:
            print(f"元数据：{meta.get('title', '?')} — {meta.get('author', '?')} (v{meta.get('version', '?')})")
        print("-" * 68)
        if not report.issues:
            print("✅ 没有发现问题")
        for issue in sorted(report.issues, key=lambda i: SEVERITY_ORDER[i["severity"]]):
            print(f"{icon[issue['severity']]} [{issue['code']}] {issue['message']}")
            if issue["hint"]:
                print(f"      → {issue['hint']}")
        print("-" * 68)
        print(f"结论：{len(report.errors)} 个错误，{len(report.warnings)} 个警告" + ("（strict 模式下警告也算失败）" if args.strict else ""))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
