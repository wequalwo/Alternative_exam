#Вернуть подмножество слов, которое есть в нашем словаре.
import pickle
from ML import *

class Advanced():
    def __init__(self):
        self.COUNTS = []
        with open('COUNTS.data', 'rb') as file:  
            self.COUNTS = pickle.load(file)
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьяюя'

    def known(self, words):
        return {w for w in words if w in self.COUNTS}


    #"Вернуть все строки, которые находятся на edit_distance == 0  (т.е., просто само слово)
    def distance0(self, word):
        return {word}

    #Вернуть все строки, которые находятся на edit_distance == 2
    def distance2(self, word):
        return {e2 for e1 in self.distance1(word) for e2 in self.distance1(e1)}

    def splits(self, word):
        "Возвращает список всех возможных разбиений слова на пару (a, b)."
        return [(word[:i], word[i:]) 
                for i in range(len(word)+1)]
    
    def distance1(self, word):
        "Возвращает список всех строк на расстоянии edit_distance == 1 от word."
        pairs      = self.splits(word)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in self.alphabet if b]
        inserts    = [a+c+b             for (a, b) in pairs for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)
    
    def advanced_correct(self, word):
        # предрассчитать edit_distance==0, затем 1, затем 2; в противном случае оставить слово "как есть".
        candidates = (self.known(self.distance0(word)) or 
                    self.known(self.distance1(word)) or 
                    self.known(self.distance2(word)) or 
                    [word])
        res = max(candidates, key=self.COUNTS.get)
        if res not in self.COUNTS:
            res = ML_T9_line(res)
        return res

    




