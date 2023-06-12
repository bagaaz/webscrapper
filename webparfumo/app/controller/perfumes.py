from model import PerfumesModel, BrandsModel
from controller import BrandsController
from lxml import html
import requests
import logging
import os

class PerfumesController:
    def __init__(self, database):
        self.database = database
        logging.basicConfig(filename='app_parfums.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def getPerfumes(self):
        perfumes = PerfumesModel(self.database)
        return perfumes.getPerfumes()
    
    def getPerfume(self, id):
        perfume = PerfumesModel(self.database)
        return perfume.getPerfume(id)
    
    def setPerfume(self, name, idBrand, url):
        perfume = PerfumesModel(self.database)
        return perfume.setPerfume(name, idBrand, url)
    
    def setPerfumeInfo(self, idPerfume, anoPerfume, concentracaoPerfume, generoPerfume, urlImagemPerfume, descricaoPerfume, acordesPerfume, notasTopoPerfume, notasCoracaoPerfume, notasBasePerfume, notasGeraisPerfume):
        perfume = PerfumesModel(self.database)
        return perfume.setPerfumeInfo(idPerfume, anoPerfume, concentracaoPerfume, generoPerfume, urlImagemPerfume, descricaoPerfume, acordesPerfume, notasTopoPerfume, notasCoracaoPerfume, notasBasePerfume, notasGeraisPerfume)
    
    def updatePerfume(self, id, ):
        perfume = PerfumesModel(self.database)
        return perfume.updatePerfume(id)

    def connectBrandListPage(self):
        brandsList = self.getBrandsList()
        for brand in brandsList:
            idBrand = brand[0]
            nameBrand = brand[1]
            urlBrand = brand[3]
            print(f"-> Indo para a marca: \033[35m{nameBrand}\033[0;0m")

            perfumes = PerfumesModel(self.database)
            perfumes.delPerfumeByBrand(idBrand)

            hasErrosOnBrand = self.connectPerfumePageListId(idBrand, nameBrand, urlBrand)

            if hasErrosOnBrand == 0:
                brandsModel = BrandsModel(self.database)
                brandsModel.updateBrand(idBrand)
        
            print(f'---> Marca: \033[32m{nameBrand}\033[0;0m finalizada com sucesso!')

    def connectPerfumePageListId(self, idBrand, nameBrand, url, page=1, error=0):
        print(f"\033[33m---> Indo para a pagina \033[37m{page} \033[33mda marca: \033[34m{nameBrand}\033[0;0m")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': os.getenv('COOKIE'),
            }

            brandPerfumePage = requests.get(url + f'?current_page={page}&', headers=headers)
            tree = html.fromstring(brandPerfumePage.content)
            PerfumesTags = tree.xpath('//div[@class="pgrid mb-1"]')[0]

            for perfumeTag in PerfumesTags:
                perfumeName =  perfumeTag.xpath('.//div[@class="name"]/a/text()')[0]
                pefumeUrl = perfumeTag.xpath('.//div[@class="name"]/a/@href')[0]

                self.setPerfume(perfumeName, idBrand, pefumeUrl)

            nextPageTag = tree.xpath('//span[@class="dir_text"]')
            for tag in nextPageTag:
                if tag.text_content() == 'Next' or tag.text_content() == 'Next ':
                    self.connectPerfumePageListId(idBrand, nameBrand, url, page+1)
                    break

        except Exception as e:
            print(f'Erro ao pegar perfumes da marca: \033[1;31m{nameBrand}\033[0;0m')
            print(f'Erro: {e}')
            logging.error("Error occurred while processing brand: {} with link: {}.".format(nameBrand, url + f'?current_page={page}&'), exc_info=True)
            error = 1

        finally:
            brandPerfumePage.close()
            return error
        
    def getBrandsList(self):
        brands = BrandsController(self.database)
        brandsList = brands.getBrands()
        return brandsList

    def connectPerfumeInfoPage(self):
        perfumesList = self.getPerfumes()
        for perfume in perfumesList:
            idPerfume = perfume[0]
            namePerfume = perfume[1]
            countryPerfume = perfume[2]
            urlPerfume = perfume[3]
            perfumeIsSaved = perfume[4]

            if perfumeIsSaved == 0:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'pt-BR',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Cookie': os.getenv('COOKIE'),
                    }

                    print(f"-> Indo para o perfume: \033[35m{namePerfume}\033[0;0m")
                    perfumePage = requests.get(urlPerfume, headers=headers)
                    tree = html.fromstring(perfumePage.content)

                    try:
                        tagYear = tree.xpath('//h1[contains(@class, "p_name_h1")]/span[@itemprop="brand"]')[0][0][1][0]
                        perfumeYear = ''.join(tagYear.xpath('./text()')).strip()
                    except:
                        perfumeYear = None

                    try:
                        tagConcentration = tree.xpath('//h1[contains(@class, "p_name_h1")]/span[@itemprop="brand"]')[0][0][2]
                        perfumeConcentration = ''.join(tagConcentration.xpath('./text()')).strip()
                    except:
                        perfumeConcentration = None

                    tagGenre = tree.xpath('//div[contains(@class, "p_gender_big ")]')[0][0]
                    classGenre = tagGenre.get('class').split(' ')[1]
                    if classGenre == 'fa-mars':
                        perfumeGenre = 'Masculino'
                    elif classGenre == 'fa-venus':
                        perfumeGenre = 'Feminino'
                    elif classGenre == 'fa-venus-mars':
                        perfumeGenre = 'Unissex'

                    tagDescription = tree.xpath('//span[contains(@itemprop, "description")]')[0]
                    perfumeDescription = tagDescription.text_content().strip().replace('  Pronunciation', '')

                    try:
                        tagImage = tree.xpath('//a[contains(@class, "p_img")]')[0]
                        perfumeImage = tagImage.get('href')
                    except:
                        try:
                            tagImage = tree.xpath('//img[@itemprop="image"]')[0]
                            perfumeImage = tagImage.get('src')
                        except:
                            perfumeImage = "N/A"

                    #Pegando notas do perfume
                    perfumeChords = []
                    headNotes = []
                    hearthNotes = []
                    baseNotes = []
                    allNotes = []

                    tagChords = tree.xpath('//div[contains(@class, "s-circle-container")]')
                    for tagChord in tagChords:
                        nameChord = tagChord[1].text_content().strip()
                        classPowerChord = tagChord[0].get('class').split(' ')[1].strip()
                        if classPowerChord == 's-circle_l':
                            powerChord = 'Alta'
                        elif classPowerChord == 's-circle_m':
                            powerChord = 'Média'
                        elif classPowerChord == 's-circle_s':
                            powerChord = 'Baixa'

                        chord = {
                            'name': nameChord,
                            'power': powerChord
                        }
                        perfumeChords.append(chord)

                    tagNotes = tree.xpath('//span[contains(@class, "notes_block")]')
                    if len(tagNotes) == 1:
                        noteSpansTag = tagNotes[0].xpath('.//span[contains(@class, "pointer clickable_note_img")]/span[@class="nowrap pointer"]')
                        for tagSpan in noteSpansTag:
                            noteName = tagSpan.text_content().strip()
                            allNotes.append(noteName)
                    elif len(tagNotes) == 3:
                        #Notas de Topo
                        noteHeadSpans = tagNotes[0].xpath('.//span[contains(@class, "pointer clickable_note_img")]/span[@class="nowrap pointer"]')
                        for noteHeadSpan in noteHeadSpans:
                            noteName = noteHeadSpan.text_content().strip()
                            headNotes.append(noteName)

                        #Notas de Meio
                        noteHearthSpans = tagNotes[1].xpath('.//span[contains(@class, "pointer clickable_note_img")]/span[@class="nowrap pointer"]')
                        for noteHerthSpan in noteHearthSpans:
                            noteName = noteHerthSpan.text_content().strip()
                            hearthNotes.append(noteName)

                        #Notas de Fundo
                        noteBaseSpans = tagNotes[2].xpath('.//span[contains(@class, "pointer clickable_note_img")]/span[@class="nowrap pointer"]')
                        for noteBaseSpan in noteBaseSpans:
                            noteName = noteBaseSpan.text_content().strip()
                            baseNotes.append(noteName)
                    elif len(tagNotes) == 0:
                        tagNotes = tree.xpath('//div[contains(@class, "notes_list")]')
                        noteSpansTag = tagNotes[0].xpath('.//span[contains(@class, "clickable_note_img")]/span[@class="nowrap pointer"]')
                        for tagSpan in noteSpansTag:
                            noteName = tagSpan.text_content().strip()
                            allNotes.append(noteName)

                    # Converta os arrays em strings
                    perfumeChordsStr = str(perfumeChords)
                    headNotesStr = str(headNotes)
                    hearthNotesStr = str(hearthNotes)
                    baseNotesStr = str(baseNotes)
                    allNotesStr = str(allNotes)

                    self.setPerfumeInfo(idPerfume, perfumeYear, perfumeConcentration, perfumeGenre, perfumeImage, perfumeDescription, perfumeChordsStr, headNotesStr, hearthNotesStr, baseNotesStr, allNotesStr)
                    self.updatePerfume(idPerfume)
                    print(f'---> Perfume: \033[32m{namePerfume}\033[0;0m finalizado com sucesso!')
                except Exception as e:
                    print(f'Erro ao pegar informações do perfume: \033[1;31m{namePerfume}\033[0;0m')
                    logging.error("Error occurred while processing parfumeInfo: {} with link: {}.".format(namePerfume, urlPerfume), exc_info=True)
                
                finally:
                    if 'perfumePage' in locals():
                        perfumePage.close()

if __name__ == '__main__':
    print('Este arquivo não deve ser executado diretamente.')