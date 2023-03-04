import nltk
from nltk.metrics.distance import jaro_winkler_similarity

class Measures:
    def __init__(self, seuil):
        self.seuil = seuil

    def qGrams(self, str1, str2):
        n = 2
        str1NGram = list(nltk.ngrams(str1.lower(), n))
        str2NGram = list(nltk.ngrams(str2.lower(), n))
        print(str1NGram)
        compteur = 0
        for item in str1NGram:
            if item in str2NGram:
                compteur = +1
        minLen = min(len(str1NGram), len(str2NGram))
        div = minLen - n + 1
        if (div != 0):
            return (compteur / div)
        else:
            return 0.0

    def identity(self, str1, str2):
        return str1 == str2

    def levenshtein(self,str1,str2):
        levenshteinDistance=nltk.edit_distance(str1,str2)
        return (1-(levenshteinDistance/max(len(str1),len(str2))))

    def jaro(self,str1,str2):
        return jaro_winkler_similarity(str1,str2)



m = Measures(0.8)
print("afficher ", m.jaro("Amadeus Mozart", "A.Mozart"))






