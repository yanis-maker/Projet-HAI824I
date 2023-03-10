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
                valuesCompare.append((ressourceS, valueS, ressourceC, valueC, prop, listMeasuresValues))
    print(valuesCompare[2][2])
    for item in valuesCompare:
        listMeasComparable = item[5]
        for meas, v in listMeasComparable:
            if isinstance(item[1], rdflib.term.Literal) and isinstance(item[3], rdflib.term.Literal):
                measureValue = compareLiteral(item[1], item[3], meas)
            if isinstance(item[1], rdflib.term.URIRef) and isinstance(item[3], rdflib.term.URIRef):
                measureValue = compareURI(item[1], item[3], meas)
            if isinstance(item[1], rdflib.term.BNode) and isinstance(item[3], rdflib.term.BNode):
                measureValue = compareBNode(item[1], item[3],item[4],meas)

            if measureValue >= seuilChoosed:
                listRessources = ((item[0], item[2]))
                if listRessources in dictRessourceMeasure:
                    for list in dictRessourceMeasure[listRessources]:
                        if list[0] == meas:
                            list[1] += measureValue
                            list[2] += 1
                else:
                    dictRessourceMeasure[listRessources] = ((meas, measureValue, 1))
            else:
                valuesCompare.remove(item)

    for key in dictRessourceMeasure:
        for list in dictRessourceMeasure[key]:
            list[1] /= list[2]

    return dictRessourceMeasure


def compareURI(value1, value2, measure):
    m = Measures(3)

    str1 = str(value1)
    str2 = str(value2)
    q = prepareQuery(
        "SELECT ?property ?value WHERE {?subject ?property ?value.}",
    )
    result1 = grapheSource.query(q, initBindings={'subject': value1})
    result2 = grapheCible.query(q, initBindings={'subject': value2})

    cpt = 1
    total = 0
    for p1, v1 in result1:
        for p2, v2 in result2:
            if str(p1) == str(p2):
                if str(p1) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                    if (str(v1) == str(v2)):
                        total += 1
                else:
                    if (isinstance(v1, Literal)):
                        cpt += 1
                        total += compareLiteral(v1, v2, measure)
                    if (isinstance(v1, URIRef)):
                        cpt += 1
                        total += compareURI(v1, v2, measure)
                    if (isinstance(v1, BNode)):
                        total += compareBNode(v1, v2, p1, measure)
    return total / cpt

    return 0


# compareURI(URIRef("http://data.doremus.org/expression/51cbf519-6243-303f-91f6-f70fe55a92d8"),
#            URIRef("http://data.doremus.org/expression/c5548a52-1da2-348d-9eb0-311293232d05"))


def compareBNode(res1, res2, prop, measure):
    m = Measures(3)
    q1 = prepareQuery(
        """SELECT ?property ?value 
        WHERE {
            ?subject ?property1 ?subject1. 
            ?subject1 ?property ?value
        }"""
    )
    res1 = grapheSource.query(q1, initBindings={'subject': res1, 'property1': prop})
    res2 = grapheCible.query(q1, initBindings={'subject': res2, 'property1': prop})
    total1 = 0
    cpt = 0

    for prop1, obj1 in res1:
        for prop2, obj2 in res2:
            if (prop1 == prop2):
                cpt += 1
                if (isinstance(obj1, Literal)):
                    total1 = compareLiteral(obj1, obj2, measure)
                if (isinstance(obj1, URIRef)):
                    total1 = compareURI(obj1, obj2)
    return total1 / cpt


# compareBNode(URIRef("http://data.doremus.org/event/a7983848-efb9-3757-bdbf-cb068aed4219"),
#              URIRef("http://data.doremus.org/event/a05cbd75-6238-3c6c-8683-f8c7aa5202a1"),
#              URIRef("http://erlangen-crm.org/current/P9_consists_of"))


def compareLiteral(value1, value2, measure):
    m = Measures(3)
    return measure(str(value1), str(value2))


def openResultFile(dicRessourceIdentique):
    # Afficher les préfixes
    with open('resultat.ttl', 'w') as file:
        file.write("@prefix owl: < http: // www.w3.org / 2002 / 07 / owl  # >\n")
        for key in dicRessourceIdentique:
            file.write(key[0] + "owl:sameAs" + key[1] + "\n")


dictionnaire = {
    ("<ressource1>", "<ressource2>"): "p", ("<ressource2>", "<ressource3>"): "p"}
openResultFile(dictionnaire)


# compareBNode(rdflib.term.BNode("n516b68b3b31b44c887c4e546191b53ebb3"),
#              rdflib.term.BNode("n8bb2785687b644cf8527fad82d3be197b9"))

def calculPrecisionRappel(resultFile, refFile):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    # TODO comparer les deux fichiers en terme des ressources et calcul des 3 variables déclarées ci-dessus
    # PAS ENCORE FINI
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return [precision, recall]
