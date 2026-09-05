#!/usr/bin/env python3
"""#4 StakeYield Copilot demo: 真实收益面板网页(绿橙主题). 输出 output/demo.html."""
import json, os
data = json.load(open("output/proposals.json"))
CARD = ""
for i, t in enumerate(data):
    apy = t["apy"]; tvl = t["tvl"]
    grade = t["grade"]
    col = "#e8b931" if "ANOMALY" in grade else ("#23c77a" if "GOOD" in grade else "#5a6b7b")
    CARD += f"""<div class="yc">
  <div class="yc-top"><span class="ast">{t['asset']}</span><span class="ch">{t['chain']} @ {t['project']}</span></div>
  <div class="yc-mid"><div class="apy">{apy:.2f}%</div><div class="apylab">APY</div></div>
  <div class="row"><span>TVL</span><b>${tvl:,.0f}</b></div>
  <div class="row"><span>风险</span><b style="color:{col}">{grade}</b></div>
  <div class="btns"><span class="guard">护栏 ✓</span><button style="background:#23c77a">质押 CONFIRM</button></div>
</div>"""
html = f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{box-sizing:border-box;margin:0}}body{{font-family:-apple-system,'SF Pro Display','Helvetica Neue',sans-serif;background:#0d1117;color:#e6edf3;padding:30px}}
.wrap{{max-width:1100px;margin:auto}}
.top{{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #21262d;padding:16px 0}}
.logo{{font-size:22px;font-weight:800;color:#23c77a;letter-spacing:-.5px}} .logo span{{color:#8193a5;font-weight:400}}
.tag{{font-size:12px;color:#8b98a5;background:#161b22;padding:6px 12px;border-radius:20px}}
h1{{font-size:26px;font-weight:800;margin:24px 0 6px}} .sub{{color:#8b98a5;font-size:13px;margin-bottom:20px}}
.yc{{background:#161b22;border:1px solid #21262d;border-radius:14px;padding:18px;margin-bottom:14px}}
.yc-top{{display:flex;align-items:center;gap:12px;margin-bottom:8px}}
.ast{{font-size:20px;font-weight:800;color:#58a6ff}} .ch{{color:#8b98a5;font-size:12px;margin-left:auto}}
.apy{{font-size:34px;font-weight:900;color:#23c77a}} .apylab{{color:#8b98a5;font-size:12px;margin-left:8px}}
.yc-mid{{display:flex;align-items:baseline;gap:8px;margin:6px 0}}
.row{{display:flex;justify-content:space-between;font-size:13px;margin:4px 0;color:#8b98a5}}
.row b{{color:#e6edf3}} .btns{{display:flex;align-items:center;justify-content:space-between;margin-top:12px}}
.guard{{font-size:12px;color:#8b98a5}} button{{border:none;color:#04170c;font-size:13px;font-weight:700;padding:8px 18px;border-radius:8px}}
.flow{{background:#161b22;border:1px solid #21262d;border-radius:14px;padding:16px;margin-top:10px;font-size:13px;color:#8b98a5;line-height:1.7}}
</style></head><body><div class="wrap">
<div class="top"><div class="logo">StakeYield<span> Copilot</span></div><div class="tag">Binance Agent OS · 链上工作流</div></div>
<h1>链上质押/收益机会</h1><div class="sub">只读扫描 · 用户扫码确认后执行 · 单笔上限/TVL下限/APY异常 护栏常开</div>
{CARD}
<div class="flow">流程：扫描 DeFi Llama 池 → APY/TVL/风险分级 → 质押提案 → 用户扫码(OAuth)确认 → 官方 Agentic 钱包链上执行 · REJECT/超时自动拒</div>
</div></body></html>"""
os.makedirs("output", exist_ok=True)
open("output/demo.html", "w").write(html)
print("demo.html size:", os.path.getsize("output/demo.html"))
