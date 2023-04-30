from unidecode import unidecode
import string
import os

FILES_FOLDER_PATH = 'files'
RESULT_FILE_NAME = 'result.txt'

def readFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo e retorna uma lista com o conteúdo dele.
    """
    with open(fileName, 'r', encoding="utf8") as file:
        return file.readlines()

def getMergedFilesContent(folderPath: str) -> list[str]:
    """
    Busca o contéudo de todos os documentos contidos no caminho folderPath concatenados.
    """
    directoryFilesName: list[str] = getAllFileNamesFromFolder(folderPath)
    mergedTextContent: list[str] = []

    for fileName in directoryFilesName:
        mergedTextContent += getCleanTextFile(f"{folderPath}/{fileName}")
    
    return removeElementFromList(mergedTextContent, '')

def getMultipleFilesVocabulary(folderPath: str) -> list[str]:
    """
    Busca e o vocabulário de todos os arquivos concatenados.
    """
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
    """
    Busca o nome de todos os arquivos contidos no diretório do caminho contido em folderPath
    """
    return os.listdir(folderPath)

def printDocumentBagOfWords(folderPath: str, vocabulary: list[str]) -> None:
    """
    Imprime a bag of wards do aqurivo contido em folderPath
    """
    documentFilesName: list[str] = getAllFileNamesFromFolder(folderPath)

    for fileName in documentFilesName:
        print(f'Bag of words do arquivo {fileName}: {getBagOfWords(vocabulary, getCleanTextFile(f"{folderPath}/{fileName}"))}')

def main():
    rootDirectoryPath: str = FILES_FOLDER_PATH
    resultsFileName: str = RESULT_FILE_NAME

    vocabulary: list[str] = getMultipleFilesVocabulary(rootDirectoryPath)

    writeFile(resultsFileName, vocabulary)
    
    printDocumentBagOfWords(rootDirectoryPath, vocabulary)

if __name__ == "__main__":
    main()