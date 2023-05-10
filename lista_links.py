# Função para ler um arquivo CSV e retornar a primeira, segunda e última colunas de cada linha
def extrair_colunas(arquivo_csv):
    colunas_selecionadas = []

    with open(arquivo_csv, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # Remover espaços em branco e quebras de linha

            if linha:  # Verificar se a linha não está vazia
                valores = linha.split(',')  # Dividir a linha em valores usando a vírgula como separador

                # Obter a primeira, segunda e última colunas e remover as aspas simples e duplas
                primeira_coluna = valores[0].replace('"', '').replace("'", "")
                segunda_coluna = valores[1].replace('"', '').replace("'", "")
                ultima_coluna = valores[-1].replace('"', '').replace("'", "")

                colunas_selecionadas.append((primeira_coluna, segunda_coluna, ultima_coluna))

    return colunas_selecionadas

# Função para salvar os valores em um arquivo de texto
def salvar_em_txt(valores, arquivo_txt):
    with open(arquivo_txt, 'w', encoding='utf-8') as arquivo:
        for valor in valores:
            # arquivo.write(f'{valor[0]},{valor[1]},{valor[2]}\n')
            arquivo.write(f'{valor[2]}\n')

def main():
    arquivo_csv = 'popular_brands.csv'
    arquivo_txt = 'colunas_selecionadas.txt'

    colunas_selecionadas = extrair_colunas(arquivo_csv)
    salvar_em_txt(colunas_selecionadas, arquivo_txt)

    print(f'As colunas selecionadas foram salvas em {arquivo_txt}')

if __name__ == '__main__':
    main()
