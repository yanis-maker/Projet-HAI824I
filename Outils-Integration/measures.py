import nltk
import py_stringmatching as psm
from nltk.metrics.distance import jaro_winkler_similarity
from py_stringmatching import Jaccard
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.spatial.distance import hamming

def QGrams(str1,str2):
    n=3
    str1NGram=list(nltk.ngrams(str1.lower(),n))
    str2NGram=list(nltk.ngrams(str2.lower(),n))
    compteur=0
    for item in str1NGram:
        if item in str2NGram:
            compteur=+1
    minLen=min(len(str1NGram),len(str2NGram))
    div=minLen-n+1
    if(div != 0):
        return (compteur/div)
    else :
        return 0.0

def Identity(str1,str2):
    if str1==str2 :
        return 1.0
    else :
        return 0.0

def Jaccard(expr1,expr2):
    n=3
    expr1=expr1.lower()
    expr2=expr2.lower()
    ngrams1=set(nltk.ngrams(expr1,n))
    ngrams2=set(nltk.ngrams(expr2,n))
    extJaccard=Jaccard()
    return extJaccard.get_sim_score(ngrams1,ngrams2)

def Jaro(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    max_dist = (max(len_str1, len_str2) // 2) - 1
    common_chars_str1 = []
    common_chars_str2 = []
    for i, char1 in enumerate(str1):
        for j in range(max(0, i - max_dist), min(len_str2, i + max_dist + 1)):
            if char1 == str2[j] and j not in common_chars_str2:
                common_chars_str1.append(i)
                common_chars_str2.append(j)
                break
    num_common_chars = len(common_chars_str1)
    if num_common_chars == 0:
        return 0.0
    num_transpositions = 0
    for i, j in zip(common_chars_str1, common_chars_str2):
        if str1[i] != str2[j]:
            num_transpositions += 1

    num_transpositions /= 2

    return ((num_common_chars / len_str1) +
                (num_common_chars / len_str2) +
                ((num_common_chars - num_transpositions) / num_common_chars)) / 3.0


def Levenshtein(str1,str2):
    levenshteinDistance=nltk.edit_distance(str1,str2)
    return (1-(levenshteinDistance/max(len(str1),len(str2))))

def JaroWinkler(str1,str2):
    return jaro_winkler_similarity(str1,str2)

def Monge_elkan(s1,s2,sim_func):
    words1 = s1.split()
    words2 = s2.split()
    sim = 0
    for w1 in words1:
        max_sim = 0
        for w2 in words2:
            current_sim = sim_func(w1, w2)
            if current_sim > max_sim:
                max_sim = current_sim
        sim += max_sim
    sim /= len(words1)
    return sim


def Tokenisation(uri):
    uriStr=str(uri)
    if(uriStr.find("http://data.doremus.org/vocabulary/key/")!=-1):
        list = uri.split("/")
        value = list[len(list) - 1]
        uriProperty = "/".join(list) + "/"
        return value
    if(uriStr.find("http://data.doremus.org/vocabulary/iaml/genre/")!=-1):
        list = uri.split("/")
        value = list[len(list) - 1]
        return value

print(Tokenisation("http://data.doremus.org/vocabulary/iaml/genre/salut"))











