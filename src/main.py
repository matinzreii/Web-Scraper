"""
Main orchestrator for the Competitor Scraper System.

This module coordinates all components:
1. Loads competitor configurations
2. Selects appropriate scraper (static/dynamic)
3. Collects and aggregates data
4. Cleans and transforms data
5. Exports to Excel
"""

from typing import List, Dict, Any

from config import COMPETITORS, DEFAULT_SELECTORS
from src.logger_config import setup_logger
from src.static_scraper import StaticScraper
from src.dynamic_scraper import DynamicScraper
from src.data_cleaner import DataCleaner
from src.excel_exporter import ExcelExporter

logger = setup_logger(__name__)


class CompetitorScraperOrchestrator:
    """
    Orchestrates the entire competitor scraping workflow.
    """

    def __init__(self):
        """Initialize the orchestrator."""
        self.all_products: List[Dict[str, Any]] = []

    def run(self) -> None:
        """
        Execute the complete scraping workflow.
        """
        logger.info("=" * 60)
        logger.info("Starting Competitor Scraper System")
        logger.info("=" * 60)

        # Step 1: Scrape all competitors
        for comp_name, comp_config in COMPETITORS.items():
            logger.info(f"Processing competitor: {comp_name}")

            scraper = self._create_scraper(
                comp_name,
                comp_config["url"],
                comp_config.get("selectors", DEFAULT_SELECTORS),
                comp_config.get("scrape_type", "static")
            )

            products = scraper.scrape()

            # Clean up dynamic scraper resources
            if hasattr(scraper, "close"):
                scraper.close()

            self.all_products.extend(products)
            logger.info(f"Competitor {comp_name} completed: {len(products)} products")

        # Step 2: Check if any data was collected
        if not self.all_products:
            logger.warning("No data collected from any competitor")
            return

        logger.info(f"Total products collected: {len(self.all_products)}")

        # Step 3: Clean and transform data
        cleaner = DataCleaner(self.all_products)
        cleaned_df = cleaner.clean()

        # Step 4: Export to Excel
        exporter = ExcelExporter(cleaned_df)
        output_path = exporter.export()

        if output_path:
            logger.info(f"Successfully exported data to {output_path}")
        else:
            logger.error("Failed to export data")

        logger.info("=" * 60)
        logger.info("Competitor Scraper System completed")
        logger.info("=" * 60)

    def _create_scraper(self, name: str, url: str, selectors: Dict[str, str], scrape_type: str):
        """
        Factory method to create appropriate scraper instance.

        Args:
            name: Competitor name.
            url: Target URL.
            selectors: CSS selectors for extraction.
            scrape_type: 'static' or 'dynamic'.

        Returns:
            Scraper instance.
        """
        if scrape_type == "dynamic":
            return DynamicScraper(name, url, selectors)
        else:
            return StaticScraper(name, url, selectors)


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        orchestrator = CompetitorScraperOrchestrator()
        orchestrator.run()
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1