# StakeYield Copilot

> 一个 **Binance Agent OS 链上工作流** Agent：扫描链上 DeFi 质押/理财池 → 算 APY/TVL/风险 → 生成**质押提案** → **用户扫码确认**后经官方 Agentic 钱包执行。
> **默认只读**；真正的链上操作（质押/赎回）必须经用户确认后才执行。

## 它能干嘛

链上收益机会到处都是，但**哪些是真的、哪些是骗你的**才是关键。StakeYield Copilot 帮你筛：

1. **扫描**：拉 DeFi Llama 上万条质押/理财池（APY / TVL / 链 / 项目）
2. **分级**：APY 异常高（>80%）标 `APY_ANOMALY_WATCH`（警惕假池）；TVL 过低标 `LOW_LIQUIDITY_WARN`
3. **护栏**：单笔上限 `ORDER_MAX_USDT`、TVL 下限 `MIN_TVL`、APY 异常提示
4. **扫码执行**：只读分析 → 质押提案 → **用户扫码(OAuth)确认** → 官方 Agentic 钱包链上执行；REJECT/超时自动拒

## 安全模型

- 只读扫描/分析为默认；变更类（质押/赎回）先过护栏 → 再进确认 → 用户批准才放行
- 护栏常开：单笔上限、TVL 下限、APY 异常提示、超时自动拒
- 模型不能"声称已执行"——如实报告确认状态

## 快速开始

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # 核心仅标准库
python3 agent.py           # 只读扫描 -> report.md + proposals.json
python3 agent.py --place   # 启用链上执行(需用户扫码+确认)
# 可选环境变量: MIN_TVL / MAX_APY / ORDER_MAX_USDT
```

## 展示

```bash
python3 make_demo.py     # 真实网页面板 -> HTML
python3 make_video.py    # 演示视频 demo.mp4
```

## 免责声明

链上质押存在协议/智能合约风险，APY 异常高多为假池。仅供研究，不构成投资建议（DYOR）。
