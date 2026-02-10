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

## 🔧 Configuration Table (Current Defaults)

| Parameter | 1m Engine | 2–3h Engine | Notes |
|---|---:|---:|---|
| max_concurrent_trades | 8 | 8 | split by caps below |
| max_1m_trades | 4 | – | 1m slot cap |
| max_2h_trades | – | 4 | 2–3h slot cap |
| confidence_threshold | 0.66 | 0.63 | signal quality gate |
| confirm_signal | True | False | 2–3h skips confirmation |
| min_volatility_pct | 0.002 | 0.006 | requires stronger move for 2–3h |
| tp_multiplier | 1.20 | 1.10 | scale TP size |
| min_tp_percent | 0.0018 | 0.005 | 0.18% vs 0.5% |
| min_sl_percent | – | 0.003 | 2–3h uses wider minimum stop |
| min_risk_reward | 1.3 | 1.5 | RR after fees |
| max_funding_long/short | 0.0005 | 0.0005 | funding filter |
| cooldown_sec | 450 | 1200 | per‑pair cooldown |
| post_close_cooldown_sec | 600 | 1800 | block re‑entry after close |
| leverage cap | 12 | 12 | enforced globally |

---

## 📌 Strategy List (Complete)

### 1m Strategies
| ID | Name | Type | TF | Typical Hold |
|---|---|---|---|---|
| ema_scalp | EMA 3/8 Scalp | Trend | 1m | 10–20m |
| rsi_snap | RSI Snap Reversal | Reversion | 1m | 10–15m |
| bb_squeeze | Bollinger Squeeze Breakout | Structural | 1m | 15–20m |
| macd_flip | MACD Histogram Flip | Trend | 1m | 15–20m |
| vwap_bounce | VWAP Bounce Scalp | Structural | 1m | 10–15m |
| stoch_cross | Stochastic Cross | Reversion | 1m | 8–12m |
| atr_breakout | ATR Volatility Breakout | Trend | 1m | 15–20m |
| triple_ema | Triple EMA Trend | Trend | 1m | 15–20m |
| engulfing_sr | Engulfing S/R | Structural | 1m | 10–15m |
| obv_divergence | OBV Divergence | Reversion | 1m | 10–15m |
| funding_fade | Funding Fade Reversion | Structural | 1m | 2–4h |
| liquidation_cascade | Liquidation Cascade (Proxy) | Trend | 1m | 1–2h |

### 2–3h Strategies
| ID | Name | Type | TF | Typical Hold |
|---|---|---|---|---|
| ichimoku_cloud | Ichimoku Cloud Breakout | Trend | 5m | 2–4h |
| keltner_reversion | Keltner Channel Reversion | Reversion | 5m | 1–3h |
| donchian_breakout | Donchian Breakout | Trend | 5m | 2–4h |
| supertrend_flip | Supertrend Flip | Trend | 5m | 1–3h |
| adx_di_cross | ADX DI Crossover | Trend | 5m | 1–3h |
| fib_pullback | Fibonacci Pullback | Structural | 5m | 2–3h |
| cmf_divergence | CMF Divergence | Reversion | 5m | 1–3h |
| vp_poc_reversion | VP POC Reversion | Reversion | 15m | 1–3h |
| pivot_bounce | Pivot Bounce | Structural | 5m | 1–2h |
| vwap_sd_reversion | VWAP SD Reversion | Reversion | 5m | 1–2h |
| mtf_ema_ribbon | Multi‑TF EMA Ribbon | Trend | 5m+15m | 2–4h |
| bb_kc_squeeze | BB + Keltner Squeeze | Structural | 5m | 2–4h |

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

If you want this README to include more detail (parameter values, examples, or strategy docs), tell me and I’ll expand it.
