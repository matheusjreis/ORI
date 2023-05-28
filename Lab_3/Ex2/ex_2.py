from Extensions import tfIdfPonderation as tfIdfExtension
import Constants
import math

FILES_FOLDER_PATH = 'files'

def getQueryTfPonderation(query: str) -> list[dict[str, int]]:
    tableTFPonderation: list[dict[str, int]] = []

    queryVocabulary: list[str] = getQueryVocabulary(query)
    filesName: list[str] = tfIdfExtension.getAllFileNamesFromFolder(FILES_FOLDER_PATH)

    for fileName in filesName:
        fileTermProportion: dict[str, int] = tfIdfExtension.calculateDocumentTermsProportion(f'{FILES_FOLDER_PATH}/{fileName}', queryVocabulary)
        tableTFPonderation.append(tfIdfExtension.calculateTFPonderation(fileTermProportion, queryVocabulary))

    return tableTFPonderation

def calculateAllDocumentsQueryIDFponderation(filesFolderPath: str, vocabulary: list[str]) -> dict[str, int]:
    """
    Cálcula o IDF de todos os documentos.
    """
    allDocumentsTermAppearences: dict[str, int] = tfIdfExtension.getallDocumentsTermAppearences(filesFolderPath)
    filesName: list[str] = tfIdfExtension.getAllFileNamesFromFolder(filesFolderPath)
    documentsQuantity: int = len(filesName)
    idfPondaration: dict[str, int] = tfIdfExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        termValue: int = allDocumentsTermAppearences.get(term)
        if termValue > 0:
            idfPondaration.update({term: round(math.log((documentsQuantity/termValue), 2), 3)})

    return idfPondaration

def getQueryTermAppearences(query: str) -> dict[str, int]:
    """
    Calcula a quantidade de vezes que algum termo do vocabulário apareceu em todos os documentos
    """
    queryTerms: list[list[str]] = getQueryTerms(query)
    vocabulary: list[str] = getQueryVocabulary(query)
    queryTermsAppearence: dict[str, int] = tfIdfExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        for documentTerms in queryTerms:
            if term in documentTerms:
                previous: int = queryTermsAppearence.get(term)
                queryTermsAppearence.update({term: previous + 1})
                
    return queryTermsAppearence

def getQueryIDFponderation(query: str) -> dict[str, int]:
    """
    Cálcula o IDF de todos os documentos.
    """

    allQueryTermAppearences: dict[str, int] = getQueryTermAppearences(query)
    vocabulary: list[str] = getQueryVocabulary(query)
    idfPondaration: dict[str, int] = tfIdfExtension.initializeDictionary(vocabulary)

    print(allQueryTermAppearences, vocabulary)

    for term in vocabulary:
        termValue: int = allQueryTermAppearences.get(term)
        if termValue > 0:
            idfPondaration.update({term: round(math.log((1/termValue), 2), 3)})

    return idfPondaration


def getQueryTfIdfPonderation(query: str) -> list[dict[str, int]]:
    tfTable: list[dict[str, int]] = getQueryTfPonderation(query)
    idfTable: dict[str, int] = getQueryIDFponderation(query)    

    return tfIdfExtension.calculateTfIdfPonderation(tfTable, idfTable) 

def getQueryTermsProportion(query: str) -> dict[str, int]:
    """
    Calcula a quantidade de ocorrências de determinado termo do vocabulário no documento contido em documentfolderPath
    e retorna essa relação em um dicionário (chave:valor)
    """
    vocabulary: list[str] = getQueryVocabulary(query)
    queryTerms: list[str] = tfIdfExtension.getStripedWords(query.split(' '))
    
    queryProportion: dict = {}

    for term in vocabulary:                             
        occurrenceTermQuantity: int = queryTerms.count(term)
        queryProportion.update({term: occurrenceTermQuantity})
    return queryProportion

def getQueryVocabulary(query: str) -> list[str]:
    cleanText: list[str] = tfIdfExtension.clearPunctuation(query).split(' ')
    unrepeteadedText: list[str] = list(set(cleanText))

    return unrepeteadedText
    
def getQueryTerms(query: str) -> list[str]:
    return tfIdfExtension.getStripedWords(query.split(' '))

def main():
    # query: str = input("Digite uma consulta qualquer: ")
    query: str = 'to do'

    tfIdfTable = getQueryTfIdfPonderation(query)
    tfIdfExtension.printTfIdfTable(tfIdfTable)

if __name__ == "__main__":
    main()