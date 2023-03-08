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

def getSubObjSource(property, graph):
    namespace=None
    uriProperty=None
    list=[]
    if(property.find("#")==-1):
        list=property.split("/")
        namespace=list[len(list)-1]
        list.remove(namespace)
        uriProperty="/".join(list) + "/"
    else:
        list = property.split("#")
        namespace = list[len(list) - 1]
        list.remove(namespace)
        uriProperty = "#".join(list) + "#"

    print(uriProperty)
    req=None
    if(uriProperty=="http://data.doremus.org/ontology#"):
        req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource mus:%s ?object.
            }
        """
    elif(uriProperty=="http://erlangen-crm.org/current/"):
        req = """
            PREFIX ecrm: <http://erlangen-crm.org/current/>
    
            SELECT ?resource ?object
            WHERE{
                ?resource ecrm:%s ?object.
            }
        """
    elif(uriProperty=="http://www.w3.org/2001/XMLSchema#"):
        req = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
            SELECT ?resource ?object
            WHERE{
                ?resource xsd:%s ?object.
            }
        """
    elif(uriProperty=="http://erlangen-crm.org/efrbroo/"):
        req = """
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
    
            SELECT ?resource ?object
            WHERE{
                ?resource efrbroo:%s ?object.
            }
        """
    elif(uriProperty=="http://purl.org/dc/terms/"):
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

def comparaisonRessources (propertiesList):
    valuesCompare =[]
    for prop in propertiesList:
        listSource = getSubObjSource(prop,grapheSource)
        listCible = getSubObjSource(prop,grapheCible)
        for ressourceS,valueS in listSource :
            for item in listCible:
                valuesCompare.append((valueS,item[1]))
    return valuesCompare

def comparaisonRessources (propertiesList,measureMethodChoosed,seuilChoosed):
    m=Measures(seuilChoosed)
    valuesCompare =[]
    dictRessourceMeasure=dict()
    for prop in propertiesList:
        listSource = getSubObjSource(prop,grapheSource)
        listCible = getSubObjSource(prop,grapheCible)
        for ressourceS,valueS in listSource :
            for ressourceC,valueC in listCible:
                valuesCompare.append((ressourceS,valueS,ressourceC,valueC,0))
    identiqueValue=[]
    for item in valuesCompare:
        #TO DO transformer les values en string 
        strS=""
        strC="" 
        measureValue=m.measureMethod(strS,strC)
        if measureValue>= seuilChoosed :
            item[4]=measureValue
            listRessources=[item[0],item[2]]
            if listRessources in dictRessourceMeasure :
                value=dictRessourceMeasure[listRessources]
                dictRessourceMeasure[listRessources][0]=value[0]+measureValue
                dictRessourceMeasure[listRessources][1]=value[1]+1 
            else : 
                dictRessourceMeasure[listRessources]=((measureValue,1))
        else :
            valuesCompare.remove(item)
    
    for key in dictRessourceMeasure:
        dictRessourceMeasure[key][0]/=dictRessourceMeasure[key][1]
        
    return dictRessourceMeasure

getSubObjSource("http://erlangen-crm.org/current/P102_has_title",grapheSource)

