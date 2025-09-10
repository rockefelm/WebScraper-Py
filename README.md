# WebScraper-Py

A Python web scraping utility for extracting structured data from web pages and generating CSV reports.

## Features
- Extracts page title (`<h1>`), first paragraph, outgoing links, and image URLs from HTML.
- Handles both relative and absolute URLs.
- Robust error handling for malformed or invalid URLs/images.
- Generates a CSV report from scraped data.
- Includes comprehensive unit tests for all major functions and edge cases.

## Project Structure
```
WebScraper-Py/
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # Project documentation
├── uv.lock                  # Dependency lock file
├── src/
│   ├── crawl.py             # Core scraping logic
│   ├── csv_report.py        # CSV report generation
│   ├── test_crawl.py        # Unit tests for scraping functions
│   └── __pycache__/         # Python bytecode cache
└── __pycache__/             # Root bytecode cache
```


## Usage

### 1. Command-Line Usage
Run the main program from the `src` directory:
```bash
python main.py <base_url> [max_concurrency] [max_pages]
```

#### Arguments
- `<base_url>` (required): The website URL to start crawling from.
- `[max_concurrency]` (optional): Maximum number of concurrent requests (default: implementation default).
- `[max_pages]` (optional): Maximum number of pages to crawl (default: implementation default).

#### Examples
```bash
# Crawl a site with default concurrency and page limit
python main.py https://example.com

# Crawl with custom concurrency
python main.py https://example.com 10

# Crawl with custom concurrency and page limit
python main.py https://example.com 10 50
```

The program will output progress to the console and write a CSV report (`report.csv`) with the results.

### 2. Scraping Web Pages (API)
Use the functions in `src/crawl.py` to extract data from HTML content:
- `extract_page_data(html, page_url)` returns a dictionary with keys: `url`, `h1`, `first_paragraph`, `outgoing_links`, `image_urls`.

### 3. Generating a CSV Report (API)
Use `write_csv_report(page_data, filename="report.csv")` from `src/csv_report.py`:
- `page_data` should be a dictionary where each value is a page data dict (as returned by `extract_page_data`).
- The CSV will include columns for page URL, title, first paragraph, outgoing links, and image URLs.

### 4. Running Tests
Run all unit tests from the `src` directory:
```bash
uv run -m unittest -v
```

## Example
```python
from crawl import extract_page_data
from csv_report import write_csv_report

html = """
<html><body>
  <h1>Example</h1>
  <p>First paragraph.</p>
  <a href="/link">Link</a>
  <img src="/img.jpg">
</body></html>
"""
url = "https://example.com"
page_data = {url: extract_page_data(html, url)}
write_csv_report(page_data, filename="example_report.csv")
```

## Dependencies
- Python 3.12+
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (for HTML parsing)
- Standard library: `csv`, `unittest`, `urllib.parse`

## Error Handling
- Invalid URLs or image sources raise `ValueError` with descriptive messages.
- Empty or malformed HTML is handled gracefully.

## Contributing
Pull requests and issues are welcome!

## License
MIT License
