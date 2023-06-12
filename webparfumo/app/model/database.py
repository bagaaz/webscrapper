import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.createTables()
    
    def createTables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT,
            url TEXT NOT NULL,
            perfumes_saved BOOLEAN NOT NULL DEFAULT 0
        );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS perfumes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            info_saved BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (marca_id) REFERENCES marcas(id)
        );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS perfumes_infos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            perfume_id INTEGER NOT NULL,
            ano TEXT,
            concentracao TEXT,
            genero TEXT,
            url_imagem TEXT,
            descricao TEXT,
            acordes TEXT,
            notas_topo TEXT,
            notas_coracao TEXT,
            notas_base TEXT,
            notas_gerais TEXT,
            FOREIGN KEY (perfume_id) REFERENCES perfumes(id)
        );''')
        self.connection.commit()

    def close(self):
        self.connection.close()
        print(' Conexão com o banco de dados fechada.')

if __name__ == '__main__':
    print('Este arquivo não deve ser executado diretamente.')