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
    valuesCompare = []
    dictRessourceMeasure = []
    identiqueValue = []
    strS = None
    strC = None
    measureValue = 0
    listMeasuresValues = []
    for measure in measuresList:
        listMeasuresValues.append([measure, 0, 0])

    for prop in propertiesList:
        listSource = getSubObjSource(prop, grapheSource)
        listCible = getSubObjSource(prop, grapheCible)
        for ressourceS, valueS in listSource:
            for ressourceC, valueC in listCible:
                if not isinstance(ressourceC,BNode) and not isinstance(ressourceS,BNode) and isinstance(valueC, rdflib.term.Literal) and isinstance(valueS, rdflib.term.Literal):
                    #print(prop)
                    valuesCompare.append((ressourceS, valueS, ressourceC, valueC, prop, listMeasuresValues))
    i=0
    size=len(valuesCompare)
    while i <len(valuesCompare):
        item=valuesCompare[i]
        property = item[4]
        resS = item[0]
        valueS = item[1]
        resC = item[2]
        valueC = item[3]
        if str(property) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and str(valueS) != str(valueC):
            del valuesCompare[i]
            j=0
            while j<size:
                itemDelete=valuesCompare[j]
                if itemDelete[0] == resS and itemDelete[2] == resC:
                    valuesCompare.remove(itemDelete)
                j+=1
        i=+1
    listMeasComparable = item[5]
    for item in valuesCompare:
        for meas, v, c in listMeasComparable:
            #print(meas.__name__)
            if isinstance(item[1], rdflib.term.Literal) and isinstance(item[3], rdflib.term.Literal):
                measureValue = compareLiteral(item[1], item[3], meas)
                listRessources = ((item[0]), (item[2]))
                b=False
                for value in dictRessourceMeasure:
                    if value[0][0]==listRessources[0] and value[0][1]==listRessources[1]:
                        b=True
                        if value[1][0] == meas:
                            value[1][1] += measureValue
                            value[1][2] += 1
                if not b :
                    listMeas=listMeasComparable
                    for m in listMeas:
                        if m[0]==meas:
                            m[1]=measureValue
                            m[2]=1
                            dictRessourceMeasure.append([listRessources,listMeas,0])
    i=0
    while i<len(dictRessourceMeasure):
        sommeMoy = 0
        compteur=0
        moyenne=0
        value=dictRessourceMeasure[i]
        v=value[1]
        for m in v:
            sommeMoy+=m[1];
            compteur+=m[2]
        moyenne=sommeMoy/compteur
        if moyenne>=seuilChoosed:
            value[2]=moyenne
            print(moyenne)
        else :
            del dictRessourceMeasure[i]
        i+=1
    return dictRessourceMeasure

def compareLiteral(value1, value2, measure):
    return measure(str(value1), str(value2))



def openResultFile(dicRessourceIdentique):
    # Afficher les préfixes
    with open('resultat.ttl', 'w') as file:
        file.write("@prefix owl: < http: // www.w3.org / 2002 / 07 / owl  # >\n")
        for key in dicRessourceIdentique:
            file.write("<"+key[0]+">" + "owl:sameAs" + "<"+key[1]+">" + "\n")

def calculPrecisionRappel():
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    # TODO comparer les deux fichiers en terme des ressources et calcul des 3 variables déclarées ci-dessus
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
        print(couple)
        if couple in ressourcesSimRef:
            true_positives += 1
    for co in ressourcesSimRef:
        print(co)

    # PAS ENCORE FINI
    # precision = true_positives / (true_positives + false_positives)
    # recall = true_positives / (true_positives + false_negatives)
    precision = true_positives / total1
    recall = true_positives / total2
    return [precision, recall]
def fMeasure(precision, recall):
    return 2 * ((precision * recall) / (precision + recall))

'''
dic = comparaisonRessources(("http://erlangen-crm.org/current/P3_has_note",),  0.5, (m.levenshtein,))
openResultFile(dic)
for d in dic:
    print(d)'''

fileRef = open('referenceFile', 'r')
fileResult = open('resultat.ttl', 'r')
lignesRef = fileRef.readlines()
lignesRes = fileResult.readlines()
ressourcesSimRes=[]
ressourcesSimRef=[]
for ligne in lignesRes:
    if "owl:sameAs" in ligne:
        r1, r2 = ligne.split("owl:sameAs")
        r1 = str(r1.strip("<>"))
        r2 = str(r2.strip("<>"))
        r2=r2[:-1]
        #print(r1)
        #print(r2)

