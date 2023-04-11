from unidecode import unidecode
import string

def readFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo e retorna uma lista com o conteúdo dele.
    """
    with open(fileName,'r',encoding="utf8") as file:
        return file.readlines()

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
    word = word.translate(str.maketrans('','', string.punctuation))
    word = unidecode(word)
    return word

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

def getCleanTextFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo, faz sua leitura e retorna o conteúdo dele sem pontuação
    e com as palavras separadas dentro de uma lista.    
    """
    fileContent: list[str] = readFile(fileName)
    stripedFileContent: list[str] = getStripedFileWords(fileContent)
    return removeElementFromList(stripedFileContent, '')

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

def main():
    """
    Executa a função para buscar o vocabulário contido dos arquivos "vocabulary.txt" e "document.txt",
    o resultado disso é passado como entrada para a função getBagOfWords que retorna a bag of words 
    do arquivo "document.txt".

    Importante citar que os arquivos de input devem estar no mesmo diretório raíz que o programa "ex_2.py"
    e devem conter os nomes "document.txt" e "vocabulary.txt".
    """
    vocabularyText: list[str] =  getCleanTextFile('vocabulary.txt')
    documentFile: list[str] = getCleanTextFile('document.txt')
    bagOfWords: list[int] = getBagOfWords(vocabularyText, documentFile)
    print(bagOfWords)

if __name__ == "__main__":
    main()