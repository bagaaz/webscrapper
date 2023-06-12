from model import Database
from controller import BrandsController, PerfumesController
import dotenv

dotenv.load_dotenv()

class App:
    def __init__(self):
        self.database = Database()
        self.database.createTables()

    def menu(self):
        while True:
            print('='*50)
            print('\033[33m         Por favor, selecione uma opção:\033[0;0m')
            print('\033[32m1: \033[0;0mBuscar marcas de perfumes')
            print('\033[32m2: \033[0;0mBuscar perfumes por marcas')
            print('\033[32m3: \033[0;0mBuscar informações dos perfumes')
            print('\033[32m0: \033[0;0mSair')
            print('='*50)

            opcao = int(input('Digite a opção escolhida: '))

            if opcao == 1:
                print('Buscando marcas de perfumes...')
                brands = BrandsController(self.database)
                brands.getBrandsFromSite()
                
            elif opcao == 2:
                print('Buscando perfumes por marcas...')
                perfumes = PerfumesController(self.database)
                perfumes.connectBrandListPage()
                
            elif opcao == 3:
                print('Buscando informações dos perfumes...')	
                perfumes = PerfumesController(self.database)
                perfumes.connectPerfumeInfoPage()
            elif opcao == 0:
                print('\033[34m Saindo...\033[0;0m')
                break
            else:
                print(f'\033[31mOpção inválida!\033[0;0m')

    def __del__(self):
        print(' Fechando conexão com o banco de dados...')
        self.database.close()


if __name__ == '__main__':
    app = App()
    app.menu()