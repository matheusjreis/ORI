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

def getVocabulary(fileName: str) -> list[str]:
    fileContent: list[str] = readFile(fileName);
    stripedFileContent: list[str] = getStripedFileWords(fileContent)
    unrepeteadedText: list[str] = list(set(stripedFileContent))
    unrepeteadedText.sort()

    return unrepeteadedText

def writeFile(fileName: str, fileContent: list[str]):
    with open(fileName,'w') as file:
        for line in fileContent:
            file.write(line + '\n')

def main():
    vocabulary = getVocabulary('file_1.txt')
    writeFile('result_ex_1.txt', vocabulary)

if __name__ == "__main__":
    main()