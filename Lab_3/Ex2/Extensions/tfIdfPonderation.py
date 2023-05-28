from Extensions import file
from Extensions import objectExtension
from unidecode import unidecode
from rich.console import Console
from rich.table import Table
import string
import os
import math
import time

FILES_FOLDER_PATH = 'files'

def getMergedFilesContent(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedTextContent: list[str] = []

    for fileName in directoryFilesName:
        mergedTextContent += getCleanTextFile(f"{folderPath}/{fileName}")
    
    return objectExtension.removeElementFromList(mergedTextContent, '')

def printPonderationDetails(TF_IDFTable: list[dict[str, int]], fileFolderPath: str) -> None:

    print(f"Quantidade de termos: {len(getMultipleFilesVocabulary(fileFolderPath))}")
    print(f"Termo(s) com maior frequência: {getMaxKeyList(TF_IDFTable)}")

def getMultipleFilesVocabulary(folderPath: str) -> list[str]:
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedVocabulary: list[str] = []

    for fileName in directoryFilesName:
        mergedVocabulary += getVocabulary(f"{folderPath}/{fileName}")
    
    resultList: list[str] = list(set(mergedVocabulary))
    resultList.sort()
    return objectExtension.removeElementFromList(resultList, '')

def getStripedWords(fileContent: list[str]) -> list[str]:
    """
    Recebe uma lista com um elemento, sendo a lista o conteúdo do arquivo e retorna outra 
    lista com cada palavra (que esteja separada por um espaço) em uma posição.
    """
    mergedContent: str = ""
    for line in fileContent:
        mergedContent += line
    
    clearedText: list[str] = clearPunctuation(mergedContent).split(' ')
    return clearedText

def clearPunctuation(word: str) -> str:
    """
    Recebe uma string com qualquer texto em questão e retorna esse mesmo texto sem nenhuma 
    pontuação, formatação ou quebra de linha.
    """
    word = word.replace('\n', ' ')
    word = word.lower()
    word = word.translate(str.maketrans('', '', string.punctuation.replace('-','')))
    word = unidecode(word)
    return word

def getVocabulary(fileName: str) -> list[str]:
    """
    Recebe o nome um arquivo em questão, faz a sua leitura (realizando os devidos tratamentos
    de string), estrutura esse conteúdo num array, remove os elementos repetidos e retorna esse
    mesmo array ordenado.
    """
    fileContent: list[str] = file.readFile(fileName)
    stripedFileContent: list[str] = getStripedWords(fileContent)
    unrepeteadedText: list[str] = list(set(stripedFileContent))

    return unrepeteadedText

def getCleanTextFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo, faz sua leitura e retorna o conteúdo dele sem pontuação
    e com as palavras separadas dentro de uma lista.    
    """
    fileContent: list[str] = file.readFile(fileName)
    stripedFileContent: list[str] = getStripedWords(fileContent)
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
    """
    Busca o nome de todos os arquivos contidos no diretório do caminho contido em folderPath
    """
    return os.listdir(folderPath)

def calculateDocumentTermsProportion(documentfolderPath: str, vocabulary: list[str]) -> dict[str, int]:
    """
    Calcula a quantidade de ocorrências de determinado termo do vocabulário no documento contido em documentfolderPath
    e retorna essa relação em um dicionário (chave:valor)
    """
    documentTerms: list[str] = getCleanTextFile(documentfolderPath)
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
        documentTerms: list[str] = getCleanTextFile(f'{filesFolderPath}/{fileName}')  
        groupedDocumentsTerms.append(documentTerms)
    
    return groupedDocumentsTerms

def initializeDictionary(keys: list[any]) -> dict[any, 0]:
    """
    Inicializa um dicionionário com as chaves contidos em keys com todos os valores zerados
    """
    filledDictionary: dict[any, 0] = {}

    for key in keys:
        filledDictionary.update({key: 0})

    return filledDictionary

def getallDocumentsTermAppearences(filesFolderPath: str) -> dict[str, int]:
    """
    Calcula a quantidade de vezes que algum termo do vocabulário apareceu em todos os documentos
    """
    allDocumentsTerms: list[list[str]] = groupAllDocumentsTerms(filesFolderPath)
    vocabulary: list[str] = getMultipleFilesVocabulary(filesFolderPath)
    allDocumentsTermAppearences: dict[str, int] = initializeDictionary(vocabulary)

    for term in vocabulary:
        for documentTerms in allDocumentsTerms:
            if term in documentTerms:
                previesTermValue: int = allDocumentsTermAppearences.get(term)
                allDocumentsTermAppearences.update({term: previesTermValue + 1})
                
    return allDocumentsTermAppearences

def multiplyDictionaryValues(firstDict: dict[any, any], secondDict: dict[any, any]) -> dict[any, any]:
    """
    Realiza a multiplicação da chaves de dois dicionários e retorna um dicionário único com esses valores
    calculados.
    """

    dictionaryResult: dict[any, any] = {}

    if(len(firstDict) != len(secondDict)):
        raise Exception("Não é possível realizar multiplicação!")
 
    for key in firstDict:
        firstDictTermValue: any = firstDict.get(key) 
        secondDictTermValue: any = secondDict.get(key)

        dictionaryResult.update({key: round(firstDictTermValue * secondDictTermValue,3)})

    return dictionaryResult

def calculateTfIdfPonderation(TFTable: list[dict[str, int]] , IDFTable: dict[str, int]) -> list[dict[str, int]]:
    """
    Recebe uma tabela com TF e outra com o IDF e retorna o TF_IDF calculado.
    """
    result: list[dict[str, int]] = []

    for TFDocument in TFTable:
        result.append(multiplyDictionaryValues(TFDocument, IDFTable))

    return result

def transposeList(elements: list[list[any]]):
    """
    Recebe uma lista de lista qualquer e retorna a mesma transposta.
    Será útil para faz a impressão dos dados na tela
    """
    return  list(map(list, zip(*elements)))

def modelateDictionaryToList(elements: list[dict[str, int]]) -> list[list[str]]:
    """
    Recebe uma lista de dicionário e transforma numa lista de listas com as chaves do dicionário.
    """
    dictionaryKeys: list[any] = list(elements[0].keys())
    dictionaryValues: list[list[any]] = [dictionaryKeys]
    for element in elements:
        dictionaryValues.append(convertListToStringList(list(element.values())))
        
    return transposeList(dictionaryValues)

def setColumnsWidth(table: Table, width: float) -> None:
    """
    Define a largura das colunas da tabela que será impressa.
    """
    for i, column in enumerate(table.columns):
        table.columns[i].width = width
        
def drawTable(tableBody: list[list[any]], Tableheader: list[str], TableTitle: str) -> None:
    """
    Recebe os dados de uma tabela qualquer e imprime os dados da mesmo de uma maneira personalizada.    
    """
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
    """
    Cálcula o IDF de todos os documentos.
    """
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

def generateHeaderTable(headerList: list[str], folderPath: str) -> list[str]:
    """
    Desenha o header de uma tabela qualquer.
    """
    documentsNames: list[str] = getAllFileNamesFromFolder(folderPath)
    headerList: list[str] = headerList

    for documentName in documentsNames:
        headerList.append(documentName)
    
    return headerList

def convertListToStringList(elements: list[any]) -> list[str]:
    """
    Converte todos os itens de uma lista para string
    """
    return [str(i) for i in elements]

def printTfIdfTable(TF_IDF_Table: list[dict[str, int]]) -> None:  
    """
    Imprime a tabela com o TF_IDF.
    """  
    bodyTable: list[list[any]] = modelateDictionaryToList(TF_IDF_Table)
    headerTable: list[str] = generateHeaderTable(["Termo"], FILES_FOLDER_PATH)

    drawTable(bodyTable, headerTable, "TF-IDF")

def printTfTable(TfTable: list[dict[str, int]]) -> None:
    """
    Imprime a tabela com o TF.
    """
    bodyTable: list[list[any]] = modelateDictionaryToList(TfTable)
    headerTable: list[str] = generateHeaderTable(["Termo"], FILES_FOLDER_PATH)

    drawTable(bodyTable, headerTable, "TF")

def printIdfTable(tfIdfTable: list[dict[str, int]]):
    """
    Imprime uma tabela com o IDF.
    """
    bodyTable: list[list[any]] = modelateDictionaryToList(tfIdfTable)
    headerTable: list[str] = ["Termo", "IDFi = log(N/ni)"]

    drawTable(bodyTable, headerTable, "IDF")

def getDictionaryKeyByValue(dictionary: dict[any, any], searchValue: any) -> any:
    """
    Busca uma chave de um dicionário pelo valor dele
    """
    dictionaryKey: any = 0

    for dictKey, dictValue in dictionary.items():
        if dictValue == searchValue:
            dictionaryKey = dictKey

    return dictionaryKey

def getMaxKeyList(listOfDicts: list[dict[any, any]]) -> list[str]:
    """
    Busca a chave do termo maior valor no vocabulário.
    """
    maxesKeysDict: list[any] = []
    maxesValuesDict: list[int] = []
    maxValue: any = 0

    for dictionary in listOfDicts:
        maxesValuesDict.append(max(dictionary.values()))

    maxValue = max(maxesValuesDict)

    for dictionary in listOfDicts:
        maxValueKey: any = getDictionaryKeyByValue(dictionary, maxValue)
        if maxValueKey != 0:
            maxesKeysDict.append(maxValueKey)

    return maxesKeysDict

def showTFIDFStatistics() -> None:
    """
    Imprime todos os dados referentes ao TF_IDF. Assim como o tempo gasto na sua execução.
    """
    startTime: float = time.time()

    tfTable: list[dict[str, int]] = calculateAllDocumentsTfPonderation(FILES_FOLDER_PATH)
    idfTable: list[dict[str, int]] = calculateAllDocumentsIDFponderation(FILES_FOLDER_PATH)
    tfIdfTable: list[dict[str, int]]= calculateTfIdfPonderation(tfTable, idfTable)

    printTfIdfTable(tfIdfTable)
    printPonderationDetails(tfIdfTable, FILES_FOLDER_PATH)

    endTime: float = time.time()
    executiontime: float = endTime - startTime 
    print("Tempo de execução (TF-IDF):", round(executiontime, 2), "segundos")

def showVocabularyStatistics() -> None:
    """
    Imprime o tempo gasto na execução da geração do vocabulário.
    """
    vocabularyStartTime: float = time.time()
    vocabulary: list[str] = getMultipleFilesVocabulary(FILES_FOLDER_PATH)
    vocabularyEndTime: float = time.time()

    executionTimeVocabulary: float = vocabularyEndTime - vocabularyStartTime

    print("Tempo de execução (Vocabulário):", round(executionTimeVocabulary, 5), "segundos")