from Extensions import tfIdfPonderation as tfIdfExtension
import Constants
import math

FILES_FOLDER_PATH = 'files'

def getQueryTfPonderation(query: str) -> list[dict[str, int]]:
    return [getQueryTermAppearences(query)]

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

    vocabulary: list[str] = getQueryVocabulary(query)
    documetsIdf: dict[str, int] = tfIdfExtension.calculateAllDocumentsIDFponderation(FILES_FOLDER_PATH)
    idfPondaration: dict[str, int] = tfIdfExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        termValue: int = documetsIdf.get(term)
        idfPondaration.update({term: termValue})

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


def printQueryTfIdfTable(TF_IDF_Table: list[dict[str, int]]) -> None:  
    """
    Imprime a tabela com o TF_IDF.
    """  
    bodyTable: list[list[any]] = tfIdfExtension.modelateDictionaryToList(TF_IDF_Table)
    headerTable: list[str] = ["Termo","Consulta"]

    tfIdfExtension.drawTable(bodyTable, headerTable, "TF-IDF") 


def main():
    # query: str = input("Digite uma consulta qualquer: ")
    query: str = 'to do'

    tfIdfTable = getQueryTfIdfPonderation(query)

    print(tfIdfTable)

    printQueryTfIdfTable(tfIdfTable)

if __name__ == "__main__":
    main()