#!/usr/bin/env python3
"""
anniversary-wishes-maker · P1 埋点脚本
全站新增统一 tool_complete 关键事件（GA4），不破坏现有 wish_generated / wish_copied 历史数据。

策略（锚点后追加，绝不替换/删除原行）：
  - index 类（含 wish_generated）：在 wish_generated 行后追加 tool_complete{action:'generate', recipient, milestone, tone}
  - 变体子页（含 wish_copied）：在 wish_copied 行后追加 tool_complete{action:'copy', page:'<文件标识>'}
  - calculator（含 anniversary_gift_calc / anniversary_countdown）：对应事件后各追加 tool_complete

用法：
  python add_tool_complete.py --dry     # 仅预览，不写盘
  python add_tool_complete.py           # 实际写入
"""
import re
import os
import sys
import glob

DRY = "--dry" in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = sorted(glob.glob(os.path.join(ROOT, "*.html")))


def add_after(s, pattern, new_line):
    """在第一个匹配 pattern 的 gtag 语句之后追加 new_line。返回 (new_s, count)。"""
    m = re.search(pattern, s)
    if not m:
        return s, 0
    semi = s.index(";", m.start())  # 该语句以 ; 结束
    pos = semi + 1
    return s[:pos] + "\n" + new_line + s[pos:], 1


total = 0
for f in PAGES:
    s = open(f, encoding="utf-8").read()
    pid = os.path.basename(f)[:-5].replace("-", "_")
    orig = s
    log = []

    # 1) index 生成动作
    s, c1 = add_after(
        s,
        r"gtag\('event',\s*'wish_generated',\s*\{[^}]*\}\)",
        "      gtag('event', 'tool_complete', { action: 'generate', recipient: who, milestone: milestone, tone: tone });",
    )
    if c1:
        log.append("+tool_complete[generate]")

    # 2) calculator 礼物计算（found:false / true）
    for found in ("false", "true"):
        s, c = add_after(
            s,
            r"gtag\('event',\s*'anniversary_gift_calc',\s*\{\s*year:\s*yr,\s*found:\s*%s\s*\}\)" % found,
            "      gtag('event', 'tool_complete', { action: 'gift_calc', year: yr, found: %s });" % found,
        )
        if c:
            log.append("+tool_complete[gift_calc:%s]" % found)

    # 3) calculator 倒计时
    s, c3 = add_after(
        s,
        r"gtag\('event',\s*'anniversary_countdown',\s*\{\}\)",
        "      gtag('event', 'tool_complete', { action: 'countdown' });",
    )
    if c3:
        log.append("+tool_complete[countdown]")

    # 4) 复制动作（index + 全部变体子页，每页 1 处）
    s, c4 = add_after(
        s,
        r"gtag\('event',\s*'wish_copied',\s*\{\}\)",
        "      gtag('event', 'tool_complete', { action: 'copy', page: '%s' });" % pid,
    )
    if c4:
        log.append("+tool_complete[copy:%s]" % pid)

    if s != orig:
        total += 1
        if DRY:
            print("[DRY]  %s : %s" % (os.path.basename(f), ", ".join(log)))
        else:
            open(f, "w", encoding="utf-8").write(s)
            print("[WRITE] %s : %s" % (os.path.basename(f), ", ".join(log)))

print("\nTotal changed: %d / %d" % (total, len(PAGES)))
