import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

nltk_id = 'machado'

nltk.download(nltk_id)

print(nltk.corpus.machado.readme())

helena = nltk.corpus.machado.raw('romance/marm03.txt')

print(helena)

helena_clean_text =  re.findall(r'\b[A-zÀ-úü]+\b', helena.lower())

print(helena_clean_text)

nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('portuguese')

print(stopwords)

portuguese_stopwords = set(stopwords)

stemming_helena_text = [w for w in helena_clean_text if w not in portuguese_stopwords]

print(stemming_helena_text)

porter = nltk.PorterStemmer()

no_stemming_helena_text = [porter.stem(t) for t in stemming_helena_text]

print(no_stemming_helena_text)

freq_sem_stem = FreqDist(no_stemming_helena_text)
freq_com_stem = FreqDist(stemming_helena_text)

print("20 palavras mais frequentes sem stem:")
print(freq_sem_stem.most_common(20))

print("20 palavras mais frequentes com stem:")
print(freq_com_stem.most_common(20))

plt.figure(figsize = (13, 8))
freq_sem_stem.plot(25, title = "Frequência de Palavras - Sem Stemming")

plt.figure(figsize = (13, 8))
freq_com_stem.plot(25, title = "Frequência de Palavras - Com Stemming")