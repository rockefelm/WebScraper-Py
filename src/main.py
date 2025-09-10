import sys
from crawl import crawl_site_async


async def main():
    
    if len(sys.argv) < 2:
        print("no website provided")
        return 1
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        return 1
    
    base_url = sys.argv[1]

    print(f"Starting crawl of: {base_url}")

    page_data = await crawl_site_async(base_url)
    for page in page_data.values():
        url = page.get("url")
        if url:
            print(url)


if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
