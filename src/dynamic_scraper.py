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