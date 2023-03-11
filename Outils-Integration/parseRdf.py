import rdflib as rdf
import rdflib.term
from rdflib import Namespace, URIRef, Literal, BNode
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib.plugins.sparql import prepareQuery
from measures import Measures

grapheSource = rdf.Graph()
grapheSource.parse("source.ttl", format="turtle")
grapheCible = rdf.Graph()
grapheCible.parse("cible.ttl", format="turtle")
m = Measures(3)


def parseSource():
    propertySource = []
    for s, p, o in grapheSource:
        namespace = grapheSource.namespace_manager.normalizeUri(p)
        if namespace not in propertySource:
            propertySource.append(namespace)

    return propertySource


def parseCible():
    propertyCible = []

    for s, p, o in grapheCible:
        namespace = grapheCible.namespace_manager.normalizeUri(p)
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
    
            SELECT ?resource ?object
            WHERE{
                ?resource mus:%s ?object.
            }
        """
    elif (uriProperty == "http://erlangen-crm.org/current/"):
        req = """
            PREFIX ecrm: <http://erlangen-crm.org/current/>
    
            SELECT ?resource ?object
            WHERE{
                ?resource ecrm:%s ?object.
            }
        """
    elif (uriProperty == "http://www.w3.org/2001/XMLSchema#"):
        req = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource xsd:%s ?object.
            }
        """
    elif (uriProperty == "http://erlangen-crm.org/efrbroo/"):
        req = """
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
    
            SELECT ?resource ?object
            WHERE{
                ?resource efrbroo:%s ?object.
            }
        """
    elif (uriProperty == "http://purl.org/dc/terms/"):
        req = """
            PREFIX dcterms: <http://purl.org/dc/terms/>
    
            SELECT ?resource ?object
            WHERE{
                ?resource dcterms:%s ?object.
            }
        """
    req = req % namespace
    results = graph.query(req)
    return results


def comparaisonRessources(propertiesList, seuilChoosed, measuresList):
    m = Measures(seuilChoosed)
    valuesCompare = []
    dictRessourceMeasure = dict()
    identiqueValue = []
    strS = None
    strC = None
    measureValue = 0
    listMeasuresValues = []
    for measure in measuresList:
        listMeasuresValues.append((measure, 0))

    for prop in propertiesList:
        listSource = getSubObjSource(prop, grapheSource)
        listCible = getSubObjSource(prop, grapheCible)
        for ressourceS, valueS in listSource:
            for ressourceC, valueC in listCible:
                if not isinstance(ressourceC,BNode) and not isinstance(ressourceS,BNode) and isinstance(valueC, rdflib.term.Literal) and isinstance(valueS, rdflib.term.Literal):
                    print(prop)
                    valuesCompare.append((ressourceS, valueS, ressourceC, valueC, prop, listMeasuresValues))


    for item in valuesCompare:
        property = item[4]
        resS = item[0]
        valueS = item[1]
        resC = item[2]
        valueC = item[3]
        if str(property) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and str(valueS) != str(valueC):
            valuesCompare.remove(item)
            for itemDelete in valuesCompare:
                if itemDelete[0] == resS and itemDelete[2] == resC:
                    valuesCompare.remove(itemDelete)

    for item in valuesCompare:
        listMeasComparable = item[5]
            #print("Ca rentre")
        for meas, v in listMeasComparable:
            print(meas.__name__)
            if isinstance(item[1], rdflib.term.Literal) and isinstance(item[3], rdflib.term.Literal):
                measureValue = compareLiteral(item[1], item[3], meas)
                listRessources = (item[0], item[2])
                if listRessources in dictRessourceMeasure:
                    for cle, list in dictRessourceMeasure.items():
                        if cle==listRessources:
                            if list[0] == meas:
                                list[1] += measureValue
                                list[2] += 1
                else:
                    dictRessourceMeasure[listRessources] = [meas, measureValue, 1]


    for key, list in dictRessourceMeasure.items():
            list[1] /= list[2]
            # if list[1] < seuilChoosed:
            #     del dictRessourceMeasure[key]

    return dictRessourceMeasure

def compareLiteral(value1, value2, measure):
    return measure(str(value1), str(value2))

dic = comparaisonRessources(("http://erlangen-crm.org/current/P3_has_note",),
                            0.5, (m.levenshtein,))


# compareURI(URIRef("http://data.doremus.org/expression/51cbf519-6243-303f-91f6-f70fe55a92d8"),
#            URIRef("http://data.doremus.org/expression/c5548a52-1da2-348d-9eb0-311293232d05"), m.levenshtein)





# compareBNode(URIRef("http://data.doremus.org/event/a7983848-efb9-3757-bdbf-cb068aed4219"),
#              URIRef("http://data.doremus.org/event/a05cbd75-6238-3c6c-8683-f8c7aa5202a1"),
#              URIRef("http://erlangen-crm.org/current/P9_consists_of"))


def openResultFile(dicRessourceIdentique):
    # Afficher les préfixes
    with open('resultat.ttl', 'w') as file:
        file.write("@prefix owl: < http: // www.w3.org / 2002 / 07 / owl  # >\n")
        for key in dicRessourceIdentique:
            file.write("<"+key[0]+">" + " owl:sameAs " + "<"+key[1]+">" + "\n")


openResultFile(dic)
for d in dic:
    print(d)


# compareBNode(rdflib.term.BNode("n516b68b3b31b44c887c4e546191b53ebb3"),
#              rdflib.term.BNode("n8bb2785687b644cf8527fad82d3be197b9"))

def calculPrecisionRappel(resultFile, refFile):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    # TODO comparer les deux fichiers en terme des ressources et calcul des 3 variables déclarées ci-dessus
    fileRef = open('reference_file.ttl', 'r')
    fileResult = open('resultat.ttl', 'r')
    lignesRef = fileRef.readlines()
    lignesRes = fileResult.readlines()
    for ligneRef in lignesRef:
        for lignesRes in lignesRes:
            print("" + lignesRes + "\n")

    # PAS ENCORE FINI
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return [precision, recall]
