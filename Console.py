# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:59:12 2018

@author: nikov
"""

import pymorphy2

from spacy.lang import ru
from nltk.stem.snowball import SnowballStemmer 
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop = set(nltk.corpus.stopwords.words('russian'))
Unused_chars=[':',',','.','-','\n','?','!']
stemmer = SnowballStemmer('russian')
morph = pymorphy2.MorphAnalyzer()


def tokenize(file_text):
    tokens = word_tokenize(file_text)
    tokens = [i for i in tokens if (i not in stop)]
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]
    return tokens


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 3]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [morph.parse(token)[0].normal_form for token in tokens]
    return tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

#Testing zone, do not launch
import random
import glob
text_data = []
'''
for filename in glob.glob('Test\*.txt'):
    with open(filename,encoding='utf-8') as f:
        for line in f:
            tokens = prepare_text_for_lda(line)
            if random.random() > .001:
                print(tokens)
                text_data.append(tokens)
'''
with open('Test\Незнакомка.txt',encoding='utf-8') as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        if random.random() > .001:
            print(tokens)
            text_data.append(tokens)
from gensim import corpora
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')
import gensim
NUM_TOPICS = 1
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=10)
for topic in topics:
    print(topic)
import re
symbols=['берег очарованный','незнакомка','диск','испытанные остряки','золотится крендель булочной','тлетворный']
symbol_counter = 0
counter=0
p=re.compile(r'"\w+"')
for topic in topics:
    #counter+=1
    lol = topic[1].replace(' +','')
    for topic_word in lol.split():
        counter+=1
        word = p.search(topic_word).group(0).replace('"','')
        print(word)
        for symbol in symbols:
            if word in symbol:
                symbol_counter+=1

'''
for topic in topics:
    counter+=1
    for topic_word in topic[1].split():
        print(topic_word)
        if topic_word in symbols:
            symbol_counter+=1
            continue
'''
print('Точность составляет '+str(symbol_counter/counter))
