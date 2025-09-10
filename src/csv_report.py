import csv


def write_csv_report(page_data, filename="report.csv"):
    if not page_data:
        print("No data to write to CSV")
        return

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "page_url",
            "h1",
            "first_paragraph",
            "outgoing_link_urls",
            "image_urls",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for page in page_data.values():
            if not page:
                continue
            outgoing_links_str = ";".join(page.get("outgoing_links", []))
            image_urls_str = ";".join(page.get("image_urls", []))

            writer.writerow(
                {
                    "page_url": page.get("url"),
                    "h1": page.get("h1"),
                    "first_paragraph": page.get("first_paragraph"),
                    "outgoing_link_urls": outgoing_links_str,
                    "image_urls": image_urls_str,
                }
            )

    print(f"Report written to {filename}")
