from unidecode import unidecode
from rich.console import Console
from rich.table import Table
import string
import os
import math
import time

def readFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo e retorna uma lista com o conteúdo dele.
    """
    with open(fileName, 'r', encoding="utf8") as file:
        return file.readlines()

def getMergedFilesContent(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedTextContent: list[str] = []

    for fileName in directoryFilesName:
        mergedTextContent += getCleanTextFile(f"{folderPath}/{fileName}")
    
    return removeElementFromList(mergedTextContent, '')

def printPonderationDetails(IDFTable: list[dict[str, int]], fileFolderPath: str) -> None:

    print(f"Quantidade de termos: {len(getMultipleFilesVocabulary(fileFolderPath))}")
    print(f"Termo(s) com maior frequência: {printMaxKeyList(IDFTable)}")


def getMultipleFilesVocabulary(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedVocabulary: list[str] = []

    for fileName in directoryFilesName:
        mergedVocabulary += getVocabulary(f"{folderPath}/{fileName}")
    
    resultList: list[str] = list(set(mergedVocabulary))
    resultList.sort()
    return removeElementFromList(resultList, '')


def removeElementFromList(listElements: list[any], element: any) -> list[any]:
    """
    Função auxiliar que recebe uma lista de elementos e um outro elemento qualquer e retorna
    essa mesma lista sem esse elemento.
    """
    result: list[any] = []
    for item in listElements:
        if item != element:
            result.append(item)
    return result

def getStripedFileWords(fileContent: list[str]) -> list[str]:
    """
    Recebe uma lista com um elemento, sendo a lista o conteúdo do arquivo e retorna outra 
    lista com cada palavra (que esteja separada por um espaço) em uma posição.
    """
    mergedContent: str = ""
    for line in fileContent:
        mergedContent += line
    return clearPunctuation(mergedContent).split(' ')


def clearPunctuation(word: str) -> str:
    """
    Recebe uma string com qualquer texto em questão e retorna esse mesmo texto sem nenhuma 
    pontuação, formatação ou quebra de linha.
    """
    word = word.replace('\n', ' ')
    word = word.lower()
    word = word.translate(str.maketrans('', '', string.punctuation))
    word = unidecode(word)
    return word


def getVocabulary(fileName: str) -> list[str]:
    """
    Recebe o nome um arquivo em questão, faz a sua leitura (realizando os devidos tratamentos
    de string), estrutura esse conteúdo num array, remove os elementos repetidos e retorna esse
    mesmo array ordenado.
    """
    fileContent: list[str] = readFile(fileName)
    stripedFileContent: list[str] = getStripedFileWords(fileContent)
    unrepeteadedText: list[str] = list(set(stripedFileContent))

    return unrepeteadedText

def writeFile(newfileName: str, fileContent: list[str]) -> None:
    """
    Recebe o nome de um arquivo qualquer, cria um arquivo com esse nome e escreve o conteúdo contido
    no array fileContent nele.
    """
    try:
        with open(newfileName, 'w') as file:
            for line in fileContent:
                file.write(line + '\n')
        print(f"Arquivo {newfileName} gerado com sucesso!")
    except:
        print("Erro ao tentar escrever no arquivo!")

def getCleanTextFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo, faz sua leitura e retorna o conteúdo dele sem pontuação
    e com as palavras separadas dentro de uma lista.    
    """
    fileContent: list[str] = readFile(fileName)
    stripedFileContent: list[str] = getStripedFileWords(fileContent)
    return stripedFileContent

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
    return os.listdir(folderPath)

def printDocumentBagOfWords(folderPath: str, vocabulary: list[str]) -> None:
    documentFilesName: list[str] = getAllFileNamesFromFolder(folderPath)

    for fileName in documentFilesName:
        print(f'Bag of words do arquivo {fileName}: {getBagOfWords(vocabulary, getCleanTextFile(f"{folderPath}/{fileName}"))}')

