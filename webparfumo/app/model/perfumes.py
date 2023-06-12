class PerfumesModel:
    def __init__(self, database):
        self.database = database

    def getPerfumes(self):
        self.database.cursor.execute('SELECT * FROM perfumes')
        return self.database.cursor.fetchall()
    
    def getPerfume(self, id):
        self.database.cursor.execute('SELECT * FROM perfumes WHERE id = ?', (id,))
        return self.database.cursor.fetchone()
    
    def setPerfume(self, nome, idMarca, url):
        self.database.cursor.execute('INSERT INTO perfumes (nome, marca_id, url) VALUES (?, ?, ?)', (nome, idMarca, url))
        self.database.connection.commit()
        return self.database.cursor.lastrowid
    
    def setPerfumeInfo(self, perfume_id, ano, concentracao, genero, url_imagem, descricao, acordes, notas_topo, notas_coracao, notas_base, notas_gerais):
        self.database.cursor.execute('INSERT INTO perfumes_infos (perfume_id, ano, concentracao, genero, url_imagem, descricao, acordes, notas_topo, notas_coracao, notas_base, notas_gerais) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (perfume_id, ano, concentracao, genero, url_imagem, descricao, acordes, notas_topo, notas_coracao, notas_base, notas_gerais))
        self.database.connection.commit()
        return self.database.cursor.lastrowid
    
    def updatePerfume(self, id):
        self.database.cursor.execute('UPDATE perfumes SET info_saved = 1 WHERE id = ?', (id,))
        self.database.connection.commit()
        return self.database.cursor.lastrowid
    
    def delPerfumeByBrand(self, idMarca):
        self.database.cursor.execute('SELECT perfumes_saved FROM marcas WHERE id = ?', (idMarca,))
        saved_perfumes = self.database.cursor.fetchone()
        if saved_perfumes is not None and saved_perfumes[0] == 0:
            self.database.cursor.execute('DELETE FROM perfumes WHERE marca_id = ?', (idMarca,))
            self.database.connection.commit()
            return self.database.cursor.lastrowid
        else:
            return None  # Ou você pode retornar algum valor indicando que a operação não foi realizada


if __name__ == '__main__':
    print('Este arquivo não deve ser executado diretamente.')