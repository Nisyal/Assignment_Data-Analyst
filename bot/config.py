"""Configuration loader for the trading bot.

Loads environment variables from a .env file using python-dotenv.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from bot.exceptions import ClientInitializationError

# Load .env from the project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def get_api_key() -> str:
    """Return the Binance API key from environment.

    Raises:
        ClientInitializationError: If the key is missing or empty.
    """
    key = os.getenv("BINANCE_API_KEY", "").strip()
    if not key:
        raise ClientInitializationError(
            "BINANCE_API_KEY is not set. Please add it to your .env file."
        )
    return key


def get_api_secret() -> str:
    """Return the Binance API secret from environment.

    Raises:
        ClientInitializationError: If the secret is missing or empty.
    """
    secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not secret:
        raise ClientInitializationError(
            "BINANCE_API_SECRET is not set. Please add it to your .env file."
        )
    return secret
