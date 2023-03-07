import rdflib as rdf
from rdflib import Namespace, URIRef

grapheSource = rdf.Graph()
grapheCible = rdf.Graph()

grapheSource.parse("source.ttl",format="turtle")
grapheCible.parse("cible.ttl",format="turtle")

propertySource=[]
propertyCible=[]
for s, p, o in grapheSource:
    namespace=grapheSource.namespace_manager.normalizeUri(p)
    if namespace not in propertySource:
      propertySource.append(namespace)

for s, p, o in grapheCible:
    namespace = grapheCible.namespace_manager.normalizeUri(p)
    if namespace not in propertyCible:
      propertyCible.append(namespace)


commonProprety=propertySource
for ps in propertySource:
    for pc in propertyCible:
        if ps!=pc and pc not in commonProprety:
            commonProprety.append(pc)


for x in commonProprety :
  print(x)
