from abc import ABC, abstractmethod


class MarketDataProvider(ABC):
    """Interface for market-data providers used by FreedomIQ."""

    @abstractmethod
    def get_latest_close(self, ticker: str) -> float | None:
        """Return the latest closing price for a ticker."""
        raise NotImplementedError