def calculateDocumentTermsProportion(documentfolderPath: str, vocabulary: list[str]) -> dict[str, int]:
    documentTerms: list[str] = getCleanTextFile(documentfolderPath)
    documentProportion: dict = {}

    for term in vocabulary:                             
        occurrenceTermQuantity: int = documentTerms.count(term)
        documentProportion.update({term: occurrenceTermQuantity})
    return documentProportion

def calculateAllDocumentsTermsProportion(filesFolderPath: str) -> list[dict[str, int]]:
    tableTermsProportion: list[dict[str, int]] = []
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)

    for fileName in filesName:
        tableTermsProportion.append(calculateDocumentTermsProportion(f'{filesFolderPath}/{fileName}', vocabulary))
    
    return tableTermsProportion

def calculateDocumentTFPonderation(documentTermsProportion: dict[str, int], vocabulary: list[str]) -> dict[str, int]:
    documentTF: dict = {}
    # print('====================document===========================')
    for term in vocabulary:
        termProportion: int = documentTermsProportion.get(term)
        tfPonderation: float = 0

        if(termProportion <= 0):
            tfPonderation = 0
        else:
            tfPonderation = 1 + round(math.log(termProportion, 2), 3)

        documentTF.update({term: tfPonderation})
    return documentTF

def printTable(elements: list[any]) -> None:
    for element in elements:
        print(element)
    print()

def calculateAllDocumentsTfPonderation(filesFolderPath: str) -> list[dict[str, int]]:
    tableTFPonderation: list[dict[str, int]] = []
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)

    for fileName in filesName:
        fileTermProportion: dict[str, int] = calculateDocumentTermsProportion(f'{filesFolderPath}/{fileName}', vocabulary)
        tableTFPonderation.append(calculateDocumentTFPonderation(fileTermProportion, vocabulary))
    
    return tableTFPonderation

def groupAllDocumentsTerms(filesFolderPath: str) -> list[list[str]]:
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    groupedDocumentsTerms: list[list[str]] = []
    for fileName in filesName:
        documentTerms: list[str] = getCleanTextFile(f'{filesFolderPath}/{fileName}')  
        groupedDocumentsTerms.append(documentTerms)
    
    return groupedDocumentsTerms

def initializeDictionary(keys: list[any]) -> dict[any, 0]:
    filledDictionary: dict[any, 0] = {}

    for key in keys:
        filledDictionary.update({key: 0})

    return filledDictionary

def getallDocumentsTermAppearences(filesFolderPath: str) -> dict[str, int]:
    allDocumentsTerms: list[list[str]] = groupAllDocumentsTerms(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)
    allDocumentsTermAppearences: dict[str, int] = initializeDictionary(vocabulary)
    # TODO - MELHORAR PERFORMANCE DESSA PARTE
    for term in vocabulary:
        for documentTerms in allDocumentsTerms:
            if term in documentTerms:
                previesTermValue: int = allDocumentsTermAppearences.get(term)
                allDocumentsTermAppearences.update({term: previesTermValue + 1})
                
    return allDocumentsTermAppearences

def multiplyDictionaryValues(firstDict: dict[any, any], secondDict: dict[any, any]) -> dict[any, any]:
    dictionaryResult: dict[any, any] = {}

    if(len(firstDict) != len(secondDict)):
        raise Exception("Não é possível realizar multiplicação!")
 
    for key in firstDict:
        firstDictTermValue: any = firstDict.get(key) 
        secondDictTermValue: any = secondDict.get(key)

        dictionaryResult.update({key: round(firstDictTermValue * secondDictTermValue,3)})

    return dictionaryResult

def calculateTfIdfPonderation(TFTable: list[dict[str, int]] , IDFTable: dict[str, int]) -> list[dict[str, int]]:
    result: list[dict[str, int]] = []

    for TFDocument in TFTable:
        result.append(multiplyDictionaryValues(TFDocument, IDFTable))

    return result

def transposeList(elements: list[list[any]]):
    return  list(map(list, zip(*elements)))

