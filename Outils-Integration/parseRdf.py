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


'''def getAllProperty():
    propertySource = parseSource()
    propertyCible = parseCible()
    commonProprety = propertySource
    for ps in propertySource:
        for pc in propertyCible:
            if ps != pc and pc not in commonProprety:
                commonProprety.append(pc)

    return commonProprety'''
commonProprety=["Title","Key","Note","Composer","Genre","Opus",""]

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
    #     (r)
    return results



#getSubObjSource("http://erlangen-crm.org/current/P102_has_title",grapheSource)


def compareLiteral(value1, value2, measure):
    return measure(value1, value2)
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

#compare(("http://data.doremus.org/ontology#U11_has_key",),  0.1, (2,))
#dic=compare(("http://erlangen-crm.org/current/P102_has_title",),  0.2, (0,))
openResultFile(dic)
# # for d in dic:
# #     print(d)
print(calculPrecisionRappel())

def getKeys(expression,graphe):
    req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?expression ?key
            WHERE {
              ?expression mus:U11_has_key ?key .
              FILTER (isIRI(?key))
            }
        """

    qres = graphe.query(req, initBindings={'expression': expression})
    result = []

    for row in qres:
        result.append(str(row.key))

    return result;

def getTitles(expression,graphe):
    req = """
           PREFIX mus: <http://data.doremus.org/ontology#>
           PREFIX ecrm: <http://erlangen-crm.org/current/>
           PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
           PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
           SELECT ?expression ?title
           WHERE {
               ?expression ecrm:P102_has_title ?title .
           }
       """

    qres = graphe.query(req, initBindings={'expression': expression})
    result = []

    for row in qres:
        result.append(str(row.title))

    return result;
def getOpus(expression,graphe):
    req = """
           PREFIX mus: <http://data.doremus.org/ontology#>
           PREFIX ecrm: <http://erlangen-crm.org/current/>
           PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
           PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
           SELECT ?expression ?opus
           WHERE {
             ?expression mus:U17_has_opus_statement / mus:U42_has_opus_number ?opus .
           }
       """

    qres = graphe.query(req, initBindings={'expression': expression})
    result = []

    for row in qres:
        result.append(str(row.opus))

    return result;
def getComposer(expression,graphe):
    req = """
           PREFIX mus: <http://data.doremus.org/ontology#>
           PREFIX ecrm: <http://erlangen-crm.org/current/>
           PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
           PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
           SELECT ?expression ?composer
           WHERE {
             ?expression a efrbroo:F22_Self-Contained_Expression .
             ?expCreation efrbroo:R17_created ?expression ;
               ecrm:P9_consists_of / ecrm:P14_carried_out_by ?composer ;
           }
       """

    qres = graphe.query(req, initBindings={'expression': expression})
    result = []

    for row in qres:
        result.append(str(row.composer))

    return result;
def getNotes(expression,graphe):
    req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?expression ?note
            WHERE {
              ?expression ecrm:P3_has_note ?note .
            }
        """

    qres = graphe.query(req, initBindings={'expression': expression})
    result = []

    for row in qres:
        result.append(str(row.note))

    return result;
def getGenres(expression,graphe):
    req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?expression ?genre
            WHERE {
              ?expression mus:U12_has_genre ?genre .
              FILTER (isIRI(?genre))
            }
        """

    result1 = graphe.query(req, initBindings={'expression': expression})
    result = []

    req2 = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?expression ?genre
            WHERE {
              ?expression mus:U12_has_genre / ecrm:P1_is_identified_by ?genre .
            }
        """

    result2 = graphe.query(req2, initBindings={'expression': expression})

    for row in result1:
        result.append(str(row.genre).split("/")[-1].replace("_", " "))

    for row in result2:
        result.append(str(row.genre))

    return result;

'''def compare(propertiesList, seuilChoosed, measuresList):
    jaro=False
    jaroWinkler=False
    identity=False
    levenshtein=False
    qGrams=False
    monge_elkan=False
    jaccard=False
    for measure in measuresList:
       if measure==0:
           jaro=True
       elif measure==1:
           jaroWinkler=True
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

        for ressourceS,valueS in listSource:
            for ressourceC, valueC in listCible:
                sommeMeasure=0
                compteur=0
                if (not isinstance(valueC, BNode) and not isinstance(valueS, BNode)):
                    #print(valueS + "    ############    " + valueC)
                    if isinstance(valueC, rdflib.term.Literal) and isinstance(valueS, rdflib.term.Literal):
                        # print(prop)
                        res = useMeasure(str(valueS), str(valueC), jaro, jaroWinkler, identity, levenshtein, qGrams,
                                         monge_elkan,jaccard)
                        valuesCompare.append((ressourceS, ressourceC, res[1], res[0]))
                    elif isinstance(valueS, URIRef) and isinstance(valueC, URIRef) and isValueMus(prop, valueS):
                        valueSTokend = Tokenisation(valueS)
                        valueCTokend = Tokenisation(valueC)
                        res = useMeasure(valueSTokend, valueCTokend, jaro=0, jaroWinkler=0, identity=1, levenshtein=0,
                                         qGrams=0, monge_elkan=0,jaccard=0)
                        valuesCompare.append((ressourceS, ressourceC, res[1], res[0]))

    for v in valuesCompare:
        print(str(v[0])+"    "+str(v[1])+"  ====== "+str(v[2])+" ; "+str(v[3]))

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
                if (str(ressourceSi)==str(ressourceSj)) and (str(ressourceCj)==str(ressourceCi)):
                    somme+=valuej[2]
                    compteur+=valuej[3]
                    # print(str(ressourceSi)+"   "+str(ressourceCi)+" ======  "+str(somme)+"     "+str(compteur))
                del valuesCompare[j]
            j += 1
        moyenne=somme/compteur
        if moyenne>=seuilChoosed :
            listFinaleMeasure.append([ressourceSi,ressourceCi,moyenne])
        i=i+1

        # for li in listFinaleMeasure
    return listFinaleMeasure

def useMeasure(valueS,valueC,jaro,jaroWinkler,identity,levenshtein,qGrams,monge_elkan,jaccard):
    compteur=0
    sommeMeasure=0
    if jaro:
        sommeMeasure += compareLiteral(valueS,valueC, Jaro)
        compteur += 1
    if jaroWinkler:
        sommeMeasure += compareLiteral(valueS,valueC, JaroWinkler)
        compteur += 1

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
    # if jaccard:
    #     sommeMeasure += compareLiteral(valueS,valueC, Jaccard)
    #     compteur += 1
    return [compteur,sommeMeasure]'''

