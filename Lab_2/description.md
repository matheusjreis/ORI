Exercício 1

Criar um programa que faça o seguinte:

1) Leia múltiplos arquivos de texto (um diretório, por exemplo).

2) Crie o vocabulário (termos de indexação únicos) dos arquivos de texto removendo qualquer tipo de pontuação e considerando somente letras minúsculas.

3) Grave o vocabulário em arquivo texto.

4) Leia o vocabulário em arquivo texto e exiba no console a BoW dos documentos (ausência/presença do termo em um determinado documento).

Submissão: envie o arquivo .py

------

Exercício 2

Criar um programa que receba como parâmetro um arquivo com o vocabulário e um diretório ou caminho com os documentos (arquivos de texto). O programa, então, deverá:

1) Calcular e exibir no console o TF-IDF de cada documento. Testar com a coleção de quatro documentos do livro/sala de aula. Verificar se os valores estão corretos.

Algumas dicas: tentem modularizar as coisas... criem uma função para tratar os documentos (pontuação, letras minúsculas), uma para calcular o TF, uma para o IDF e outra para o TF-IDF. Pode ser interessante usar uma estrutura em Python chamada de "dict" (dicionário). É como se fosse algo como "chave" e "valor". A chave poderia ser o termo (palavra) e o valor o TF-IDF, por exemplo.

Submissão: envie o arquivo .py e um print do console com os valores TF-IDF da coleção do livro/sala de aula.


Exercício 3

-----

1) Crie uma coleção de documentos com as letras das músicas do top 100 da Billboard de 1983 (https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_1983). Trabalhe com somente as 20 primeiras músicas (Top 20). Cada uma das músicas deverá ser transformada um arquivo .txt.

2) Use o programa criado no Exercício 2 para responder as seguintes perguntas:

a) Qual o tamanho do vocabulário da coleção (quantos termos)?
b) Qual termo, em qual documento, possui o maior peso TF-IDF?
c) Quanto tempo o programa demorou para criar o vocabulário da coleção de músicas?
d) Quanto tempo o programa demorou para calcular o TF-IDF da coleção inteira?


Submissão: envie um .zip com os hinos, um print do console com os valores TF-IDF da coleção (o print não precisa mostrar tudo!) e um PDF com as respostas do item 2).

---

Instruções gerais: as respostas devem ser enviadas em um arquivo .zip chamado "TP2_nome_sobrenome.zip". O arquivo deverá ter os seguintes diretórios: "Ex1", "Ex2" e "Ex3". Dentro de cada diretório deve constar cada uma das respostas indicadas cima. IMPORTANTE: caso o arquivo resposta não respeite essa organização/nomenclatura e não possua cada um dos itens solicitados, a nota da atividade será 0.