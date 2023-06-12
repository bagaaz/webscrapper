class BrandsModel:
    def __init__(self, database):
        self.database = database

    def getBrands(self):
        self.database.cursor.execute(f'SELECT * FROM marcas WHERE perfumes_saved = ?', (0,))
        return self.database.cursor.fetchall()
    
    def getBrand(self, id):
        self.database.cursor.execute('SELECT * FROM marcas WHERE id = ?', (id,))
        return self.database.cursor.fetchone()
    
    def setBrand(self, nome, pais, url):
        self.database.cursor.execute('INSERT INTO marcas (nome, pais, url) VALUES (?, ?, ?)', (nome, pais, url))
        self.database.connection.commit()
        return self.database.cursor.lastrowid
    
    def updateBrand(self, id):
        self.database.cursor.execute(f'UPDATE marcas SET perfumes_saved = ? WHERE id = ?', (1, id))
        self.database.connection.commit()
        return self.database.cursor.lastrowid
    
if __name__ == '__main__':
    print('Este arquivo não deve ser executado diretamente.')