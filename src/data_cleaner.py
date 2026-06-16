"""
Data cleaning and transformation module.

This module handles cleaning, standardizing, and transforming scraped data
into a structured format suitable for analysis and export.
"""

import re
from typing import List, Dict, Any

import pandas as pd

from src.logger_config import setup_logger

logger = setup_logger(__name__)


class DataCleaner:
    """
    Clean and transform scraped product data.
    """

    def __init__(self, raw_data: List[Dict[str, Any]]):
        """
        Initialize the cleaner with raw scraped data.

        Args:
            raw_data: List of dictionaries containing raw product data.
        """
        self.raw_data = raw_data
        self.df = None

    def clean(self) -> pd.DataFrame:
        """
        Execute the complete data cleaning pipeline.

        Returns:
            Cleaned pandas DataFrame.
        """
        logger.info(f"Starting data cleaning for {len(self.raw_data)} records")

        # Convert to DataFrame
        self.df = pd.DataFrame(self.raw_data)

        if self.df.empty:
            logger.warning("No data to clean")
            return self.df

        # Apply cleaning steps
        self._remove_duplicates()
        self._handle_missing_values()
        self._clean_price_column()
        self._clean_rating_column()
        self._standardize_availability()
        self._clean_text_columns()

        logger.info(f"Data cleaning complete. Final shape: {self.df.shape}")
        return self.df

    def _remove_duplicates(self):
        """
        Remove duplicate rows based on product name and competitor.
        """
        initial_count = len(self.df)
        if "name" in self.df.columns:
            self.df = self.df.drop_duplicates(subset=["name", "competitor_name"], keep="first")
            removed = initial_count - len(self.df)
            if removed > 0:
                logger.info(f"Removed {removed} duplicate records")

    def _handle_missing_values(self):
        """
        Handle missing values in the dataset.
        """
        missing_before = self.df.isnull().sum().sum()
        logger.info(f"Missing values before handling: {missing_before}")

        # Fill missing names with placeholder
        if "name" in self.df.columns:
            self.df["name"] = self.df["name"].fillna("Unknown Product")

        # Fill missing prices with placeholder
        if "price" in self.df.columns:
            self.df["price"] = self.df["price"].fillna("N/A")

        # Fill missing ratings with 0
        if "rating" in self.df.columns:
            self.df["rating"] = self.df["rating"].fillna(0)

        # Fill missing availability with "Unknown"
        if "availability" in self.df.columns:
            self.df["availability"] = self.df["availability"].fillna("Unknown")

        missing_after = self.df.isnull().sum().sum()
        logger.info(f"Missing values after handling: {missing_after}")

    def _clean_price_column(self):
        """
        Standardize price column by extracting numeric values.
        """
        if "price" not in self.df.columns:
            return

        def extract_price(price_str):
            if pd.isna(price_str) or price_str == "N/A":
                return "N/A"
            # Extract numbers, decimals, and currency symbols
            # Keep original as string for now, but extract numeric for analysis
            numbers = re.findall(r"[\d,]+\.?\d*", str(price_str))
            if numbers:
                # Remove commas and convert to float
                clean_num = numbers[0].replace(",", "")
                try:
                    return float(clean_num)
                except ValueError:
                    return price_str
            return price_str

        # Create a numeric price column for analysis
        self.df["price_numeric"] = self.df["price"].apply(extract_price)

        # Convert to numeric where possible
        self.df["price_numeric"] = pd.to_numeric(self.df["price_numeric"], errors="coerce")

        logger.info(f"Price column cleaned. Numeric prices: {self.df['price_numeric'].notna().sum()}")

    def _clean_rating_column(self):
        """
        Standardize rating column to numeric values (0-5 scale).
        """
        if "rating" not in self.df.columns:
            return

        def normalize_rating(rating):
            if pd.isna(rating) or rating == 0:
                return None
            try:
                # Handle ratings that are out of 5, 10, or 100
                rating_str = str(rating).strip()
                # Extract numeric value
                num_match = re.search(r"(\d+(?:\.\d+)?)", rating_str)
                if not num_match:
                    return None
                num = float(num_match.group(1))

                # Normalize to 0-5 scale based on range
                if num > 5 and num <= 10:
                    return num / 2
                elif num > 10 and num <= 100:
                    return num / 20
                elif num > 5:
                    return 5
                return round(num, 1)
            except (ValueError, TypeError):
                return None

        self.df["rating_normalized"] = self.df["rating"].apply(normalize_rating)
        logger.info(f"Rating column cleaned. Normalized ratings available.")

    def _standardize_availability(self):
        """
        Standardize availability status to categorical values.
        """
        if "availability" not in self.df.columns:
            return

        def standardize(status):
            if pd.isna(status) or status == "Unknown":
                return "Unknown"
            status_lower = str(status).lower()
            if any(word in status_lower for word in ["in stock", "available", "in-stock", "instock"]):
                return "In Stock"
            elif any(word in status_lower for word in ["out of stock", "unavailable", "sold out"]):
                return "Out of Stock"
            elif any(word in status_lower for word in ["pre-order", "preorder"]):
                return "Pre-order"
            else:
                return status

        self.df["availability_standardized"] = self.df["availability"].apply(standardize)
        logger.info("Availability standardized")

    def _clean_text_columns(self):
        """
        Clean text columns by removing extra whitespace and normalizing.
        """
        text_columns = ["name", "competitor_name"]

        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()
                # Remove multiple spaces
                self.df[col] = self.df[col].str.replace(r"\s+", " ", regex=True)

        logger.info("Text columns cleaned")