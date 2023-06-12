#Projeto Web Scraping de Perfumes

###Este é um projeto Python para fazer web scraping do site parfumo.com. Ele recupera informações sobre marcas e perfumes, permitindo análises e pesquisas detalhadas sobre os produtos disponíveis.

##Estrutura do Projeto

###A estrutura de diretórios do projeto é a seguinte:

```
/parfumo.com
|---/app
|   |--- __init__.py
|   |--- main.py
|   |--- get_brands.py
|   |--- get_parfum.py
|--- requirements.txt
|--- README.md
|--- .gitignore

```

##Requisitos

###Este projeto requer Python 3.11 ou superior. Além disso, algumas bibliotecas externas são necessárias:

- lxml==4.9.2
- requests==2.30.0
- csv
- traceback

##Como Usar

###Primeiro, instale as dependências necessárias com:

```
pip install -r requirements.txt
```

###Em seguida, você pode executar o programa principal com:

```
python parfumo/main.py
```

###Este comando irá executar o web scraping do site parfumo.com e coletar informações sobre marcas e perfumes.

##Arquivos do Projeto

- `main.py`: Este é o arquivo principal que orquestra o web scraping.
- `get_brands.py`: Este arquivo contém a lógica para extrair informações sobre marcas.
- `get_parfum.py`: Este arquivo contém a lógica para extrair informações sobre perfumes.

##Tratamento de Erros

###Este projeto inclui tratamento básico de erros para problemas de rede e HTTP. Se ocorrer um erro durante o scraping, ele será impresso no console.

##Contribuindo

###Sinta-se à vontade para forkar este projeto e enviar pull requests. Todas as contribuições são bem-vindas!

##Licença

###Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo LICENSE para mais detalhes.