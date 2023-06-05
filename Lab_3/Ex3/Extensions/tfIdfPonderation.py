from Extensions import file
from Extensions import objectExtension
from Extensions import constants
from Extensions import tableView
import os
import math

def getMergedFilesContent(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedTextContent: list[str] = []

    for fileName in directoryFilesName:
        mergedTextContent += objectExtension.getCleanTextFile(f"{folderPath}/{fileName}")
    
    return objectExtension.removeElementFromList(mergedTextContent, '')

def printPonderationDetails(TF_IDFTable: list[dict[str, int]], fileFolderPath: str) -> None:

    print(f"Quantidade de termos: {len(getMultipleFilesVocabulary(fileFolderPath))}")
    print(f"Termo(s) com maior frequência: {objectExtension.getMaxKeyList(TF_IDFTable)}")

def getMultipleFilesVocabulary(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedVocabulary: list[str] = []

    for fileName in directoryFilesName:
        mergedVocabulary += getVocabulary(f"{folderPath}/{fileName}")
    
    resultList: list[str] = list(set(mergedVocabulary))
    resultList.sort()
    return objectExtension.removeElementFromList(resultList, '')

def getVocabulary(fileName: str) -> list[str]:
    """
    Recebe o nome um arquivo em questão, faz a sua leitura (realizando os devidos tratamentos
    de string), estrutura esse conteúdo num array, remove os elementos repetidos e retorna esse
    mesmo array ordenado.
    """
    fileContent: list[str] = file.readFile(fileName)
    stripedFileContent: list[str] = objectExtension.getStripedWords(fileContent)
    unrepeteadedText: list[str] = list(set(stripedFileContent))

    return unrepeteadedText

def getBagOfWords(vocabulary: list[str], document: list[str]) -> list[int]:
    """
    Receba uma lista com os termos do vocabulário, outra com o os termos do documento e 
    retorna uma outra lista representando a ausência ou presença dos termos do vocabulário
    no documento em questão.
    """
    bafOfWords: list[int] = []
    termAbsence: int = 0
    termPresence: int = 1

    for term in vocabulary:
        if term in document:
            bafOfWords.append(termPresence)
        else:
            bafOfWords.append(termAbsence)
    return bafOfWords

def getAllFileNamesFromFolder(folderPath: str) -> list[str]:
    """
    Busca o nome de todos os arquivos contidos no diretório do caminho contido em folderPath
    """
    return os.listdir(folderPath)

def calculateDocumentTermsProportion(documentfolderPath: str, vocabulary: list[str]) -> dict[str, int]:
    """
    Calcula a quantidade de ocorrências de determinado termo do vocabulário no documento contido em documentfolderPath
    e retorna essa relação em um dicionário (chave:valor)
    """
    documentTerms: list[str] = objectExtension.getCleanTextFile(documentfolderPath)
    documentProportion: dict = {}

    for term in vocabulary:                             
        occurrenceTermQuantity: int = documentTerms.count(term)
        documentProportion.update({term: occurrenceTermQuantity})
    return documentProportion

def calculateAllDocumentsTermsProportion(filesFolderPath: str) -> list[dict[str, int]]:
    """
    Calcula proporção da ocorrência dos termos do vocabulário para com todos os documentos.
    """
    tableTermsProportion: list[dict[str, int]] = []
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)

    for fileName in filesName:
        tableTermsProportion.append(calculateDocumentTermsProportion(f'{filesFolderPath}/{fileName}', vocabulary))
    
    return tableTermsProportion

def calculateTFPonderation(documentTermsProportion: dict[str, int], vocabulary: list[str]) -> dict[str, int]:
    """
    Calcula o TF de um documento específico contido, nos quais seus termos estão contidos em  documentTermsProportion
    """
    documentTF: dict = {}
    for term in vocabulary:
        termProportion: int = documentTermsProportion.get(term)
        tfPonderation: float = 0
        if(termProportion <= 0):
            tfPonderation = 0
        else:
            tfPonderation = 1 + round(math.log(termProportion, 2), 3)

        documentTF.update({term: tfPonderation})
    return documentTF

def calculateAllDocumentsTfPonderation(filesFolderPath: str) -> list[dict[str, int]]:
    """
    Faz o cálculo do TF para com todos os documentos, sendo um calculado um documento por vez, através da 
    função calculateTFPonderation.
    """
    tableTFPonderation: list[dict[str, int]] = []
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)

    for fileName in filesName:
        fileTermProportion: dict[str, int] = calculateDocumentTermsProportion(f'{filesFolderPath}/{fileName}', vocabulary)
        tableTFPonderation.append(calculateTFPonderation(fileTermProportion, vocabulary))
    
    return tableTFPonderation

