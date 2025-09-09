import sys
import importlib.util

crawler_spec = importlib.util.spec_from_file_location("crawl", "./src/crawl.py")
crawler = importlib.util.module_from_spec(crawler_spec)
crawler_spec.loader.exec_module(crawler)


def main():
    
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    url = sys.argv[1]

    print(f"Starting crawl of: {url}")

    page_data = crawler.crawl_page(url)

    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")

    sys.exit(0)


if __name__ == "__main__":
    main()
