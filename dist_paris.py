import requests
from lxml import html
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def format_html_output(tree):
    return html.tostring(tree, pretty_print=True, encoding='unicode', method='html')

# Primeiro, faça o login usando a biblioteca `requests`
login_url = 'https://vendasdistribuidoraparis.com.br/Account/Login?ReturnUrl=%2F'
session = requests.Session()
response = session.get(login_url)

# Pegando o token de autenticação
tree = html.fromstring(response.content)
csrf_token = tree.xpath('//input[@name="__RequestVerificationToken"]/@value')[0]

login_data = {
    '__RequestVerificationToken': csrf_token,
    'Email': 'gabriel.acz.br@gmail.com',
    'Password': getpass('Digite sua senha: '),  # Utilizando getpass para evitar expor a senha
}

login_response = session.post(login_url, data=login_data)

if login_response.status_code != 200:
    raise Exception("Não foi possível fazer login")

# Após o login bem-sucedido, obtenha os cookies da sessão
cookies = session.cookies.get_dict()

# Agora, use Selenium para navegar na página de pedidos
driver = webdriver.Chrome()  # ou outro navegador de sua escolha

try:
    # Adicione os cookies à sessão do Selenium
    driver.get('https://vendasdistribuidoraparis.com.br')  # Primeiro, visite o site para criar uma sessão
    for cookie_name, cookie_value in cookies.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})

    # Agora você pode visitar a página de pedidos diretamente
    driver.get('https://vendasdistribuidoraparis.com.br/Order')

    # Esperando a div que contém os produtos estar presente na página
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@id, "div-product")]')))

    lista_produtos = driver.find_elements(By.XPATH, '//div[contains(@id, "div-product")]')

    for produto in lista_produtos:
        WebDriverWait(produto, 10).until(EC.visibility_of_element_located((By.XPATH, './/div[contains(@class, "col-md-5")]/span[1]')))
        WebDriverWait(produto, 10).until(EC.visibility_of_element_located((By.XPATH, './/span[contains(@class, "product-price")]')))
        nome = produto.find_element(By.XPATH, './/div[contains(@class, "col-md-5")]/span[1]')
        preco = produto.find_element(By.XPATH, './/span[contains(@class, "product-price")]')
        print(nome.text, preco.text)

finally:
    driver.quit()  # Certifique-se de que o navegador seja fechado no final
