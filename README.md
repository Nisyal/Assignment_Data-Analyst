# Binance Futures Testnet Trading Bot

A production-quality Python CLI application for placing **MARKET** and **LIMIT** orders on the **Binance USDT-M Futures Testnet**.

---

## Features

- Place **MARKET** and **LIMIT** orders (BUY / SELL)
- Full input validation with descriptive error messages
- Confirmation prompt before every order (skip with `--yes`)
- Coloured terminal output for requests and responses
- Rotating log file at `logs/app.log` (5 MB × 3 backups)
- Logs: request payload, response payload, HTTP status, exceptions, stack traces
- API secrets are **never** logged
- Clean modular architecture with separation of concerns

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # Binance Futures client wrapper
│   ├── orders.py            # Order construction and placement
│   ├── validators.py        # Input validation logic
│   ├── logging_config.py    # Rotating file + console logging
│   ├── exceptions.py        # Custom exception hierarchy
│   └── config.py            # Environment variable loading
│
├── logs/                    # Auto-created on first run
│
├── cli.py                   # CLI entry point (argparse)
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## API Key Setup

### Obtain Binance Futures Testnet credentials

1. Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with your GitHub account
3. Navigate to **API Key** in the top menu
4. Click **Generate Key** — your API Key and Secret will be displayed once
5. Copy both values immediately

### Configure your `.env` file

```bash
cp .env.example .env
```

Edit `.env`:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> ⚠️ Never commit `.env` to version control. It is already in `.gitignore`.

---

## Running Examples

### MARKET BUY order

```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### LIMIT SELL order

```bash
python cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 115000
```

### Skip confirmation prompt

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --yes
```

---

## Sample Output

```
======== ORDER REQUEST ========
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.001
  Price    : MARKET
===============================

⚠  You are about to place a BUY MARKET order:
   0.001 BTCUSDT @ MARKET PRICE
   Confirm? [y/N] y

  Sending order to Binance Futures Testnet...
  ✓  Order placed successfully!

======== ORDER RESPONSE ========
  Order ID     : 4612460891
  Status       : FILLED
  Executed Qty : 0.001
  Avg Price    : 104823.50
  Symbol       : BTCUSDT
  Timestamp    : 2026-06-30 10:42:17 UTC
=================================
```

---

## Logging

Logs are written to `logs/app.log` automatically on first run.

Each log entry includes:

```
[2026-06-30 10:42:17] [DEBUG   ] bot.orders — Order params constructed: {...}
[2026-06-30 10:42:17] [INFO    ] bot.orders — Placing BUY MARKET order — symbol: BTCUSDT | qty: 0.001
[2026-06-30 10:42:18] [DEBUG   ] bot.client — Order response received — payload: {...}
[2026-06-30 10:42:18] [INFO    ] bot.orders — Order placed successfully — order ID: 4612460891
```

Log files rotate at 5 MB with 3 backups kept (`app.log`, `app.log.1`, `app.log.2`).

---

## Assumptions

- The Binance Futures Testnet supports the same API contract as production
- `timeInForce` is set to `GTC` (Good Till Cancelled) for all LIMIT orders
- Quantity precision requirements are enforced by Binance; the bot passes the user-supplied value directly
- The `--price` argument is silently ignored for MARKET orders

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `BINANCE_API_KEY is not set` | Ensure `.env` exists and contains valid keys |
| `Binance rejected the order: [-4003]` | Quantity is below minimum lot size for the symbol |
| `Binance rejected the order: [-1121]` | Symbol does not exist on Futures Testnet |
| `Network issue connecting to Binance Testnet` | Check internet connection; Testnet may be temporarily unavailable |
| `Order cancelled by user` | Type `y` at the confirmation prompt, or pass `--yes` to skip |
