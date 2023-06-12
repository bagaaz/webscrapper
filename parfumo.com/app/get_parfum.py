from lxml import html
import requests
import csv
import logging

class Parfums:
    def __init__(self):
        logging.basicConfig(filename='app_parfums.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def get_parfums_links_from_brand(self):

        with open('brands.csv', 'r', encoding='utf-8') as f:
            next(f)
            reader = csv.reader(f)

            self.create_perfums_link_file()

            for row in reader:
                print(f'-> Pegando perfumes da marca: \033[1;34m{row[0]}\033[0;0m')
                brand = {
                    'name': row[0],
                    'country': row[1],
                    'link': row[2]
                }

                self.conect_to_link(brand)
                
    def conect_to_link(self, brand, page=1):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': 'PHPSESSID=6umbjqtc7ljs0bifvpfhj9leda; _ga_47SHE0CVWT=GS1.1.1683834598.1.1.1683834747.0.0.0; _ga=GA1.1.1304156602.1683834599; _sp_enable_dfp_personalized_ads=true; consentUUID=0e1c0df6-d050-4361-ad57-95bf2f91f52f_19; euconsent-v2=CPrmeAAPrmeAAAGABCENDDCsAP_AAAAAAAKIIsgZ5D5cTWFBeXx7QPs0eYwf11ARJmAiCgKAA6ABSDIAcLQEkmASMAyAAAACAAQEIBIBAAAkCAEEAEAQQIgAABHkAgAEhAAIICBEABERAAAACAIKCAAAAQAIAAARIgAAmQCAQ0LmRFQAgIAQJAAAgIgAAAAFAgMAAAAAAAIAAAAAgAAAAQAAAAAAAAACAAABIJAkAAWABUADIAHIAPABAADQAHkARABFACYAE8AN4AcwA_ACEAENAIgAiQBHACWAE0AKUAW4Aw4B-AH6AQMAjgBJgCUgGKANwAcQBIgCkQF5gMkAZcA1gIAJABIADIAH4AfwBzgI9ASsAuoBkIaAQAFwAQwA_ACCgEmALQAkQBSIYACAdQRAFAEMAPwAkwCRAFIiAAIAJB0DEABYAFQAMgAcgA-AEAANAAeAA-gCIAIoATAAnwBcAF0AMQAZgA3gBzAD8AIaARABEgCWAE0AKUAWIAtwBhgDRgH4AfoBAwCLQEcAR0AkwBKQC0AGKANwAcQA5wB1AD7AIvASIAvMBfQDJAGWAMuAaqA1gCDQ4AmABcAEgAMgAfgBoAD-AI4AZoA5wB3AEFAIQAYEA14CPQErAJiAXUAyElAaAAWABkADgAHwAeABEACYAFwAMQAZgBDQCIAIkARwApQBbgD8AI4AWgAxQBuADqAIvASIAvMBlgDWCQAkAC4AuQBmgDuANeAdsA-wCPQErCoAwATAAuACOAI4AWgBeYoAEAQUBHoyAIAEwARwBHAF5jAAICPSEBIABYAGQAmABcADEAGYAN4AjgBSgCxAI4ASkAtABigDnAHUASIA1UgAIADQAH8AZoA5wCCgHbAR6AmIpAkAAWABUADIAHIAPgBAADQAHkARABFACYAE8AKQAYgAzABzAD8AIaARABEgClAFiALcAaMA_AD9AItARwBHQCUgGKANwAfYBF4CRAF5gL6AZIAywBlwDWCgBAAC4AJAAZAA_ADaAH8ARwAuQBmgDnAHcAXUA14B2wEegJiA.YAAAAAAAAAAA; user_id=282285; last_login=1683834739; user_id_key=b89cf5ee67a173a207e7ef8a4c9cbc1e; m7er8padf9=%5B%22QmFnYWF6%22%5D; xbb2mysql_data=N%3B',
            }

            brand_parfums_page = requests.get(brand['link'] + f'?current_page={page}&', headers=headers)
            tree = html.fromstring(brand_parfums_page.content)
            
            tag_perfums = tree.xpath('//div[@class="pgrid mb-1"]')[0]

            for parfum_tag in tag_perfums:
                parfum = {
                    'name': parfum_tag.xpath('.//div[@class="name"]/a/text()')[0],
                    'url': parfum_tag.xpath('.//div[@class="name"]/a/@href')[0]
                }
                self.save_brands(parfum)

            tag_next_page = tree.xpath('//span[@class="dir_text"]')
            for tag in tag_next_page:
                if tag.text_content() == 'Next' or tag.text_content() == 'Next ':
                    print(f"\033[1;43m -> Indo para a pagina {page+1} da marca: \033[1;32m{brand['name']}\033[0;0m")
                    self.conect_to_link(brand, page+1)
                    break

        except Exception as e:
            print(f'Erro ao pegar perfumes da marca: \033[1;31m{brand["name"]}\033[0;0m')
            logging.error("Error occurred while processing brand: {} with link: {}. Perfume: {} with link: {}".format(brand['name'], brand['link'], parfum['name'], parfum['url']), exc_info=True)

        finally:
            print(f"\033[1;32m -> Links de perfumes capturados com sucesso!, fechando conexão...\033[0;0m")
            brand_parfums_page.close()

    def create_perfums_link_file(self):
        print(f"\033[1;36m -> Criando arquivo de links de perfumes...\033[1;36m")
        with open("perfumes_link.csv", "w", encoding='utf-8') as p:
            p.write('"name","url"\n')

    def save_brands(self, parfum):
        print(f"\033[1;36m -> Salvando link do perfume -- {parfum['name']} --...\033[1;36m")
        with open("perfumes_link.csv", "a", encoding='utf-8') as b:
            b.write(f'"{parfum["name"]}","{parfum["url"]}"\n')

    def format_html_output(self, elements):
        return '\n'.join(html.tostring(element, pretty_print=True, encoding='unicode', method='html') for element in elements)



if __name__ == '__main__':
    parfum = Parfums()
    parfum.get_parfums_links_from_brand()