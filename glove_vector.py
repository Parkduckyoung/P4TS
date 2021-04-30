from glove import Corpus, Glove
from gensim.models import Word2Vec
from konlpy.tag import Mecab
import csv

mecab = Mecab(); corpus = Corpus()

def tokenize(doc):
    vector = []
    for t in mecab.pos(doc):
        if "+" in t[1] or t[1] is "XR":
            vector.append(t[0])
        if "NNB" not in t[1] and "J"not in t[1]:
            if "J" not in t[1] and "S"not in t[1] :
                if "E" not in t[1] and "X"not in t[1]:
                    vector.append(t[0])
    return vector

filename = './data/북한_result.csv'
f = open(filename,'r')
rd = csv.reader(f)
r = list(rd)

docs = []

for row in r: 
    if row[1] < '2019.06.01' : docs.append(row[5])

tokens = [tokenize(row) for row in docs]
"""
model = Word2Vec(sentences = tokens, size=300, sg = 1, window = 3, alpha=0.002,min_count = 5, min_alpha=0.0002, iter=20)
model.save('Word2vec')
"""
corpus.fit(tokens,window=5)
glove = Glove(no_components=100, learning_rate=0.05)
glove.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
glove.add_dictionary(corpus.dictionary)
print(glove.dictionary)
"""
a=model.wv.most_similar("미사일")
print("미사일")
print(a)
print('============================\n')
a=model.wv.most_similar("회담")
print("회담")
print(a)
print('============================\n')
a=model.wv.most_similar("핵")
print("핵")
print(a)
print('============================\n')
a=model.wv.most_similar("북")
print("북")
print(a)
print('============================\n')    
print(model.wv["회담"])
"""