import requests

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if response.status_code > 399:
        raise ValueError(f"URL returned status code {response.status_code}")
    if response.headers["Content-Type"] != "text/html":
        raise ValueError("URL did not return HTML content")
    response.raise_for_status()
    return response.text