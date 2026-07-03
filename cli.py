"""CLI entry point for the Binance Futures trading bot.

Usage examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 115000
"""

import argparse
import sys
from datetime import datetime, timezone
from typing import Optional

from bot.logging_config import setup_logging, get_logger
from bot.validators import validate_all
from bot.client import BinanceFuturesClient
from bot.orders import submit_futures_order
from bot.exceptions import TradingBotError, ValidationError

# Initialise logging before anything else
setup_logging()
logger = get_logger(__name__)

# ── ANSI colour helpers ────────────────────────────────────────────────────────

def _c(text: str, code: str) -> str:
    """Wrap text in an ANSI colour code if stdout supports it."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

def green(text: str) -> str:
    return _c(text, "32")

def red(text: str) -> str:
    return _c(text, "31")

def cyan(text: str) -> str:
    return _c(text, "36")

def yellow(text: str) -> str:
    return _c(text, "33")

def bold(text: str) -> str:
    return _c(text, "1")

# ── Display helpers ────────────────────────────────────────────────────────────

def print_request_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> None:
    """Print a formatted order request summary to stdout."""
    print()
    print(bold(cyan("======== ORDER REQUEST ========")))
    print(f"  Symbol   : {bold(symbol)}")
    print(f"  Side     : {bold(green(side) if side == 'BUY' else bold(red(side)))}")
    print(f"  Type     : {bold(order_type)}")
    print(f"  Quantity : {bold(str(quantity))}")
    print(f"  Price    : {bold(str(price)) if price else yellow('MARKET')}")
    print(bold(cyan("===============================")))
    print()


def print_response_summary(response: dict) -> None:
    """Print a formatted order response summary to stdout."""
    ts_raw = response.get("updateTime") or response.get("transactTime", 0)
    try:
        ts = datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        ts = str(ts_raw)

    avg_price = response.get("avgPrice", "N/A")
    if avg_price == "0" or avg_price == 0:
        avg_price = yellow("Pending (LIMIT)")

    print()
    print(bold(green("======== ORDER RESPONSE ========")))
    print(f"  Order ID     : {bold(str(response.get('orderId', 'N/A')))}")
    print(f"  Status       : {bold(str(response.get('status', 'N/A')))}")
    print(f"  Executed Qty : {bold(str(response.get('executedQty', 'N/A')))}")
    print(f"  Avg Price    : {bold(str(avg_price))}")
    print(f"  Symbol       : {bold(str(response.get('symbol', 'N/A')))}")
    print(f"  Timestamp    : {bold(ts)}")
    print(bold(green("=================================")))
    print()


def confirm_order(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> bool:
    """Prompt the user to confirm before placing the order (bonus UX feature).

    Returns:
        True if the user confirms, False otherwise.
    """
    side_display = green("BUY") if side == "BUY" else red("SELL")
    price_display = str(price) if price else yellow("MARKET PRICE")

    print(yellow(f"\n⚠  You are about to place a {side_display} {bold(order_type)} order:"))
    print(f"   {bold(quantity)} {symbol} @ {price_display}")
    try:
        answer = input(cyan("   Confirm? [y/N] ")).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer in {"y", "yes"}


# ── Argument parsing ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Construct and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description=bold("Binance Futures Testnet Order Placer"),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 115000\n"
        ),
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side",     required=True,  help="Order side: BUY or SELL")
    parser.add_argument("--type",     required=True,  dest="order_type", help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True,  type=float, help="Order quantity (e.g. 0.001)")
    parser.add_argument("--price",    required=False, type=float, default=None, help="Limit price (required for LIMIT orders)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    return parser


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        # Step 1 — Validate all inputs
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        print(red(f"\n✗  Validation error: {exc}\n"))
        logger.error("Validation failed: %s", exc)
        sys.exit(1)

    # Step 2 — Show request summary
    print_request_summary(
        symbol=params["symbol"],
        side=params["side"],
        order_type=params["order_type"],
        quantity=params["quantity"],
        price=params["price"],
    )

    # Step 3 — Confirmation prompt (bonus UX feature)
    if not args.yes:
        if not confirm_order(
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        ):
            print(yellow("\n  Order cancelled by user.\n"))
            sys.exit(0)

    # Step 4 — Initialise client
    try:
        client = BinanceFuturesClient()
    except TradingBotError as exc:
        print(red(f"\n✗  Client error: {exc}\n"))
        logger.error("Client initialisation failed: %s", exc)
        sys.exit(1)

    # Step 5 — Place order
    try:
        print(cyan("  Sending order to Binance Futures Testnet..."))
        response = submit_futures_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )
    except TradingBotError as exc:
        print(red(f"\n✗  Order failed: {exc}\n"))
        logger.error("Order placement failed: %s", exc)
        sys.exit(1)

    # Step 6 — Show response
    print(green("\n  ✓  Order placed successfully!"))
    print_response_summary(response)


if __name__ == "__main__":
    main()
