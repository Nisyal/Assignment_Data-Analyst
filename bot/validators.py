"""Input validation for order parameters.

All validators raise descriptive exceptions from bot.exceptions
so the CLI can surface clean user-facing messages.
"""

from typing import Optional
from bot.config import VALID_SIDES, VALID_ORDER_TYPES
from bot.exceptions import (
    InvalidSymbolError,
    InvalidQuantityError,
    InvalidSideError,
    InvalidOrderTypeError,
    MissingLimitPriceError,
    InvalidPriceError,
)
from bot.logging_config import get_logger

logger = get_logger(__name__)


def validate_symbol(symbol: str) -> str:
    """Validate and normalise a trading symbol.

    Args:
        symbol: Raw symbol string from CLI input.

    Returns:
        Uppercase, stripped symbol string.

    Raises:
        InvalidSymbolError: If the symbol is empty or contains spaces.
    """
    symbol = symbol.strip().upper()
    if not symbol:
        raise InvalidSymbolError("Symbol cannot be empty.")
    if " " in symbol:
        raise InvalidSymbolError(f"Symbol '{symbol}' must not contain spaces.")
    if not symbol.isalnum():
        raise InvalidSymbolError(
            f"Symbol '{symbol}' must contain only letters and digits (e.g. BTCUSDT)."
        )
    logger.debug("Symbol validated: %s", symbol)
    return symbol


def validate_side(side: str) -> str:
    """Validate order side (BUY or SELL).

    Args:
        side: Raw side string from CLI input.

    Returns:
        Uppercase side string.

    Raises:
        InvalidSideError: If the side is not BUY or SELL.
    """
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise InvalidSideError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )
    logger.debug("Side validated: %s", side)
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type (MARKET or LIMIT).

    Args:
        order_type: Raw order type string from CLI input.

    Returns:
        Uppercase order type string.

    Raises:
        InvalidOrderTypeError: If the type is not MARKET or LIMIT.
    """
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise InvalidOrderTypeError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
    logger.debug("Order type validated: %s", order_type)
    return order_type


def validate_quantity(quantity: float) -> float:
    """Validate order quantity.

    Args:
        quantity: Quantity from CLI input.

    Returns:
        The validated quantity as a float.

    Raises:
        InvalidQuantityError: If quantity is zero, negative, or non-numeric.
    """
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise InvalidQuantityError(
            f"Quantity '{quantity}' is not a valid number."
        )
    if quantity <= 0:
        raise InvalidQuantityError(
            f"Quantity must be greater than zero. Got: {quantity}."
        )
    logger.debug("Quantity validated: %s", quantity)
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Validate limit price when required.

    Args:
        price: Price from CLI input (may be None for MARKET orders).
        order_type: The already-validated order type string.

    Returns:
        The validated price as a float, or None for MARKET orders.

    Raises:
        MissingLimitPriceError: If a LIMIT order has no price.
        InvalidPriceError: If the price is not a positive number.
    """
    if order_type == "LIMIT":
        if price is None:
            raise MissingLimitPriceError(
                "A price (--price) is required for LIMIT orders."
            )
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise InvalidPriceError(
                f"Price '{price}' is not a valid number."
            )
        if price <= 0:
            raise InvalidPriceError(
                f"Price must be greater than zero. Got: {price}."
            )
        logger.debug("Limit price validated: %s", price)
        return price

    # MARKET orders — price is ignored
    if price is not None:
        logger.debug("Price argument ignored for MARKET order.")
    return None


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
) -> dict:
    """Run all validations and return a clean parameter dict.

    Args:
        symbol: Trading pair symbol.
        side: BUY or SELL.
        order_type: MARKET or LIMIT.
        quantity: Order quantity.
        price: Limit price (required for LIMIT, ignored for MARKET).

    Returns:
        A dict of validated, normalised order parameters.
    """
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)
    validated_price = validate_price(price, validated_type)

    return {
        "symbol": validated_symbol,
        "side": validated_side,
        "order_type": validated_type,
        "quantity": validated_quantity,
        "price": validated_price,
    }
