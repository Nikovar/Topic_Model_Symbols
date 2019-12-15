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