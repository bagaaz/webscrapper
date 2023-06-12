from lxml import html
import requests
import traceback
import logging

class Brands:
    def __init__(self):
        self.initial_url = 'https://www.parfumo.com/brands_list.php?l='
        self.variables_url = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q','r','s','t','u','v','w','x','y','z', '0']
        self.brands = []

        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def get_brands(self, save_to_file=False):
        for letter_url in self.variables_url:
            self.get_brands_on_page(self.initial_url + letter_url)

        if save_to_file:
            self.save_brands()

        return self.brands

    def get_brands_on_page(self, url):
        try: 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': 'PHPSESSID=6umbjqtc7ljs0bifvpfhj9leda; _ga_47SHE0CVWT=GS1.1.1683834598.1.1.1683834747.0.0.0; _ga=GA1.1.1304156602.1683834599; _sp_enable_dfp_personalized_ads=true; consentUUID=0e1c0df6-d050-4361-ad57-95bf2f91f52f_19; euconsent-v2=CPrmeAAPrmeAAAGABCENDDCsAP_AAAAAAAKIIsgZ5D5cTWFBeXx7QPs0eYwf11ARJmAiCgKAA6ABSDIAcLQEkmASMAyAAAACAAQEIBIBAAAkCAEEAEAQQIgAABHkAgAEhAAIICBEABERAAAACAIKCAAAAQAIAAARIgAAmQCAQ0LmRFQAgIAQJAAAgIgAAAAFAgMAAAAAAAIAAAAAgAAAAQAAAAAAAAACAAABIJAkAAWABUADIAHIAPABAADQAHkARABFACYAE8AN4AcwA_ACEAENAIgAiQBHACWAE0AKUAW4Aw4B-AH6AQMAjgBJgCUgGKANwAcQBIgCkQF5gMkAZcA1gIAJABIADIAH4AfwBzgI9ASsAuoBkIaAQAFwAQwA_ACCgEmALQAkQBSIYACAdQRAFAEMAPwAkwCRAFIiAAIAJB0DEABYAFQAMgAcgA-AEAANAAeAA-gCIAIoATAAnwBcAF0AMQAZgA3gBzAD8AIaARABEgCWAE0AKUAWIAtwBhgDRgH4AfoBAwCLQEcAR0AkwBKQC0AGKANwAcQA5wB1AD7AIvASIAvMBfQDJAGWAMuAaqA1gCDQ4AmABcAEgAMgAfgBoAD-AI4AZoA5wB3AEFAIQAYEA14CPQErAJiAXUAyElAaAAWABkADgAHwAeABEACYAFwAMQAZgBDQCIAIkARwApQBbgD8AI4AWgAxQBuADqAIvASIAvMBlgDWCQAkAC4AuQBmgDuANeAdsA-wCPQErCoAwATAAuACOAI4AWgBeYoAEAQUBHoyAIAEwARwBHAF5jAAICPSEBIABYAGQAmABcADEAGYAN4AjgBSgCxAI4ASkAtABigDnAHUASIA1UgAIADQAH8AZoA5wCCgHbAR6AmIpAkAAWABUADIAHIAPgBAADQAHkARABFACYAE8AKQAYgAzABzAD8AIaARABEgClAFiALcAaMA_AD9AItARwBHQCUgGKANwAfYBF4CRAF5gL6AZIAywBlwDWCgBAAC4AJAAZAA_ADaAH8ARwAuQBmgDnAHcAXUA14B2wEegJiA.YAAAAAAAAAAA; user_id=282285; last_login=1683834739; user_id_key=b89cf5ee67a173a207e7ef8a4c9cbc1e; m7er8padf9=%5B%22QmFnYWF6%22%5D; xbb2mysql_data=N%3B',

            }

            brand_page = requests.get(url, headers=headers)
            tree = html.fromstring(brand_page.content)

            brands_list_html = tree.xpath(f'//div[@id="brands_{url[-1]}"]/a')

            for brand in brands_list_html:
                brand_name = brand.text_content().strip()
                brand_url = brand.attrib['href']
                try:
                    brand_country = brand.xpath('.//img')[0].attrib['alt'].strip()
                except:
                    brand_country = ''

                self.brands.append({
                    'name': brand_name,
                    'url': brand_url,
                    'country': brand_country
                })

                print(f"Marca: \033[1;34m{brand_name}\033[0;0m salva com sucesso!")

        except Exception as e:
                error_type = type(e).__name__
                error_message = str(e)
                error_traceback = traceback.format_exc()

                print(f"\033[1;31m Error occurred! {error_type}\033[1;31m: {error_message} | {error_traceback}")
                logging.error(f"Error occurred!", exc_info=True)
        finally:
            print(f"\033[1;32m -> Marcas capturadas com sucesso!, fechando conexão...\033[1;32m")
            brand_page.close()

    def create_brands_file(self):
        print(f"\033[1;36m -> Criando arquivo de marcas...\033[1;36m")
        with open("brands.csv", "w", encoding='utf-8') as b:
            b.write('"name","country","url"\n')

    def save_brands(self):
        self.create_brands_file()
        print(f"\033[1;36m -> Salvando marcas no arquivo...\033[1;36m")
        with open("brands.csv", "a", encoding='utf-8') as b:
            for brand in self.brands:
                b.write(f'"{brand["name"]}","{brand["country"]}","{brand["url"]}"\n')


if __name__ == '__main__':
    brands = Brands()
    brands.get_brands(save_to_file=True)


