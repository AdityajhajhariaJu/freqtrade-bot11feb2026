# freqtrade-bot11feb2026

This repository contains **both** the 1‑minute scalping engine and the 2–3h swing engine used in your Binance USDT‑M trading setup, plus supporting reports and Freqtrade `user_data`.

> **Important:** Secrets (API keys) and runtime logs are intentionally excluded from this repo.

---

## 📁 Structure

```
├── multi-strat-engine/          # Custom multi-strategy trading engine
│   ├── strategies.py            # 1m strategies + core scan/filters
│   ├── new_strategies_2h.py     # 2–3h higher‑TF strategies
│   ├── trade_loop.py            # Live execution loop (Binance futures)
│   ├── run_scan.py              # Signal‑only runner (no execution)
│   └── reports/                 # Reporting scripts (health, PnL, heatmaps, etc.)
└── user_data/                   # Freqtrade configs & sample strategies
```

---

## ✅ What’s Inside

### 1) **1‑Minute Engine (Scalp)**
- **Timeframe:** 1m
- **Goal:** frequent, short‑hold trades
- **Key filters:** confidence threshold, EMA trend alignment, confirmation (optional)
- **Strategies (examples):**
  - EMA Scalps
  - RSI Snap
  - Stoch Cross
  - Bollinger Squeeze
  - VWAP Bounce
  - MACD Flip
  - ATR Breakout
  - OBV Divergence

### 2) **2–3 Hour Engine (Swing)**
- **Timeframe:** 5m/15m aggregated from 1m
- **Goal:** higher‑conviction, fewer trades, larger TP
- **Strategies (examples):**
  - Ichimoku Cloud Breakout
  - Donchian Breakout
  - Supertrend Flip
  - Keltner Reversion
  - MTF EMA Ribbon
  - BB + Keltner Squeeze
  - VP POC Reversion
  - Pivot Bounce

---

## 🧭 Core Filters & Rules (Important)

These filters apply **after** a strategy fires. A signal must pass all of them to trade.

### 1) **Confidence Threshold**
Only signals with confidence ≥ threshold are allowed.

### 2) **Confirmation (optional)**
If enabled, the previous candle must show the **same signal direction** and also meet confidence.

### 3) **Trend EMA Alignment**
- **LONG** only if `price > EMA_fast > EMA_slow`  
- **SHORT** only if `price < EMA_fast < EMA_slow`

### 4) **Regime Filter**
If trend strength is too weak, **trend strategies are blocked** (reversion/structural can still trade).

### 5) **Cooldowns**
After a signal/trade, the pair is blocked for a cooldown period:
- 1m scalps (default ~450s)
- 2–3h strategies (default ~1200s)

### 6) **Category Cap**
Limits number of open trades per category (trend / reversion / structural). Prevents over‑exposure.

### 7) **Risk/Reward Guard**
Trades must meet minimum RR (e.g., ≥1.3) after fees/TP/SL adjustments.

### 8) **Funding Filter**
If funding is too high in the wrong direction, trades are blocked.

---

## ⚙️ Execution

### Run the live trading loop:
```bash
cd /opt/multi-strat-engine
/opt/freqtrade/.venv/bin/python trade_loop.py
```

### Run signal‑only scan (no execution):
```bash
cd /opt/multi-strat-engine
/opt/freqtrade/.venv/bin/python run_scan.py
```

---

## 🔧 Key Specifications (Current Defaults)

- **Max concurrent trades:** 8 (split 4 × 1m + 4 × 2–3h)
- **Confidence threshold (1m):** 0.66
- **Confidence threshold (2–3h):** 0.63
- **Min volatility:** 0.20%
- **Min risk‑reward:** 1.3
- **TP multiplier:** 1.20
- **Min TP:** 0.18%
- **Leverage cap:** 12

---

## 📊 Reports

Scripts in `multi-strat-engine/reports/` generate:
- Strategy PnL
- Pair performance
- Pipeline health
- Heatmaps
- TP/SL checks

> These produce CSVs which are **excluded** from git.

---

## 🔐 Secrets & Logs (Excluded)

Not committed (kept local only):
- `user_data/config*.json` (API keys)
- `user_data/freqtrade-run.log`
- `user_data/logs/`
- `reports/*.csv`
- `__pycache__/`

---

## 🔄 Strategy Tracking

Each trade is logged with **strategy name**, **side**, and **PnL**, so you can compare:
- how often each strategy triggers
- whether it’s profitable or losing

The trade‑to‑strategy mapping is done via `trade_events.csv` + `post_trade_pipeline.py`.

---

## 📌 Systemd Service (optional)

The live bot typically runs via:
```
multistrat.service
```

Logs are stored in:
```
/home/ubuntu/.openclaw/workspace/logs/multistrat.log
/home/ubuntu/.openclaw/workspace/logs/multistrat.err
```

---

If you want this README to include more detail (parameters, config tables, or strategy docs), tell me and I’ll expand it.
