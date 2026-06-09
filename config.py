"""
Configuration file for competitor data scraping.

This file holds all the configuration settings for the scraper,
including competitor website URLs, scraping parameters, and file paths.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Competitor websites configuration
# Format: 'competitor_name': {'url': 'https://...', 'scrape_type': 'static'/'dynamic'}
COMPETITORS = {
    "example_electronics": {
        "url": "https://www.example-electronics.com/products",
        "scrape_type": "static",
        "selectors": {
            "product_container": "div.product-item",
            "name": "h3.product-title",
            "price": "span.price",
            "rating": "div.rating span.value",
            "availability": "div.stock span"
        }
    },
    # Add more competitors here...
}

# Default selectors (fallback if competitor-specific ones are missing)
DEFAULT_SELECTORS = {
    "product_container": "div.product, div.product-item, article.product-card",
    "name": "h2, h3, .product-title, .product-name",
    "price": ".price, .product-price, [data-price]",
    "rating": ".rating, .product-rating, .stars",
    "availability": ".stock, .availability, .in-stock"
}

# Scraping settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 2))
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))

# Output settings
OUTPUT_FILE_PREFIX = "competitor_data"
EXCEL_ENGINE = "openpyxl"