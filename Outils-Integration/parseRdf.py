import rdflib as rdf
from rdflib import Namespace, URIRef
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON

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

    for x in commonProprety:
        print(x)

    return commonProprety


def getSubObjSource(property,graph):
    print(property[len(property)-1])
    req = """
        PREFIX mus: <http://data.doremus.org/ontology#>
        PREFIX ecrm: <http://erlangen-crm.org/current/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        
        SELECT ?resource ?object
        WHERE{
            ?resource mus:%s ?object.
        }
    """

    req = req % property
    results = graph.query(req)

    for result in results:
        print(result)


getSubObjSource("U5_had_premiere")