def modelateDictionaryToList(elements: list[dict[str, int]]) -> list[list[str]]:
    dictionaryKeys: list[any] = list(elements[0].keys())
    dictionaryValues: list[list[any]] = [dictionaryKeys]
    for element in elements:
        dictionaryValues.append(convertListToStringList(list(element.values())))
        
    return transposeList(dictionaryValues)

def setColumnsWidth(table: Table, width: float) -> None:
    for i, column in enumerate(table.columns):
        table.columns[i].width = width
            
        
def drawTable(tableBody: list[list[any]], Tableheader: list[str], TableTitle: str) -> None:
    table = Table(title=TableTitle)

    for headerColumn in Tableheader:
        table.add_column(headerColumn)
    
    for bodyRow in tableBody:
        table.add_row(*bodyRow, style='bright_green')

    console = Console()
    setColumnsWidth(table, 12)
    table.columns[0].width = 18
    console.print(table)


def calculateAllDocumentsIDFponderation(filesFolderPath: str) -> dict[str, int]:
    allDocumentsTermAppearences: dict[str, int] = getallDocumentsTermAppearences(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)
    filesName: list[str] = getAllFileNamesFromFolder(filesFolderPath)
    documentsQuantity: int = len(filesName)
    idfPondaration: dict[str, int] = initializeDictionary(vocabulary)

    for term in vocabulary:
        termValue: int = allDocumentsTermAppearences.get(term)
        if termValue > 0:
            idfPondaration.update({term: round(math.log((documentsQuantity/termValue), 2), 3)})

    return idfPondaration

def generateTFIDFHeaderTable(folderPath: str) -> list[str]:
    documentsNames: list[str] = getAllFileNamesFromFolder(folderPath)
    headerList: list[str] = ["Termo"]

    for documentName in documentsNames:
        headerList.append(documentName)
    
    return headerList

def convertListToStringList(elements: list[any]) -> list[str]:
    return [str(i) for i in elements]

def printTfIdfTable(TF_IDF_Table: list[dict[str, int]]) -> None:    
    bodyTable: list[list[any]] = modelateDictionaryToList(TF_IDF_Table)
    headerTable: list[str] = generateTFIDFHeaderTable('files')

    drawTable(bodyTable, headerTable, "TF-IDF")

def printTfTable(TfTable: list[dict[str, int]]) -> None:
    bodyTable: list[list[any]] = modelateDictionaryToList(TfTable)
    headerTable: list[str] = generateTFIDFHeaderTable('files')

    drawTable(bodyTable, headerTable, "TF")

def printIdfTable(tfIdfTable: list[dict[str, int]]):
    bodyTable: list[list[any]] = modelateDictionaryToList(tfIdfTable)
    headerTable: list[str] = ["Termo", "IDFi = log(N/ni)"]

    drawTable(bodyTable, headerTable, "IDF")

# TODO - MELHORAR FUNÇÃO
def printMaxKeyList(listOfDicts: list[dict[any, any]]):
    max_value: any = max(d[max(d, key=d.get)] for d in listOfDicts)
    max_keys: list[any] = [k for d in listOfDicts for k, v in d.items() if v == max_value]
    return max_keys



def main(): 
    vocabulary_start_time: float = time.time()

    vocabulary: list[str] = getMultipleFilesVocabulary('files')

    vocabulary_end_time: float = time.time()

    start_time: float = time.time()

    TfTable: list[dict[str, int]] = calculateAllDocumentsTfPonderation('files')
    IDFTable: list[dict[str, int]] = calculateAllDocumentsIDFponderation('files')
    TF_IDF_Table: list[dict[str, int]]= calculateTfIdfPonderation(TfTable, IDFTable)

    printTfIdfTable(TF_IDF_Table)
    printPonderationDetails(TF_IDF_Table, 'files')

    end_time: float = time.time()

    execution_time: float = end_time - start_time
    execution_time_vocabulary: float = vocabulary_end_time - vocabulary_start_time

    print("Tempo de execução (Vocabulário):", round(execution_time_vocabulary, 5), "segundos")
    print("Tempo de execução (TF-IDF):", round(execution_time, 2), "segundos")

if __name__ == "__main__":
    main()