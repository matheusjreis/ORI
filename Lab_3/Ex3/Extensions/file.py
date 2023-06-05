def readFile(fileName: str) -> list[str]:
    """
    Recebe o nome de um arquivo e retorna uma lista com o conteúdo dele.
    """
    with open(fileName, 'r', encoding="utf8") as file:
        return file.readlines()


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