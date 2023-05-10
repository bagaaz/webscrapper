from lxml import html
import requests
import csv

def get_perfume_links_from_txt(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def format_html_output(tree):
    return html.tostring(tree, pretty_print=True, encoding='unicode', method='html')

def escape_quotes(data):
    if data is None:
        return ""
    elif isinstance(data, list):
        return "; ".join([escape_quotes(item) for item in data])
    elif isinstance(data, dict):
        return "; ".join([f"{k}: {escape_quotes(v)}" for k, v in data.items()])
    else:
        return data.replace('"', '""')

perfumes_links = get_perfume_links_from_txt("colunas_selecionadas.txt")

def main():
    # Permite acesso à página usando python
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    with open("perfumes.csv", "w", encoding='utf-8') as p:
        p.write("nome,marca,ano,concentracao,sexo,imagem,descricao,acordes,notas_topo,notas_meio,notas_fundo,notas_gerais,url\n")

    with open("links_quebrados.csv", "w", encoding='utf-8') as error_file:
        error_writer = csv.writer(error_file)
        error_writer.writerow(["link", "error"])

        for perfume_link in perfumes_links:
            try:
                perfum_page = requests.get(perfume_link, headers=headers)

                # Aqui eu pego o conteúdo da página e transformo em uma árvore
                tree1 = html.fromstring(perfum_page.content)

                #Pegando nome do perfume
                tag_nome = tree1.xpath('//h1[contains(@class, "p_name_h1")]')[0]
                nome = ''.join(tag_nome.xpath('./text()')).strip()

                #Pegando marca do perfume
                tag_marca = tree1.xpath('//h1[contains(@class, "p_name_h1")]/span[@itemprop="brand"]')[0][0][0][0]
                marca = ''.join(tag_marca.xpath('./text()')).strip()

                #Se existir, pegando ano de lançamento do perfume
                try:
                    tag_ano = tree1.xpath('//h1[contains(@class, "p_name_h1")]/span[@itemprop="brand"]')[0][0][1][0]
                    ano = ''.join(tag_ano.xpath('./text()')).strip()
                except:
                    ano = None
                

                try:
                    tag_concentracao = tree1.xpath('//h1[contains(@class, "p_name_h1")]/span[@itemprop="brand"]')[0][0][2]
                    concentracao = ''.join(tag_concentracao.xpath('./text()')).strip()
                except:
                    concentracao = None

                #Pegando o genero do perfume
                tag_genero = tree1.xpath('//div[contains(@class, "p_gender_big ")]')[0][0]
                class_genero = tag_genero.get('class').split(' ')[1]
                if class_genero == 'fa-mars':
                    genero = 'Masculino'
                elif class_genero == 'fa-venus':
                    genero = 'Feminino'
                elif class_genero == 'fa-venus-mars':
                    genero = 'Unissex'

                #Pegando descrição do perfume
                tag_descricao = tree1.xpath('//span[contains(@itemprop, "description")]')[0]
                descricao = tag_descricao.text_content().strip().replace('  Pronunciation', '')

                #Pegando imagem do perfume
                tag_imagem = tree1.xpath('//a[contains(@class, "p_img")]')[0]
                imagem = tag_imagem.get('href')

                #Pegando acordes do perfume
                acordes = []
                tag_acordes = tree1.xpath('//div[contains(@class, "s-circle-container")]')
                for tag_acorde in tag_acordes:
                    nome_acorde = tag_acorde[1].text_content().strip()
                    class_forca_acorde = tag_acorde[0].get('class').split(' ')[1].strip()
                    if class_forca_acorde == 's-circle_l':
                        forca_acorde = 'Alta'
                    elif class_forca_acorde == 's-circle_m':
                        forca_acorde = 'Média'
                    elif class_forca_acorde == 's-circle_s':
                        forca_acorde = 'Baixa'

                    acorde = {
                        'nome': nome_acorde,
                        'forca': forca_acorde
                    }
                    acordes.append(acorde)

                #Pegando notas do perfume
                notas_topo = []
                notas_meio = []
                notas_fundo = []
                notas_gerais = []

                tag_notas = tree1.xpath('//span[contains(@class, "notes_block")]')
                if len(tag_notas) == 1:
                    for nota in tag_notas[0]:
                        nome_nota = nota.xpath('./span')[0].text_content().strip()
                        notas_gerais.append(nome_nota)
                elif len(tag_notas) == 3:
                    #Notas de Topo
                    for nota_topo in tag_notas[0]:
                        nome_nota = nota_topo.xpath('./span')[0].text_content().strip()
                        notas_topo.append(nome_nota)

                    #Notas de Meio
                    for nota_meio in tag_notas[1]:
                        nome_nota = nota_meio.xpath('./span')[0].text_content().strip()
                        notas_meio.append(nome_nota)

                    #Notas de Fundo
                    for nota_fundo in tag_notas[2]:
                        nome_nota = nota_fundo.xpath('./span')[0].text_content().strip()
                        notas_fundo.append(nome_nota)

                with open("perfumes.csv", "a", encoding='utf-8') as p:
                    p.write(f'"{escape_quotes(nome)}","{escape_quotes(marca)}","{escape_quotes(ano)}","{escape_quotes(concentracao)}","{escape_quotes(genero)}","{escape_quotes(imagem)}","{escape_quotes(descricao)}","{escape_quotes(acordes)}","{escape_quotes(notas_topo)}","{escape_quotes(notas_meio)}","{escape_quotes(notas_fundo)}","{escape_quotes(notas_gerais)}","{escape_quotes(perfume_link)}"\n')
                
                print(f'Perfume {nome} salvo com sucesso!')

            except Exception as e:
                error_writer.writerow([perfume_link, str(e)])
                print(e)
                print(f'\033[31m Erro ao salvar perfume, adicionado ao arquivo de erros! \033[0;0m')

            finally:
                perfum_page.close()

if __name__ == '__main__':
    main()
