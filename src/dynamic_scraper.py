"""
Dynamic web scraper using Selenium for JavaScript-rendered pages.

This module handles websites that load content dynamically via JavaScript,
requiring a real browser to render the page before extraction.
"""

from typing import List, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from src.base_scraper import BaseScraper
from config import HEADLESS_MODE, PAGE_LOAD_TIMEOUT
from src.logger_config import setup_logger

logger = setup_logger(__name__)


class DynamicScraper(BaseScraper):
    """
    Scraper for dynamic websites using Selenium WebDriver.
    """

    def __init__(self, competitor_name: str, url: str, selectors: Dict[str, str]):
        """
        Initialize the dynamic scraper.

        Args:
            competitor_name: Name of the competitor.
            url: Target URL to scrape.
            selectors: CSS selectors for data extraction.
        """
        super().__init__(competitor_name, url, selectors)
        self.driver = None

    def _create_driver(self) -> webdriver.Chrome:
        """
        Create and configure a Chrome WebDriver instance.

        Returns:
            Configured Chrome WebDriver.
        """
        chrome_options = Options()

        if HEADLESS_MODE:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={USER_AGENT}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

        return driver

    def fetch_page(self) -> str:
        """
        Fetch page content using Selenium (renders JavaScript).

        Returns:
            Rendered HTML content as string.
        """
        logger.info(f"Loading dynamic page: {self.url}")

        self.driver = self._create_driver()
        self.driver.get(self.url)

        # Wait for body to be present
        WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Optional: wait for specific elements if selectors are provided
        container_selector = self.selectors.get("product_container")
        if container_selector:
            try:
                WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, container_selector))
                )
                logger.info(f"Product container found with selector: {container_selector}")
            except TimeoutException:
                logger.warning(f"Product container not found: {container_selector}")

        html = self.driver.page_source
        logger.info("Successfully fetched rendered page")
        return html

    def extract_products(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract product data using BeautifulSoup (parsing the rendered HTML).

        Since the HTML is already rendered, we reuse the BeautifulSoup-based
        extraction logic from the static scraper for consistency.

        Args:
            html: Rendered HTML content.

        Returns:
            List of product dictionaries.
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        products = []

        container_selector = self.selectors.get("product_container")
        if container_selector:
            product_elements = soup.select(container_selector)
        else:
            product_elements = [soup]

        logger.info(f"Found {len(product_elements)} product elements")

        for elem in product_elements:
            product = self._extract_product_data(elem, soup)
            if product and product.get("name"):
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
        fields = ["name", "price", "rating", "availability"]

        for field in fields:
            selector = self.selectors.get(field)
            if selector:
                found = element.select_one(selector)
                if not found and full_soup:
                    found = full_soup.select_one(selector)

                if found:
                    text = found.get_text(strip=True)
                    product[field] = text

        return product

    def close(self):
        """
        Close the WebDriver and clean up resources.
        """
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")