"""
Base scraper class defining the interface for all scrapers.

This module contains the abstract base class that defines the contract
for all concrete scraper implementations (static and dynamic).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time

from config import REQUEST_DELAY
from src.logger_config import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers.

    Defines the interface that all concrete scraper implementations must follow.
    """

    def __init__(self, competitor_name: str, url: str, selectors: Dict[str, str]):
        """
        Initialize the scraper with competitor information.

        Args:
            competitor_name: Name of the competitor being scraped.
            url: Target URL to scrape.
            selectors: Dictionary of CSS selectors for extracting data.
        """
        self.competitor_name = competitor_name
        self.url = url
        self.selectors = selectors
        self.products = []

    @abstractmethod
    def fetch_page(self) -> str:
        """
        Fetch the HTML content of the target page.

        Returns:
            HTML content as a string.
        """
        pass

    @abstractmethod
    def extract_products(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract product information from the HTML content.

        Args:
            html: HTML content to parse.

        Returns:
            List of dictionaries containing product data.
        """
        pass