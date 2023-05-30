from unidecode import unidecode
from Extensions import objectExtension
import string
from Extensions import file


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

def convertStringListToFloatList(stringList: list[str]) -> list[float]:
    floatList: list[float] = []
    for item in stringList:
        floatList.append(float(item))
    
    return floatList

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

def modelateDictionaryToList(elements: list[dict[str, int]]) -> list[list[str]]:
    """
    Recebe uma lista de dicionário e transforma numa lista de listas com as chaves do dicionário.
    """
    if elements == {}:
        print('vazio')
        return []

    dictionaryKeys: list[any] = list(elements[0].keys())
    dictionaryValues: list[list[any]] = [dictionaryKeys]
    for element in elements:
        dictionaryValues.append(convertListToStringList(list(element.values())))
    
    return transposeList(dictionaryValues)

def transposeList(elements: list[list[any]]):
    """
    Recebe uma lista de lista qualquer e retorna a mesma transposta.
    Será útil para faz a impressão dos dados na tela
    """
    return  list(map(list, zip(*elements)))

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

        if firstDictTermValue == None:
            firstDictTermValue = 0
        
        if secondDictTermValue == None:
            secondDictTermValue = 0

        dictionaryResult.update({key: round(firstDictTermValue * secondDictTermValue,3)})

    return dictionaryResult

def initializeDictionary(keys: list[any]) -> dict[any, 0]:
    """
    Inicializa um dicionionário com as chaves contidos em keys com todos os valores zerados
    """
    filledDictionary: dict[any, 0] = {}

    for key in keys:
        filledDictionary.update({key: 0})

    return filledDictionary

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


def convertListToStringList(elements: list[any]) -> list[str]:
    """
    Converte todos os itens de uma lista para string
    """
    return [str(i) for i in elements]

def getCleanTextFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo, faz sua leitura e retorna o conteúdo dele sem pontuação
    e com as palavras separadas dentro de uma lista.    
    """
    fileContent: list[str] = file.readFile(fileName)
    stripedFileContent: list[str] = getStripedWords(fileContent)
    return stripedFileContent

def getStripedWords(fileContent: list[str]) -> list[str]:
    """
    Recebe uma lista com um elemento, sendo a lista o conteúdo do arquivo e retorna outra 
    lista com cada palavra (que esteja separada por um espaço) em uma posição.
    """
    mergedContent: str = ""
    for line in fileContent:
        mergedContent += line
    
    clearedText: list[str] = objectExtension.clearPunctuation(mergedContent).split(' ')
    return clearedText