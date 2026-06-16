#!/usr/bin/env python3
"""
Entry point for the Competitor Scraper System.

This script initializes and runs the competitor data collection workflow.
"""

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())