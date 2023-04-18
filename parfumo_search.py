import sys, csv, requests
from lxml import html

NAME = 0
BRAND = 1
YEAR = 2
CONCENTRATION = 3
URL = 4
MANIFEST = "manifest copy.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def print_itemized(items):
    for i in range(len(items)):
        print(f"{i}: {items[i]}")


def select_item(items, name):
    print(f"Available {name}s are:")
    print_itemized(items)
    selected = input(f"\nSelect one of the available {name}s: ")

    # Match input to one available brand
    if selected.isnumeric():
        selected = items[int(selected)]
    else:
        for item in items:
            if selected.lower() in item.lower():
                selected = item
                break
        if selected not in items:
            print(f'\n"{selected}" does not match any {name} in the list')
            return
    print(f"You selected {selected}\n")
    return items.index(selected)


def floatify(nums):
    result = []
    for num in nums:
        try:
            result.append(float(num[0]))
        except:
            result.append(None)
    return result


def search(url):
    # Go to parfumo.com for specific perfume
    page = requests.get(url, headers=HEADERS)
    tree = html.fromstring(page.content)
    page.close()

    accords = tree.xpath(
        "//div[contains(@class, 's-circle-container')]/div[contains(@class, 'text-xs')]/text()"
    )
    notes = tree.xpath("//span[@class='nowrap pointer']/text()")
    rating = tree.xpath("//span[@itemprop='ratingValue']/text()")
    scent = tree.xpath(
        "//div[@data-type='scent']/*/*/span[contains(@class, 'bold')]/text()"
    )
    longevity = tree.xpath(
        "//div[@data-type='durability']/*/*/span[contains(@class, 'bold')]/text()"
    )
    sillage = tree.xpath(
        "//div[@data-type='sillage']/*/*/span[contains(@class, 'bold')]/text()"
    )
    bottle = tree.xpath(
        "//div[@data-type='bottle']/*/*/span[contains(@class, 'bold')]/text()"
    )
    value = tree.xpath(
        "//div[@data-type='pricing']/*/*/span[contains(@class, 'bold')]/text()"
    )

    rating, scent, longevity, sillage, bottle, value = floatify(
        [rating, scent, longevity, sillage, bottle, value]
    )

    print(f"rating: {rating}, accords: {accords}, notes: {notes}")
    print(
        f"scent: {scent}, longevity: {longevity}, sillage: {sillage}, bottle: {bottle}, value: {value}"
    )

    return


def main():
    name = ""
    if len(sys.argv) > 2:
        query = sys.argv[2]
        page = requests.get(
            f'https://www.parfumo.com/s_perfumes.php?lt=1&filter={query.replace(" ", "+")}'
        )
        tree = html.fromstring(page.content)
        page.close()
        try:
            result = tree.xpath("//div[@id='s_ext_res']/*/*/a")[0].get("href")
            print(result)
            search(result)
        except:
            print("No results")
        return

    if len(sys.argv) < 2:
        while name == "":
            name = input("Input perfume name: ")
    else:
        name = sys.argv[1]

    if name[:5] == "https":
        search(name)
        return

    print("Keyword:", name, "\n")
    perfume = None
    with open(MANIFEST, "r", encoding="unicode_escape") as f:
        lines = csv.reader(f)
        next(lines)

        # Find all perfume elements that match keyword
        matches = [line for line in lines if name.lower() in line[NAME].lower()]

        # Show brands with a matching perfume
        brands = sorted(list(set([match[BRAND] for match in matches])))
        brand = brands[select_item(brands, "brand")]

        # Show matching perfumes from selected brand
        perfumes = [match for match in matches if match[BRAND] == brand]
        perfume_names = [
            f"{match[NAME]} ({match[YEAR]}) {match[CONCENTRATION]}"
            for match in perfumes
        ]
        perfume = perfumes[select_item(perfume_names, "perfume")]
        print(perfume)

    if perfume is not None:
        search(perfume[URL])


if __name__ == "__main__":
    main()
