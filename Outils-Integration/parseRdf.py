import rdflib as rdf
grapheSource=rdf.Graph()


grapheSource.parse("file1.ttl",format="turtle")
proprety=[]

listProprietes=[]
for s, p, o in grapheSource :
    namespace = grapheSource.namespace_manager.normalizeUri(p)
    if namespace not in listProprietes:
        listProprietes.append(namespace)

for x in listProprietes :
  print(x)
