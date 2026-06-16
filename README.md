
# 🕸️ Competitor Scraper – Web Scraping for Market Intelligence

A **production‑grade** web scraping system that extracts competitor product data (prices, ratings, availability) from both static and dynamic websites, cleans the data, and exports it to a professionally formatted Excel file.

---

## 🚀 Key Features

- 🌐 **Handles Both Static & Dynamic Content** – Uses `requests` + `BeautifulSoup` for static sites and `Selenium` for JavaScript‑rendered pages
- 🧹 **Automated Data Cleaning** – Removes duplicates, normalizes prices/ratings, standardizes availability status
- 📊 **Professional Excel Export** – Auto‑adjusted columns, color‑coded headers, summary sheet with key metrics
- 🛡️ **Ethical Scraping** – Configurable delays, user‑agent rotation, retry logic
- 📝 **Structured JSON Logging** – Easy integration with log aggregation tools
- 🔧 **Modular & Maintainable** – Separate classes for scraping, cleaning, and exporting

---

## 📦 Prerequisites

- Python 3.9 or higher
- Chrome browser (for dynamic scraping with Selenium)
- Git (optional, for cloning)

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/competitor-scraper.git
   cd competitor-scraper

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env if you want to customize timeouts or user-agent
   ```

---

## ⚙️ Configuration

Edit `config.py` to add your competitors:

```python
COMPETITORS = {
    "example_store": {
        "url": "https://www.example.com/products",
        "scrape_type": "static",  # or "dynamic" for JavaScript-rendered pages
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
```

### Selector Tips

- Use **CSS selectors** (e.g., `div.product`, `.price`, `#main-content`)
- Test your selectors using browser Developer Tools (F12 → Elements tab)
- For dynamic sites, ensure selectors target elements that exist after JavaScript loads

---

## ▶️ Usage

Run the scraper:

```bash
python run.py
```

### Sample Output (JSON Log)

```json
{"timestamp": "2025-01-15 10:30:45", "level": "INFO", "logger": "src.main", "message": "Starting Competitor Scraper System"}
{"timestamp": "...", "level": "INFO", "message": "Processing competitor: example_store"}
{"timestamp": "...", "level": "INFO", "message": "Successfully scraped 24 products from example_store"}
{"timestamp": "...", "level": "INFO", "message": "Total products collected: 24"}
{"timestamp": "...", "level": "INFO", "message": "Excel file saved: output/competitor_data_20250115_103045.xlsx"}
```

### Output Location

Excel files are saved in the `output/` directory with timestamped filenames:

```
output/
├── competitor_data_20250115_103045.xlsx
├── competitor_data_20250116_142200.xlsx
└── ...
```

---

## 📁 Project Structure

```
competitor-scraper/
├── config.py                 # Configuration (competitors, selectors, paths)
├── run.py                    # Entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Files to exclude from Git
├── logs/                    # Log files directory
│   └── scraper_20250115_103045.log
├── output/                  # Excel output directory
│   └── competitor_data_*.xlsx
└── src/
    ├── __init__.py          # Package marker
    ├── main.py              # Orchestrator (coordinates all modules)
    ├── base_scraper.py      # Abstract base class for all scrapers
    ├── static_scraper.py    # Requests + BeautifulSoup implementation
    ├── dynamic_scraper.py   # Selenium WebDriver implementation
    ├── data_cleaner.py      # Pandas-based data cleaning pipeline
    ├── excel_exporter.py    # OpenPyXL formatting and export
    └── logger_config.py     # Structured JSON logging setup
```

---

## 📊 Excel Output Features

The exported Excel file includes:

### Sheet 1: "Competitor Data"
- **Raw cleaned data** with columns: `name`, `price`, `price_numeric`, `rating`, `rating_normalized`, `availability`, `availability_standardized`, `competitor_name`, `scrape_timestamp`
- **Auto‑adjusted column widths** for easy reading
- **Color‑coded headers** (blue with white text)
- **Number formatting** (currency for prices, decimals for ratings)
- **Filter‑enabled tables** for quick analysis

### Sheet 2: "Summary"
- Key metrics:
  - Total products scraped
  - Unique competitors
  - Products with valid prices
  - Average price (numeric only)
  - Average rating (normalized to 0‑5 scale)
  - In‑stock vs. Out‑of‑stock counts
  - Scrape timestamp

---

## 🧪 Testing the Scraper

### Test Static Scraper (with example)
```python
from src.static_scraper import StaticScraper

scraper = StaticScraper("test", "https://example.com", {"name": "h1"})
html = scraper.fetch_page()
products = scraper.extract_products(html)
print(f"Found {len(products)} products")
```

### Test Dynamic Scraper (with example)
```python
from src.dynamic_scraper import DynamicScraper

scraper = DynamicScraper("test", "https://example.com", {"name": "h1"})
html = scraper.fetch_page()
products = scraper.extract_products(html)
scraper.close()
print(f"Found {len(products)} products")
```

---

## ⚠️ Ethical Scraping Guidelines

- ✅ Always check `robots.txt` (e.g., `https://example.com/robots.txt`)
- ✅ Implement reasonable delays between requests (default: 2 seconds)
- ✅ Identify your scraper with a custom User‑Agent
- ❌ Do NOT overload the target server (use delays)
- ❌ Do NOT scrape personal or sensitive data
- ❌ Do NOT bypass rate‑limiting or anti‑scraping mechanisms

---

## 🐛 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"No module named 'selenium'"** | Run `pip install -r requirements.txt` |
| **ChromeDriver not found** | The `webdriver-manager` package automatically downloads and manages ChromeDriver. Ensure you have an internet connection. |
| **Page loads but no products found** | Check your CSS selectors. Use browser DevTools to verify. The site might be dynamic — try switching to `"scrape_type": "dynamic"`. |
| **SSL Certificate error** | Add `verify=False` to `requests.get()` (for testing only). |
| **Excel file not created** | Check if the `output/` directory exists. The system creates it automatically. |

---

## 🔄 Future Improvements

- [ ] Add proxy rotation for large‑scale scraping
- [ ] Implement data export to CSV and JSON formats
- [ ] Add email notifications on scrape completion
- [ ] Schedule regular scraping with cron jobs
- [ ] Add unit tests and CI/CD pipeline

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "feat: add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---



---

## 🙏 Acknowledgements

- [Requests](https://docs.python-requests.org/) – HTTP library for Python
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – HTML parsing library
- [Selenium](https://www.selenium.dev/) – Browser automation framework
- [Pandas](https://pandas.pydata.org/) – Data manipulation library
- [OpenPyXL](https://openpyxl.readthedocs.io/) – Excel file library

---


## 👤 Author

**[Matin Zarei]**
*2026*
**Happy scraping! 🕸️📊**
---


> ⭐ If you found this project useful or interesting, feel free to star the repository.

