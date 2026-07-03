"""Custom exception classes for the trading bot."""


class TradingBotError(Exception):
    """Base exception for all trading bot errors."""
    pass


class ValidationError(TradingBotError):
    """Raised when input validation fails."""
    pass


class InvalidSymbolError(ValidationError):
    """Raised when the trading symbol is invalid."""
    pass


class InvalidQuantityError(ValidationError):
    """Raised when the order quantity is invalid."""
    pass


class InvalidSideError(ValidationError):
    """Raised when the order side is invalid."""
    pass


class InvalidOrderTypeError(ValidationError):
    """Raised when the order type is invalid."""
    pass


class MissingLimitPriceError(ValidationError):
    """Raised when a LIMIT order is placed without a price."""
    pass


class InvalidPriceError(ValidationError):
    """Raised when the limit price is invalid."""
    pass


class OrderPlacementError(TradingBotError):
    """Raised when an order fails to be placed on Binance."""
    pass


class ClientInitializationError(TradingBotError):
    """Raised when the Binance client fails to initialize."""
    pass


class NetworkError(TradingBotError):
    """Raised when a network-related error occurs."""
    pass