def groupAllDocumentsTerms(filesFolderPath: str) -> list[list[str]]:
    """
    Agrupa os termos de todos os documentos contidos no diretório de caminho filesFolderPath
    """
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    groupedDocumentsTerms: list[list[str]] = []
    for fileName in filesName:
        documentTerms: list[str] = objectExtension.getCleanTextFile(f'{filesFolderPath}/{fileName}')  
        groupedDocumentsTerms.append(documentTerms)
    
    return groupedDocumentsTerms

def getallDocumentsTermAppearences(filesFolderPath: str) -> dict[str, int]:
    """
    Calcula a quantidade de vezes que algum termo do vocabulário apareceu em todos os documentos
    """
    allDocumentsTerms: list[list[str]] = groupAllDocumentsTerms(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)
    allDocumentsTermAppearences: dict[str, int] = objectExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        for documentTerms in allDocumentsTerms:
            if term in documentTerms:
                previesTermValue: int = allDocumentsTermAppearences.get(term)
                allDocumentsTermAppearences.update({term: previesTermValue + 1})
                
    return allDocumentsTermAppearences

def calculateTfIdfPonderation(TFTable: list[dict[str, int]] , IDFTable: dict[str, int]) -> list[dict[str, int]]:
    """
    Recebe uma tabela com TF e outra com o IDF e retorna o TF_IDF calculado.
    """
    result: list[dict[str, int]] = []

    for TFDocument in TFTable:
        result.append(objectExtension.multiplyDictionaryValues(TFDocument, IDFTable))
    return result

def calculateAllDocumentsIDFponderation(filesFolderPath: str) -> dict[str, int]:
    """
    Cálcula o IDF de todos os documentos.
    """
    allDocumentsTermAppearences: dict[str, int] = getallDocumentsTermAppearences(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    documentsQuantity: int = len(filesName)
    idfPondaration: dict[str, int] = objectExtension.initializeDictionary(vocabulary)

    for term in vocabulary:
        termValue: int = allDocumentsTermAppearences.get(term)
        if termValue > 0:
            idfPondaration.update({term: round(math.log((documentsQuantity/termValue), 2), 3)})

    return idfPondaration

def generateHeaderTable(headerList: list[str], folderPath: str) -> list[str]:
    """
    Desenha o header de uma tabela qualquer.
    """
    documentsNames: list[str] = getAllFileNamesFromFolder(folderPath)
    headerList: list[str] = headerList

    for documentName in documentsNames:
        headerList.append(documentName)
    
    return headerList

def printTfIdfTable(TF_IDF_Table: list[dict[str, int]]) -> None:  
    """
    Imprime a tabela com o TF_IDF.
    """  
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList(TF_IDF_Table)
    headerTable: list[str] = generateHeaderTable(["Termo"], constants.FILES_FOLDER_PATH)

    tableView.drawTable(bodyTable, headerTable, "TF-IDF")

def getRelationshipDocumentTfIdf(TF_IDF_Table: list[dict[str, int]]) -> dict[str, list[any]]:
    structuredTfIdf: dict[str, list[any]] = {}
    headerTable: list[str] = generateHeaderTable(["Termo"], constants.FILES_FOLDER_PATH)[1:]
    model = objectExtension.modelateDictionaryToList(TF_IDF_Table)
    bodyTable: list[list[any]] = objectExtension.transposeList(model)[1:]

    for i, title in enumerate(headerTable):
        if len(bodyTable) > 0:
            structuredTfIdf.update({title: bodyTable[i]})
                        
    return structuredTfIdf


def getTfIdfUnifedMatrix(TF_IDF_Table: list[dict[str, int]]) -> list[list[any]]:  
    """
    Imprime a tabela com o TF_IDF.
    """  
    headerTable: list[str] = generateHeaderTable(["Termo"], constants.FILES_FOLDER_PATH)
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList(TF_IDF_Table)

    bodyTable.append(headerTable)

    return bodyTable[::-1]

def printTfTable(TfTable: list[dict[str, int]]) -> None:
    """
    Imprime a tabela com o TF.
    """
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList(TfTable)
    headerTable: list[str] = generateHeaderTable(["Termo"], constants.FILES_FOLDER_PATH)

    tableView.drawTable(bodyTable, headerTable, "TF")

def printIdfTable(tfIdfTable: list[dict[str, int]]):
    """
    Imprime uma tabela com o IDF.
    """
    bodyTable: list[list[any]] = objectExtension.modelateDictionaryToList(tfIdfTable)
    headerTable: list[str] = ["Termo", "IDFi = log(N/ni)"]

    tableView.drawTable(bodyTable, headerTable, "IDF")