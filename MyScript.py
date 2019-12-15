# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:58:16 2019

@author: nikov
"""


import pymorphy2
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
Unused_chars=[':',',','.','-','\n','?','!',"»","«"]
morph = pymorphy2.MorphAnalyzer()



def prepare_text_for_lda(text):
    tokens=text.split()
    tokens = [token for token in tokens if len(token) > 3]
    tokens = [morph.parse(token)[0].normal_form for token in tokens]
    return tokens



decision_value=0.75

Unused_chars=[':',',','.','-','\n','?','!']
custom_useless_words=['из-за','марка','ведь','патриарший','борменталь','филипп','кихот','санчо','антоний','сансон','шарик','мой','такой','другой','ваш','этот','сам','свой','тот','варенуха','степ','маргарита','иван','воланд','коровьев','пилат','николай','какой-то','свой','самый','быть','стать','это','что-то','весь','какой','мочь','никанор','который','ты','никакой','азазело','азазелло','берлиоз']
useless_set=set(custom_useless_words)

#Логический разделитель
Logic_Sep=['PREP','CONJ','PRCL']
Logic_AdVerb=['PRTF','PRTS','GRND']
Logic_Adj=['ADJF','ADJS']
verb=['VERB','INFN']
Separators=Logic_Sep+Logic_AdVerb+verb+Logic_Adj



def logic_construct_extractor(string):
    temp_string=''
    state=False
    Logical_structure=[]
    for word in string.split():
        f_word=word
        for char in Unused_chars:
            if char in f_word:
                f_word=f_word.replace(char,'')
        p=morph.parse(f_word)[0]
        if p.tag.POS in Separators and len(temp_string)>0 and not state:
            Logical_structure.append(temp_string)
            temp_string=f_word+' '
            state=True
        else:
            temp_string+=f_word+' '
            state=False
    Logical_structure.append(temp_string)
    return Logical_structure

def check_symbol_string(string,decision_value):
    count=0
    ngramm=string.split()
    res=decision_value*len(ngramm)
    for gramm in ngramm:
        tokens=prepare_text_for_lda(gramm)
        if not(len(tokens)>0 and (tokens[0] not in useless_set)):
            continue
        for symbol in symbols:
            if tokens[0] in symbol:
                count+=1
                break
    if (count>=res)and len(ngramm)>1:
        return True
    else:
        return False
    
def check_file_symbol(filename,decision_value):
    result={}
    with open(os.path.join(__location__, filename+'.txt'),'r',encoding='utf-8') as f:
        for line in f:
            if not len(line)>1:
                continue
            for string in line.split('.'):
                logic_structs=logic_construct_extractor(string)
                for logic_struct in logic_structs:
                    if check_symbol_string(logic_struct,decision_value):
                        result[logic_struct]=string
    return result


symbols=[]
with open(os.path.join(__location__, 'symbols.txt'),'r',encoding='utf-8') as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        for token in tokens:
            symbols.append(token)

print('\n')
print('Введите имя файла. Регистр важен. Файл должен быть в той же папке, как и приложение. \n')
filename=str(input())
print('Введите вес от 1 до 99')
decision_value=int(input())/100
print('\n')
print('Начало обработки')
print('\n')
some=check_file_symbol(filename,decision_value)
print('\n')
print('Файл обработан')
print('\n')

with open(os.path.join(__location__, 'Confirmed.txt'),'w',encoding='utf-8') as f:
    for meow in some:
        print('Это символ? Введите y - для потверждения, q - для выхода, иной символ для игнорирования')
        print('\n')
        print('{}'.format(meow))
        print('\n')
        print('Предложение')
        print('\n')
        print('{}'.format(some[meow]))
        print('\n')
        if 'y' in (input()).lower():
            f.write('{} \n'.format(meow))
        elif 'q' in (input()).lower():
            print('Завершение работы')
            break
