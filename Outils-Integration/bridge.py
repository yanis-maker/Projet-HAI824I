# Classe pont permettant de sauvegarder les éléments sélectionner dans l'interface graphique et de les envoyer à la fonction qui va effectuer les comparaisons et autres..


class Bridge:

  def __init__(self):
    self.fichierSource = None
    self.fichierCible = None
    self.fichierAlign = None
    self.seuil = None
    self.listSimilarity = []

  def getFichierSource(self):
    return self.fichierSource

  def setFichierSource(self, valeur):
    self.fichierSource = valeur

  def getFichierCible(self):
    return self.fichierCible

  def setFichierCible(self, valeur):
    self.fichierCible = valeur

  def getFichierAlign(self):
    return self.fichierAlign

  def setFichierAlign(self, valeur):
    self.fichierAlign = valeur

  def getSeuil(self):
    return self.seuil

  def setSeuil(self, valeur):
    self.seuil = valeur

  def getListSimilarity(self):
    return self.listSimilarity

  def setListSimilarity(self, valeur):
    self.listSimilarity = valeur

  def addListSimilarity(self, valeur):
    self.listSimilarity.append(valeur)