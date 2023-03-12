import nltk
#import py_stringmatching
from nltk.metrics.distance import jaro_winkler_similarity
#from py_stringmatching import Jaccard
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

# def jaro(self,str1,str2):
#   list1=list(str1)
#   list2=list(str2)
#   lenstr1=len(list1)
#   lenstr2=len(list2)
#   commonChar=[]
#   commonNotSamePos=0
#   for char in list1 :
#     if char in list2:
#       if list1.index(char) != list2.index(char) :
#         commonNotSamePos+=1
#       commonChar.append(char)
#       list1.remove(char)
#       list2.remove(char)
#   nbCommon=len(commonChar)
#   return 1/3*((nbCommon/lenstr1)+(nbCommon/lenstr2)+((nbCommon-commonNotSamePos)/nbCommon))

# def softdfidf(self,expr1,expr2):
#   vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(3,3))
#   vector = vectorizer.fit_transform([expr1,expr2])
#   matrix=vector.toarray()
#   for i in range(matrix.shape[0]):
#       for j in range(matrix.shape[1]):
#           if matrix[i,j] != 0:
#               matrix[i,j] = 1 + np.log10(matrix[i,j])
#   num = np.sum(np.min(matrix, axis=0))
#   den = np.sum(np.max(matrix, axis=0))
#   return num / den

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


# def isURL(str):
#     return str.startswith("http")
#
#
# def tokenisation(str):
#     if (type(str) == list):
#         token = []
#         for elem in str:
#             token = list(set(token) | set(elem.split(" ")))
#         return token
#     elif (isURL(str)):
#         token = str.split("/")[-2:]
#         return token
#     else:
#         return str.split(" ")
#
#
# def pretraitementURL(url):
#     token = tokenisation(url)
#     resultat = "".join(token)
#     return resultat
#
#
# # Fonctions de comparaison de Strings/URL
# def Identity(str1, str2):
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     elif (str1 == str2):
#         return 1.0
#     else:
#         return 0.0
#
#
# def Jaro(str1, str2):
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     else:
#         str1 = pretraitementURL(str1)
#         str2 = pretraitementURL(str2)
#         return psm.Jaro().get_sim_score(str(str1), str(str2))
#
#
# def JaroWinkler(str1, str2):
#
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     else:
#         str1 = pretraitementURL(str1)
#         str2 = pretraitementURL(str2)
#         return psm.JaroWinkler().get_sim_score(str1, str2)
#
#
# def Jaccard(str1, str2):
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     else:
#         str1 = tokenisation(str1)
#         str2 = tokenisation(str2)
#         print(str1)
#         print(str2)
#         return psm.Jaccard().get_sim_score(str1, str2)
#
#
# def QGrams(s1, s2):
#     s1 = pretraitementURL(s1)
#     s2 = pretraitementURL(s2)
#     print(s1)
#     print(s2)
#     i = 0
#     id = 0
#     while ((i + 3) <= len(s1)) or ((i + 3) <= len(s2)):
#         # print(s1[i:i + s], " == ", s2[i:i + s] + "     ?")
#         if s1[i:i + 3] == s2[i:i + 3]:
#             # print("OUI")
#             id += 1
#         i += 1
#     if ((min(len(s1), len(s2)) - 3) < 0):
#         # print("trop grand")
#         return 0
#     return (id) / (min(len(s2), len(s1)) - 3 + 1)
#
#
# def Monge_elkan(str1, str2):
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     else:
#         str1 = tokenisation(str1)
#         str2 = tokenisation(str2)
#         return psm.MongeElkan().get_raw_score(str1, str2)
#
#
# def Levenshtein(str1, str2):
#     if (len(str1) == 0 or len(str2) == 0):
#         return 0.0
#     else:
#         str1 = pretraitementURL(str1)
#         str2 = pretraitementURL(str2)
#         return psm.Levenshtein().get_sim_score(str1, str2)
#
#
# def numSimilarity(num1, num2):
#     if (len(num1) == 0 or len(num2) == 0):
#         return 0.0
#     elif (num1 == num2):
#         return 1.0
#     else:
#         return 0.0

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
#print(m.jaccard("amadus mozart","a.mozart"))
# print(m.jaro("amadus mozart","a.mozart"))
# print(m.jaroWinkler("amadus mozart","a.mozart"))
# print(m.monge_elkan("amadus mozart","a.mozart",jaro_winkler_similarity))
# print(m.levenshtein("amadus mozart","a.mozart"))
# print(m.qGrams("amadus mozart","a.mozart"))











