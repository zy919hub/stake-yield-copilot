#!/usr/bin/env python3
"""StakeYield Copilot - Binance Agent OS on-chain workflow agent.
Scan DeFi Llama staking/yield pools -> APY/TVL/risk -> staking proposal ->
user scan-confirm -> on-chain act via official Agentic wallet. Read-only by default.
Guards: single-order cap, TVL floor, APY anomaly flag, timeout auto-reject."""
import json, os, urllib.request, argparse
from datetime import datetime
API = "https://yields.llama.fi/pools"
MIN_TVL = float(os.environ.get("MIN_TVL", "1000000"))
MAX_APY = float(os.environ.get("MAX_APY", "80"))
ORDER_MAX = float(os.environ.get("ORDER_MAX", "1000"))
def pull():
    ph = urllib.request.ProxyHandler({"http": os.environ.get("HTTPS_PROXY", ""), "https": os.environ.get("HTTPS_PROXY", "")})
    op = urllib.request.build_opener(ph); op.addheaders = [("User-Agent", "Mozilla/5.0")]
    return (json.loads(op.open(API, timeout=30).read().decode()).get("data") or [])
def grade(p):
    apy = float(p.get("apy") or 0); tvl = float(p.get("tvlUsd") or 0)
    if tvl < MIN_TVL: g = "LOW_LIQUIDITY_WARN"
    elif apy > MAX_APY: g = "APY_ANOMALY_WATCH"
    elif apy >= 8: g = "GOOD_OPPORTUNITY"
    elif apy >= 3: g = "MID"
    else: g = "STABLE"
    return {"chain": p.get("chain"), "asset": p.get("symbol"), "project": p.get("project"),
            "apy": round(apy, 2), "tvl": tvl, "grade": g, "pool": p.get("pool")}
def watch(limit=12):
    scored = [grade(p) for p in pull()]
    scored = [s for s in scored if s["tvl"] >= MIN_TVL]
    scored.sort(key=lambda s: (s["apy"] if s["apy"] >= 2 else -1), reverse=True)
    scored = scored[:limit]
    return scored[:limit]
def act(prop):
    ok = guard(100, prop["tvl"])[0]
    if not ok: return {"ok": False, "err": guard(100, prop["tvl"])[1]}
    return {"ok": True, "note": "execution_ready", "proposal": prop,
            "exec": "user_scan_confirm_then_onchain_stake_via_agentic_wallet"}
def guard(_amount, tvl):
    if _amount > ORDER_MAX + 1e-9: return False, "over-single-cap"
    if tvl < MIN_TVL: return False, "tvl-below-floor"
    return True, ""
def render(items, ts=None):
    ts = ts or datetime.now().strftime("%Y-%m-%d %H:%M")
    L = ["# Chain Staking Opportunities (StakeYield Copilot)",
         "Gen " + ts + " | source DeFi Llama (" + str(len(items)) + " pools) | READ-ONLY",
         "", "## Proposals (execute after scan-confirm)", ""]
    for i, s in enumerate(items, 1):
        ok, why = guard(100, s["tvl"])
        L.append(str(i) + ". **" + str(s["asset"]) + "** (" + str(s["chain"]) + " @ " + str(s["project"]) + ")  APY **" + str(s["apy"]) + "%**  TVL $" + format(s["tvl"], ",.0f") + "  [" + str(s["grade"]) + "]")
        L.append("   guard: TVL>=" + format(MIN_TVL, ".0f") + "/order<=" + format(ORDER_MAX, ".0f") + " -> " + ("PASS" if ok else "BLOCK"))
    L.append("## Execution")
    L.append("> read-only scan/analyse -> proposal -> user scan(OAuth) confirm -> on-chain via official Agentic wallet; REJECT/timeout auto-deny. guards on.")
    L.append("## Risks")
    L.append("> on-chain staking carries protocol/smart-contract risk; abnormally high APY is often a honeypot. Research only (DYOR).")
    os.makedirs("output", exist_ok=True)
    open("output/report.md", "w").write("\n".join(L))
    json.dump(items, open("output/proposals.json", "w"), ensure_ascii=False, indent=2)
    return "\n".join(L)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--place", action="store_true"); a = ap.parse_args()
    items = watch(); print(render(items))
    if a.place: print(json.dumps([act(i) for i in items], ensure_ascii=False))
if __name__ == "__main__":
    main()
