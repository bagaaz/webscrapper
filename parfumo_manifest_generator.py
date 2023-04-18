from lxml import html
import requests, sys

BRANDS_LIMIT = 1
PERFUMES_LIMIT = 20  # Max of 20 items on a page
LETTERS_LIMIT = 27  # Max of 27 name categories
PAGES_LIMIT = 1
LETTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
]


def main():
    # Allow access to page using python
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Will be saving information regarding all perfumes to a manifest.txt file
    # Information = name, brand, year, concentration, and url
    with open("manifest.csv", "w") as f:
        f.write("name,brand,year,concentration,url\n")

        # Check all letter categories (a-z,0)
        # This is primarily to control the volume of requests more granularly
        for letter in LETTERS[:LETTERS_LIMIT]:
            print(f"Letter: {letter.upper()}\n\n")

            # Query parfumo.com Popular Brands page to see a list of all major brands
            home_page = requests.get(
                "https://www.parfumo.com/Popular_Brands",
                headers=headers,
            )
            tree1 = html.fromstring(home_page.content)
            home_page.close()

            # Select all links to brand pages
            brand_urls = tree1.xpath(f"//div[@id='letter_{letter}']/div/a")
            for brand_url in brand_urls[:BRANDS_LIMIT]:
                brand_url = brand_url.get("href")
                print("Brand:", brand_url[33:], "\n")

                # Checking each page of brand to see all perfumes (limited to 20 per page)
                for page_number in range(1, PAGES_LIMIT + 1):
                    # Query parfumo.com for current brand
                    # Visits pages in order
                    brand_page = requests.get(
                        f"{brand_url}?current_page={page_number}",
                        headers=headers,
                    )
                    tree2 = html.fromstring(brand_page.content)

                    # Select all links to perfume pages
                    perfume_urls = tree2.xpath(
                        "//div[@class='col col-normal']/div[@class='image ']/a"
                    )

                    # Move to next brand if current one has no more pages
                    if len(perfume_urls) == 0:
                        break

                    print(f"Page: {page_number}")
                    for perfume_url in perfume_urls[:PERFUMES_LIMIT]:
                        url = perfume_url.get("href")

                        # Query parfumo.com for the current fragrance
                        perfume_page = requests.get(url, headers=headers)
                        tree3 = html.fromstring(perfume_page.content)
                        name = tree3.xpath(f"//h1")[0].text.strip()

                        # Select more information from page
                        # Missing details are padded out with ""
                        details = tree3.xpath(
                            f"//span[contains(@itemprop, 'brand')]/span/a/span/text()"
                        )
                        brand, year, *_ = details + ["", "", ""]
                        concentration, *_ = tree3.xpath(
                            f"//span[contains(@itemprop, 'brand')]/span/span/text()"
                        ) + ["", ""]
                        # Save information to csv
                        entry = ascii(
                            f'"{name}","{brand}",{year},"{concentration.rstrip()}","{url}"'
                        )[1:-1]
                        print(entry)
                        f.write(entry + "\n")


if __name__ == "__main__":
    main()
