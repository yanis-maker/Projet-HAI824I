import rdflib as rdf
import rdflib.term
from rdflib import Namespace, URIRef
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

def comparaisonRessources(propertiesList,seuilChoosed,measuresList):
    m=Measures(seuilChoosed)
    valuesCompare = []
    dictRessourceMeasure = dict()
    identiqueValue = []
    strS = None
    strC = None
    measureValue = 0
    listMeasuresValues=[]
    for measure in measuresList:
        listMeasuresValues.append((measure,0))

    for prop in propertiesList:
        listSource = getSubObjSource(prop, grapheSource)
        listCible = getSubObjSource(prop, grapheCible)
        for ressourceS, valueS in listSource:
            for ressourceC, valueC in listCible:
                valuesCompare.append((ressourceS, valueS, ressourceC, valueC, listMeasuresValues))
    for item in valuesCompare:
        ''' 
        if isinstance(item[1], rdflib.term.URIRef) and isinstance(item[3], rdflib.term.URIRef):
            measureValue = compareURI(item[1], item[3])

        if isinstance(item[1], rdflib.term.BNode) and isinstance(item[3], rdflib.term.BNode):
            measureValue = compareBNode(item[1], item[3])
        '''
        if isinstance(item[1], rdflib.term.Literal) and isinstance(item[3], rdflib.term.Literal):
            strS = str(item[1])
            strC = str(item[3])
            listMeasComparable=item[4]
            for meas,v in listMeasComparable:
                measureValue=m.meas(strS,strC)
                if measureValue >= seuilChoosed:
                    listRessources = ((item[0], item[2]))
                    if listRessources in dictRessourceMeasure:
                        for list in dictRessourceMeasure[listRessources] :
                            if list[0]==meas :
                                list[1]+=measureValue
                                list[2]+=1
                    else:
                        dictRessourceMeasure[listRessources] = ((meas, measureValue,1))
                else:
                    valuesCompare.remove(item)

    for key in dictRessourceMeasure:
        for list in dictRessourceMeasure[key]:
            list[1]/=list[2]

    return dictRessourceMeasure

def compareURI(value1, value2, seuilChoosed):
    str1 = str(value1)
    str2 = str(value2)
    q = prepareQuery(
        "SELECT ?property ?value WHERE {?subject ?property ?value .}",
    )
    result1 = grapheSource.query(q, initBindings={'subject': value1})
    result2 = grapheCible.query(q, initBindings={'subject' : value2})

    return 0


# compareURI(URIRef("http://data.doremus.org/expression/51cbf519-6243-303f-91f6-f70fe55a92d8"),
#                   URIRef("http://data.doremus.org/expression/c5548a52-1da2-348d-9eb0-311293232d05"))

def compareBNode(value1, value2, seuil):
    result1 = []
    result2 = []
    m=Measures(seuil)
    for s, p, o in grapheSource:
        if isinstance(s, rdflib.term.BNode):
            result1.append(list[p, o])

    for s, p, o in grapheCible:
        if isinstance(s, rdflib.term.BNode) and s == value1:
            result2.append(list[p, o])
    cpt = 0
    total = 0
    for p1, v1 in result1:
        for p2, v2 in result2:
            if (p1 == p2):
                cpt += 1
                if isinstance(v1, URIRef) and isinstance((v2, URIRef)):
                    total += compareURI(v1, v2)
                else:
                    mesureValue = m.measureMethod(v1, v2)
                    total += mesureValue
    return total / cpt
def openResultFile(dicRessourceIdentique):
    # Afficher les préfixes
    with open('resultat.ttl', 'w') as file:
        file.write("@prefix owl: < http: // www.w3.org / 2002 / 07 / owl  # >\n")
        for key in dicRessourceIdentique:
            file.write(key[0]+"owl:sameAs"+key[1]+"\n")

dictionnaire={
    ("<ressource1>","<ressource2>"):"p",("<ressource2>","<ressource3>"):"p"}
openResultFile(dictionnaire)
# compareBNode(rdflib.term.BNode("n516b68b3b31b44c887c4e546191b53ebb3"),
#              rdflib.term.BNode("n8bb2785687b644cf8527fad82d3be197b9"))

