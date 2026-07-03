"""Authenticated Binance USDT-M Futures Testnet client.

Wraps the binance-futures-connector UMFutures class with structured
per-request logging, secret-safe error reporting, and a clean exception
surface that the rest of the application depends on.
"""

from typing import Any, Dict
from binance.um_futures import UMFutures
from binance.error import ClientError, ServerError
from bot.config import get_api_key, get_api_secret, BINANCE_TESTNET_BASE_URL
from bot.exceptions import (
    ClientInitializationError,
    NetworkError,
    OrderPlacementError,
)
from bot.logging_config import get_logger

logger = get_logger(__name__)


class BinanceFuturesClient:
    """Thin, testnet-targeted wrapper around UMFutures.

    Owns authentication, base URL configuration, and the translation
    of SDK-level exceptions into the project's own exception hierarchy.
    All response bodies are logged at DEBUG level; no API secret is
    ever included in log output.
    """

    def __init__(self) -> None:
        """Instantiate and authenticate the UMFutures client.

        Reads credentials from environment via config module.

        Raises:
            ClientInitializationError: If credentials are absent or
                the underlying SDK raises during construction.
        """
        try:
            self._client = UMFutures(
                key=get_api_key(),
                secret=get_api_secret(),
                base_url=BINANCE_TESTNET_BASE_URL,
            )
            logger.info(
                "Binance Futures Testnet client ready — base URL: %s",
                BINANCE_TESTNET_BASE_URL,
            )
        except ClientInitializationError:
            raise
        except Exception as exc:
            logger.exception("Unexpected failure during Binance client setup.")
            raise ClientInitializationError(
                f"Could not initialise Binance client: {exc}"
            ) from exc

    def new_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Forward an order payload to the Binance Futures REST API.

        Logs the outbound payload and the inbound response at DEBUG
        level. Translates ClientError, ServerError, and network-level
        errors into the project's exception hierarchy so callers have
        a single, consistent error surface.

        Args:
            params: A Binance-compatible order parameter dict produced
                by orders._assemble_payload().

        Returns:
            The Binance API response dict on success.

        Raises:
            OrderPlacementError: On ClientError or ServerError from Binance.
            NetworkError: On connection or timeout failures.
        """
        logger.debug("Outbound order payload → %s", params)

        try:
            response: Dict[str, Any] = self._client.new_order(**params)
            logger.debug("Inbound order response ← %s", response)
            return response

        except ClientError as exc:
            logger.error(
                "Binance rejected the request — HTTP %s | code %s | %s",
                exc.status_code,
                exc.error_code,
                exc.error_message,
            )
            raise OrderPlacementError(
                f"Binance API error [{exc.error_code}]: {exc.error_message}"
            ) from exc

        except ServerError as exc:
            logger.error("Binance server-side error — %s", exc)
            raise OrderPlacementError(f"Binance server error: {exc}") from exc

        except (ConnectionError, TimeoutError) as exc:
            logger.error("Network failure reaching Binance Testnet — %s", exc)
            raise NetworkError(
                f"Could not reach Binance Testnet ({type(exc).__name__}): {exc}"
            ) from exc

        except Exception as exc:
            logger.exception("Unhandled exception during order submission.")
            raise OrderPlacementError(
                f"Unexpected error during order submission: {exc}"
            ) from exc
