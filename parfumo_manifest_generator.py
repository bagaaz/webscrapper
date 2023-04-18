from lxml import html
import requests, sys

BRANDS_LIMIT = 1
PERFUMES_LIMIT = 1  # Max of 20 on a page
LETTERS_LIMIT = 1  # Max of 27 name categories
PAGES_LIMIT = 2
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    with open("manifest.txt", "w") as f:
        f.write("name,brand,year,concentration,url\n")
        for letter in LETTERS[:LETTERS_LIMIT]:
            print(f"Letter: {letter.upper()}\n\n")
            page1 = requests.get(
                "https://www.parfumo.com/Popular_Brands",
                headers=headers,
            )
            tree1 = html.fromstring(page1.content)
            page1.close()
            brand_urls = tree1.xpath(f"//div[@id='letter_{letter}']/div/a")
            for brand_url in brand_urls[:BRANDS_LIMIT]:
                brand_url = brand_url.get("href")

                brand_name = brand_url[33:]
                print("Brand:", brand_name, "\n")

                for page_number in range(1, PAGES_LIMIT + 1):
                    page2 = requests.get(
                        f"{brand_url}?current_page={page_number}",
                        headers=headers,
                    )
                    print(f"Page: {page_number}")
                    tree2 = html.fromstring(page2.content)
                    perfume_urls = tree2.xpath(
                        "//div[@class='col col-normal']/div[@class='image ']/a"
                    )

                    for perfume_url in perfume_urls[:PERFUMES_LIMIT]:
                        url = perfume_url.get("href")
                        page3 = requests.get(url, headers=headers)
                        tree3 = html.fromstring(page3.content)
                        name = tree3.xpath(f"//h1")[0].text.strip()
                        details = tree3.xpath(
                            f"//span[contains(@class, 'p_brand_name')]/*/span/text()"
                        ) + [None, None, None]
                        brand, year, concentration = details[:3]
                        print(
                            f"name: {name}, brand: {brand}, year: {year}, concentration: {concentration}"
                        )
                        f.write(
                            f'"{name}","{brand}",{int(year)},"{concentration}","{url}"\n'
                        )


if __name__ == "__main__":
    main()
