import rdflib as rdf
import rdflib.term
from rdflib import Namespace, URIRef, Literal, BNode
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib.plugins.sparql import prepareQuery
from measures import Jaro,JaroWinkler,Identity,Levenshtein,QGrams,Monge_elkan,Jaccard,Tokenisation
import re

grapheSource = rdf.Graph()
grapheSource.parse("source.ttl", format="turtle")
grapheCible = rdf.Graph()
grapheCible.parse("cible.ttl", format="turtle")

mus="http://data.doremus.org/ontology#"
uriU11="http://data.doremus.org/ontology#U11_has_key"
uriU12="http://data.doremus.org/ontology#U12_has_genre"


def parseSource():
    propertySource = []
    for s, p, o in grapheSource:
         namespace = p
        if namespace not in propertySource:
            propertySource.append(namespace)

    return propertySource


def parseCible():
    propertyCible = []

    for s, p, o in grapheCible:
         namespace = p
        if namespace not in propertyCible:
            propertyCible.append(namespace)

    return propertyCible


def getAllProperty():
    propertySource = parseSource()
    propertyCible = parseCible()
    commonProprety = propertySource
    for ps in propertySource:
        for pc in propertyCible:
            if ps != pc and pc not in commonProprety:
                commonProprety.append(pc)

    return commonProprety

def isValueMus(prop,uri):
    if str(prop)==uriU11:
        return True
    if str(prop)==uriU12 and str(uri).find("http://data.doremus.org/vocabulary/iaml/genre/")!=-1:
        return True
    else :
        return False


def getSubObjSource(property, graph):
    namespace = None
    uriProperty = None
    list = []
    if (property.find("#") == -1):
        list = property.split("/")
        namespace = list[len(list) - 1]
        list.remove(namespace)
        uriProperty = "/".join(list) + "/"
    else:
        list = property.split("#")
        namespace = list[len(list) - 1]
        list.remove(namespace)
        uriProperty = "#".join(list) + "#"

    req = None
    if (uriProperty == "http://data.doremus.org/ontology#"):
        req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource mus:%s ?object.
                ?resource rdf:type efrbroo:F22_Self-Contained_Expression
            }
        """
    elif (uriProperty == "http://erlangen-crm.org/current/"):
        req = """
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource ecrm:%s ?object.
                ?resource rdf:type efrbroo:F22_Self-Contained_Expression
            }
        """
    elif (uriProperty == "http://www.w3.org/2001/XMLSchema#"):
        req = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource xsd:%s ?object.
                ?resource rdf:type efrbroo:F22_Self-Contained_Expression
            }
        """
    elif (uriProperty == "http://erlangen-crm.org/efrbroo/"):
        req = """
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource efrbroo:%s ?object.
                ?resource rdf:type efrbroo:F22_Self-Contained_Expression
            }
        """
    elif (uriProperty == "http://purl.org/dc/terms/"):
        req = """
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource dcterms:%s ?object.
                ?resource rdf:type efrbroo:F22_Self-Contained_Expression
            }
        """
    req = req % namespace
    results = graph.query(req)
    # for r in results:
    #     print(r)
    return results



#getSubObjSource("http://erlangen-crm.org/current/P102_has_title",grapheSource)
def compare(propertiesList, seuilChoosed, measuresList):

    jaro=False
    jaroWinkler=False
    identity=False
    levenshtein=False
    qGrams=False
    monge_elkan=False
    jaccard=False
    for measure in measuresList:
       print("hi")
       if measure==0:
           jaro=True
           print("true")
       elif measure==1:
           jaroWinkler=True
           print("true")
       elif measure==2 :
           identity=True
       elif measure==3:
           levenshtein=True
       elif measure==4:
           qGrams=True
       elif measure==5 :
            monge_elkan=True
    valuesCompare = []
    listFinaleMeasure = []
    for prop in propertiesList:
        listSource = getSubObjSource(prop, grapheSource)
        listCible = getSubObjSource(prop, grapheCible)
        print(prop)
        for ressourceS,valueS in listSource:
            for ressourceC, valueC in listCible:
                sommeMeasure=0
                compteur=0
                if isinstance(valueC,rdflib.term.Literal) and isinstance(valueS, rdflib.term.Literal):
                    #print(prop)
                    res=useMeasure(str(valueS),str(valueC),jaro,jaroWinkler,identity,levenshtein,qGrams,monge_elkan)
                    valuesCompare.append((ressourceS, ressourceC,res[1],res[0]))
                elif isinstance(valueS,URIRef) and isinstance(valueC,URIRef) and isValueMus(prop,valueS):
                    valueSTokend=Tokenisation(valueS)
                    valueCTokend=Tokenisation(valueC)
                    res=useMeasure(valueSTokend,valueCTokend,jaro,jaroWinkler,identity,levenshtein,qGrams,monge_elkan)
                    valuesCompare.append((ressourceS, ressourceC, res[1], res[0]))
    i=0
    size=len(valuesCompare)
    somme=0
    compteur=0
    while i<len(valuesCompare) :
        j=i+1
        valuei=valuesCompare[i]
        ressourceSi=valuei[0]
        ressourceCi=valuei[1]
        somme=valuei[2]
        compteur=valuei[3]
        del valuesCompare[i]
        while j<len(valuesCompare):
            if i<(len(valuesCompare)-1) :
                valuej = valuesCompare[j]
                ressourceSj = valuej[0]
                ressourceCj = valuej[1]
                if (ressourceSi==ressourceSj) and (ressourceCj==ressourceCi):
                    somme+=valuej[2]
                    compteur+=valuej[3]
                del valuesCompare[j]
            j += 1
        moyenne=somme/compteur
        if moyenne>=seuilChoosed :
            print(moyenne)
            listFinaleMeasure.append([ressourceSi,ressourceCi,moyenne])
        i=i+1
    return listFinaleMeasure


