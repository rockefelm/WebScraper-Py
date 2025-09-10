import sys
import asyncio
from crawl import crawl_site_async
from csv_report import write_csv_report



async def main():
    
    if len(sys.argv) < 2:
        print("no website provided")
        return 1
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        return 1    
    
    base_url = sys.argv[1]
    print(f"Starting crawl of: {base_url}")
    if len(sys.argv) == 2:
        page_data = await crawl_site_async(base_url)
    elif len(sys.argv) == 3:
        max_concurrency = int(sys.argv[2])
        page_data = await crawl_site_async(base_url, max_concurrency)
    elif len(sys.argv) == 4:
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
        page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    print(f"Crawling complete. Found {len(page_data)} pages.")

    write_csv_report(page_data)

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
