from Extensions import tfIdfPonderation as tfIdfExtension
from Extensions import constants
from Extensions import vector
from Extensions import objectExtension
from Extensions import tableView

import math

def getQueryTfPonderation(query: str) -> list[dict[str, int]]:
    return [getQueryTermAppearences(query)]

def calculateAllDocumentsQueryIDFponderation(filesFolderPath: str, vocabulary: list[str]) -> dict[str, int]:
    """
    Cálcula o IDF de todos os documentos.
    """
    allDocumentsTermAppearences: dict[str, int] = tfIdfExtension.getallDocumentsTermAppearences(filesFolderPath)
    filesName: list[str] = tfIdfExtension.getAllFileNamesFromFolder(filesFolderPath)
    documentsQuantity: int = len(filesName)
    idfPondaration: dict[str, int] = objectExtension.initializeDictionary(vocabulary)

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
    queryTermsAppearence: dict[str, int] = objectExtension.initializeDictionary(vocabulary)

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
    documetsIdf: dict[str, int] = tfIdfExtension.calculateAllDocumentsIDFponderation(constants.FILES_FOLDER_PATH)
    idfPondaration: dict[str, int] = objectExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        termValue: int = documetsIdf.get(term)
        idfPondaration.update({term: termValue})

    return idfPondaration


def getQueryTfIdfPonderation(query: str) -> list[dict[str, int]]:
    tfTable: list[dict[str, int]] = getQueryTfPonderation(query)
    idfTable: dict[str, int] = getQueryIDFponderation(query)    

    return tfIdfExtension.calculateTfIdfPonderation(tfTable, idfTable) 

def getDocumentTfIdfPonderation() -> list[dict[str, int]]:
    tfTable: list[dict[str, int]] = tfIdfExtension.calculateAllDocumentsTfPonderation(constants.FILES_FOLDER_PATH)
    idfTable: list[dict[str, int]] = tfIdfExtension.calculateAllDocumentsIDFponderation(constants.FILES_FOLDER_PATH)  

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
    cleanText: list[str] = objectExtension.clearPunctuation(query).split(' ')
    unrepeteadedText: list[str] = list(set(cleanText))

    return unrepeteadedText
    
def getQueryTerms(query: str) -> list[str]:
    return  objectExtension.getStripedWords(query.split(' '))

def printSimilarityTable(similarityTable: dict, query: str) -> None:
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList([similarityTable])
    headerTable: list[str] = ["Documento","Similaridade"]

    tableView.drawTable(bodyTable, headerTable, f"MODELO VETORIAL - '{query}'")

def printQueryTfIdfTable(TF_IDF_Table: list[dict[str, int]]) -> None:  
    """
    Imprime a tabela com o TF_IDF.
    """  
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList(TF_IDF_Table)
    headerTable: list[str] = ["Termo","Consulta"]

    tableView.drawTable(bodyTable, headerTable, "TF-IDF")

def getQueryDocumentSimilarity(queryVector: list[float], documentVector: list[float]) -> float:
    return vector.calculateVectorProduct(queryVector, documentVector)/vector.calculateVectorNormProduct(queryVector, documentVector)


def getFilteredTfIdfByTerms(terms: list[str], tfIdfTable: list[dict[str, int]]) -> list[dict[str, int]]:
    result = {}
    resultList = []

    for document in tfIdfTable:
        for prop in terms:
            if prop in document:
                result[prop] = document[prop]
            else:
                result.update({prop: 0})
        resultList.append(result)
        result = {}
    return resultList

def getQueryVector(tfIdfTableQuery: list[dict[str, int]]) -> list[float]:
    modelatedQuery = objectExtension.modelateDictionaryToList(tfIdfTableQuery)
    return objectExtension.transposeList(modelatedQuery)[1]

def getQuerySimilarityByDocument(tfIdfDocument: list[dict[str, float]], query: str) -> dict[str, float]:
    tfIdfTableQuery = getQueryTfIdfPonderation(query)
    queryVector = getQueryVector(tfIdfTableQuery)
    filteredDocumentData = getFilteredTfIdfByTerms(getQueryVocabulary(query), tfIdfDocument)
    documentVectors = tfIdfExtension.getRelationshipDocumentTfIdf(filteredDocumentData)
    documentsSimilarities = {}

    for document, documentVector in documentVectors.items():
        convertedQueryVector = objectExtension.convertStringListToFloatList(queryVector)
        convertedDocumentVector =  objectExtension.convertStringListToFloatList(documentVector)
        documentsSimilarities.update({document: getQueryDocumentSimilarity(convertedQueryVector, convertedDocumentVector)})

    return documentsSimilarities

def main():
    query: str = input("Digite uma consulta qualquer: ")
    tfIdfDocument = getDocumentTfIdfPonderation()
    similarity = getQuerySimilarityByDocument(tfIdfDocument, query)
    
    printSimilarityTable(similarity, query)

if __name__ == "__main__":
    main()