def compareLiteral(value1, value2, measure):
    return measure(value1, value2)
def useMeasure(valueS,valueC,jaro,jaroWinkler,identity,levenshtein,qGrams,monge_elkan,jaccard):
    compteur=0
    sommeMeasure=0
    if jaro:
        sommeMeasure += compareLiteral(valueS,valueC, Jaro)
        compteur += 1
        print(compteur)
    if jaroWinkler:
        sommeMeasure += compareLiteral(valueS,valueC, JaroWinkler)
        compteur += 1
        print(compteur)
    if identity:
        sommeMeasure += compareLiteral(valueS,valueC, Identity)
        compteur += 1
    if levenshtein:
        sommeMeasure += compareLiteral(valueS,valueC, Levenshtein)
        compteur += 1
    if qGrams:
        sommeMeasure += compareLiteral(valueS,valueC, QGrams)
        compteur += 1
    if monge_elkan:
        sommeMeasure += compareLiteral(valueS,valueC, Monge_elkan)
        compteur += 1
    if jaccard:
        sommeMeasure += compareLiteral(valueS,valueC, Jaccard)
        compteur += 1
    return [compteur,sommeMeasure]


def openResultFile(dicRessourceIdentique):
    # Afficher les préfixes
    with open('resultat.ttl', 'w') as file:
        file.write("@prefix owl: < http: // www.w3.org / 2002 / 07 / owl  # >\n")
        for key in dicRessourceIdentique:
            file.write("<"+str(key[0])+">" + "owl:sameAs" + "<"+str(key[1])+">" + "\n")

def calculPrecisionRappel():
    true_positives = 0
    fileRef = open('referenceFile', 'r')
    fileResult = open('resultat.ttl', 'r')
    lignesRef = fileRef.readlines()
    lignesRes = fileResult.readlines()
    ressourcesSimRes = []
    ressourcesSimRef = []
    # Pour le fichier résultat
    for line in lignesRes:
        match = re.match(r"<(.+)>owl:sameAs<(.+)>", line)
        if match:
            r1 = match.group(1)
            r2 = match.group(2)
            ressourcesSimRes.append((r1, r2))
    # Pour le fichier référence
    i = 0
    while i < len(lignesRef):
        if "<entity1" in lignesRef[i]:
            # Utilisation d'une regex pour extraire les URIs
            r1 = re.search('rdf:resource="(.*?)"', lignesRef[i]).group(1)
            r2 = re.search('rdf:resource="(.*?)"', lignesRef[i + 1]).group(1)
            ressourcesSimRef.append((r1, r2))
        i += 1
    # Calcul TP, FP, FN
    total1 = len(ressourcesSimRef)
    total2 = len(ressourcesSimRes)
    for couple in ressourcesSimRes:
        #print(couple)
        if couple in ressourcesSimRef:
            true_positives += 1         
    precision = true_positives / total2
    recall = true_positives / total1
    return [precision, recall]

def fMeasure(precision, recall):
    return 2 * ((precision * recall) / (precision + recall))


# dic = compare(("http://erlangen-crm.org/current/P102_has_title",),  0.1, (0,))
# openResultFile(dic)
# # for d in dic:
# #     print(d)
print(calculPrecisionRappel())


