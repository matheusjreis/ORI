1) Fazer um programa em Python que receba como entrada um arquivo contendo um texto qualquer e devolva como saída um arquivo de texto contendo o vocabulário (termos de indexação) de tal arquivo. Exemplo:

Entrada:

"Salve o tricolor paulista
Amado clube brasileiro
Tu és forte, tu és grande
Dentre os grandes és o primeiro
Tu és forte, tu és grande
Dentre os grandes és o primeiro"

Saída:

amado
brasileiro
clube
dentre
es
forte
grande
grandes
o
os
paulista
primeiro
salve
tricolor
tu


Pontos importantes:

- Os termos de indexação do arquivo de saída devem estar em ordem alfabética (existe uma função no Python que faz isso!)

- Ao processar o arquivo de entrada: a) considere todas as palavras com letras minúsculas e b) desconsidere pontuação e acentuação. Existem funções no Python que fazem isso!

- Faça testes com diferentes arquivos de entrada;

2) Fazer um programa (ou ajustes no seu programa anterior) que recebe como entrada o arquivo de vocabulário e um arquivo de texto representando um documento. O programa deve devolver como saída a representação "bag of words" (presença/ausência de termos) de tal arquivo texto. Exemplo:

Entrada 1

amado
brasileiro
clube
dentre
es
forte
grande
grandes
o
os
paulista
primeiro
salve
tricolor
tu


Entrada 2

"Tu és forte, tu és grande
Dentre os grandes és o primeiro"

Saída:

[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1]


Outros pontos importantes:

- Pense em como você poderia generalizar o seu programa lendo diversos arquivos (documentos) de uma vez.

- Na medida do possível, tente modularizar o seu código.

Entrega/Desenvolvimento:

- Na sala de aula, use IDEs online como replit.com. Em casa, sugiro usar o Pycharm ou o Jupyter Notebook. Envie como resposta os arquivos *.py correspondentes aos itens 1) e 2).

Algumas dicas:

1) Primeiro o arquivo deve ser aberto usando a função "open()". Depois o arquivo deve ser lido e usando a função "read()".

2) A função unidecode da biblioteca "Unidecode" ajuda no tratamento das palavras chave.

3) A função split() é muito importante!

4) Aprender como percorrer um vetor em Python será essencial para separar as palavras repetidas e criar o vocabulário.