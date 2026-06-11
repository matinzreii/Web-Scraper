"""
Static web scraper using requests and BeautifulSoup.

This module handles scraping websites that render all content server-side,
making them accessible via simple HTTP requests.
"""

from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.base_scraper import BaseScraper
from config import REQUEST_TIMEOUT, USER_AGENT
from src.logger_config import setup_logger

logger = setup_logger(__name__)


class StaticScraper(BaseScraper):
    """
    Scraper for static websites using requests and BeautifulSoup.
    """

    def __init__(self, competitor_name: str, url: str, selectors: Dict[str, str]):
        """
        Initialize the static scraper.

        Args:
            competitor_name: Name of the competitor.
            url: Target URL to scrape.
            selectors: CSS selectors for data extraction.
        """
        super().__init__(competitor_name, url, selectors)
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Create a configured requests session with retry strategy.

        Returns:
            Configured requests Session object.
        """
        session = requests.Session()

        # Set default headers
        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def fetch_page(self) -> str:
        """
        Fetch HTML content using HTTP GET request.

        Returns:
            HTML content as string.

        Raises:
            requests.RequestException: If the request fails.
        """
        logger.info(f"Fetching page: {self.url}")

        response = self.session.get(self.url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"

        logger.info(f"Successfully fetched page (status: {response.status_code})")
        return response.text

    def extract_products(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract product data from HTML using CSS selectors.

        Args:
            html: HTML content to parse.

        Returns:
            List of product dictionaries.
        """
        soup = BeautifulSoup(html, "html.parser")
        products = []

        # Get the product container selector
        container_selector = self.selectors.get("product_container")
        if not container_selector:
            logger.warning("No product container selector found, using body as fallback")
            product_elements = [soup]
        else:
            product_elements = soup.select(container_selector)

        logger.info(f"Found {len(product_elements)} product elements")

        for elem in product_elements:
            product = self._extract_product_data(elem, soup)
            if product and product.get("name"):  # Only add products with at least a name
                product = self._normalize_product(product)
                products.append(product)

        return products

    def _extract_product_data(self, element: BeautifulSoup, full_soup: BeautifulSoup = None) -> Dict[str, Any]:
        """
        Extract individual product data from an HTML element.

        Args:
            element: BeautifulSoup element containing product data.
            full_soup: Full page soup for context-based extraction.

        Returns:
            Dictionary with product attributes.
        """
        product = {}

        # Define field extractors
        fields = ["name", "price", "rating", "availability"]

        for field in fields:
            selector = self.selectors.get(field)
            if selector:
                # Try to find within the product element first
                found = element.select_one(selector)
                if not found and full_soup:
                    # Fallback to full soup search
                    found = full_soup.select_one(selector)

                if found:
                    text = found.get_text(strip=True)
                    product[field] = text

        return product