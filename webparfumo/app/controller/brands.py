from model import BrandsModel
from lxml import html
import requests
import traceback
import logging
import os

class BrandsController:
    def __init__(self, database):
        self.initial_url = 'https://www.parfumo.com/brands_list.php?l='
        self.variables_url = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q','r','s','t','u','v','w','x','y','z', '0']
        self.database = database
        self.brands = BrandsModel(database)
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def getBrandsFromSite(self):
        for variable in self.variables_url:
            url = self.initial_url + variable
            self.connectBrandsPage(url)

    def getBrands(self):
        return self.brands.getBrands()

    def setBrand(self, nome, pais, url):
        self.brands.setBrand(nome, pais, url)
        return 

    def connectBrandsPage(self, url):
        try:
            headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Cookie': os.getenv('COOKIE'),
                }
            print(f"\033[1;32m -> Conectando a página de marcas da letra {url[-1]}...\033[1;32m")
            brand_page = requests.get(url, headers=headers)
            self.captureBrandsOnPage(brand_page, url)

        except Exception as e:
            error_type = type(e).__name__
            error_message = str(e)
            error_traceback = traceback.format_exc()

            print(f"\033[1;31m Error occurred! {error_type}\033[1;31m: {error_message} | {error_traceback}")
            logging.error(f"Error occurred!", exc_info=True)

    def captureBrandsOnPage(self, brand_page, url):
        tree = html.fromstring(brand_page.content)

        brands_list_html = tree.xpath(f'//div[@id="brands_{url[-1]}"]/a')

        for brand in brands_list_html:
            brand_name = brand.text_content().strip()
            brand_url = brand.attrib['href']
            try:
                brand_country = brand.xpath('.//img')[0].attrib['alt'].strip()
            except:
                brand_country = ''

            self.setBrand(brand_name, brand_country, brand_url)
            print(f"Marca: \033[1;34m{brand_name}\033[0;0m salva com sucesso!")


if __name__ == '__main__':
    print('Este arquivo não deve ser executado diretamente.')