"""Order construction and execution for Binance Futures.

Responsible solely for assembling Binance-compatible order payloads
and delegating execution to the authenticated client instance.
"""

from typing import Any, Dict, Optional
from bot.client import BinanceFuturesClient
from bot.logging_config import get_logger

logger = get_logger(__name__)


def _assemble_payload(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
) -> Dict[str, Any]:
    """Assemble the raw Binance API parameter dict for a futures order.

    For LIMIT orders, timeInForce is set to GTC (Good Till Cancelled)
    and the price is included. For MARKET orders, price is omitted
    entirely as Binance rejects MARKET orders that include a price field.

    Args:
        symbol: Validated trading pair (e.g. BTCUSDT).
        side: BUY or SELL.
        order_type: MARKET or LIMIT.
        quantity: Validated order quantity.
        price: Validated limit price, or None for MARKET orders.

    Returns:
        A parameter dict ready for the Binance UMFutures API.
    """
    payload: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"

    logger.debug("Order payload assembled: %s", payload)
    return payload


def submit_futures_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    """Submit a validated futures order to Binance Testnet.

    Constructs the payload via _assemble_payload and delegates
    the actual HTTP call to the client's new_order method.

    Args:
        client: An authenticated BinanceFuturesClient instance.
        symbol: Validated trading pair symbol.
        side: BUY or SELL.
        order_type: MARKET or LIMIT.
        quantity: Validated order quantity.
        price: Validated limit price (None for MARKET orders).

    Returns:
        Raw API response dict from Binance on success.

    Raises:
        OrderPlacementError: Propagated from client.new_order on failure.
        NetworkError: Propagated from client.new_order on connection issues.
    """
    payload = _assemble_payload(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    logger.info(
        "Submitting %s %s — symbol: %s | qty: %s | price: %s",
        side,
        order_type,
        symbol,
        quantity,
        price if price is not None else "MARKET",
    )

    response = client.new_order(payload)

    logger.info(
        "Order accepted by Binance — ID: %s | status: %s",
        response.get("orderId"),
        response.get("status"),
    )
    return response
