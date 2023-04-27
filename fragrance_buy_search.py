import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL = "https://fragrancebuy.ca/pages/search-results?q="


def main():
    if len(sys.argv) < 2:
        print("Usage: py fragrance_buy_search.py <query>")
        return
    query = " ".join(sys.argv[1:])

    # Selenium options
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    search_query(query, options)


def search_query(query, options):
    # Query search
    driver = webdriver.Chrome(options=options)
    print(URL + query)
    driver.get(URL + query)

    # Select first linked element (can expand to others if needed)
    elements = driver.find_elements(By.CSS_SELECTOR, ".isp_product_image_href")
    links = [a.get_attribute("href") for a in elements]

    search_product(links[0], options)


def search_product(url, options):
    # Visit specific product page
    driver = webdriver.Chrome(options=options)
    print(url)
    driver.get(url)

    # Save information about variants
    elements = driver.find_elements(By.CSS_SELECTOR, "#variant_selector a")
    variants = [
        {
            "price": float(a.get_attribute("data-variant-price")[19:-11]),
            "currency": a.get_attribute("data-variant-price")[-10:-7],
            "available": a.get_attribute("data-variant-available") == "true",
            "size": a.get_attribute("innerText"),
        }
        for a in elements
    ]
    available = [variant for variant in variants if variant["available"]]
    not_available = [variant for variant in variants if not variant["available"]]

    print("\nNot in Stock:")
    for variant in not_available:
        print(f'{variant["size"]}')

    print("\nAvailable:")
    for variant in available:
        print(f'{variant["size"]}: {variant["price"]} {variant["currency"]}')


if __name__ == "__main__":
    main()
