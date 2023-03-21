from unidecode import unidecode
import string

def readFile(fileName: str) -> list[str]:
    with open(fileName,'r',encoding="utf8") as file:
        return file.readlines()

def getStripedFileWords(fileContent: list[str]) -> list[str]:
    mergedContent: str = ""
    for line in fileContent:
        mergedContent += line
    return clearPontuation(mergedContent).split(' ')

def clearPontuation(word: str) -> str:
    word = word.replace('\n', ' ')
    word = word.lower()
    word = word.translate(str.maketrans('','', string.punctuation))
    word = unidecode(word)
    return word

def getCleanTextFile(fileName: str) -> list[str]:
    fileContent: list[str] = readFile(fileName)
    stripedFileContent: list[str] = getStripedFileWords(fileContent)
    return stripedFileContent


def main():
    vocabularyText =  getCleanTextFile('file_1.txt')
    documentFile = getCleanTextFile('file_2.txt')
    bagOfWords = getBagOfWords(vocabularyText, documentFile)
    print(bagOfWords)

def getBagOfWords(vocabulary: list[str], document: list[str]) -> list[int]:
    bafOfWords: list[int] = []
    for word in vocabulary:
        if word in document:
            bafOfWords.append(1)
        else:
            bafOfWords.append(0)
    return bafOfWords

if __name__ == "__main__":
    main()