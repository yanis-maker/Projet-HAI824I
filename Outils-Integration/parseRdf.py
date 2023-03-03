import rdflib as rdf
grapheSource=rdf.Graph()
grapheCible=rdf.Graph()

grapheSource.parse("file1.ttl",format="turtle")
grapheCible.parse("file2.ttl",format="turtle")


listPropretiesSource = []
listPropertiesCible = []
for s, p, o in grapheSource:
    # namespace = grapheSource.namespace_manager.normalizeUri(p)
    if p not in listPropretiesSource:
        listPropretiesSource.append(p)


for s, p, o in grapheCible:
    # namespace = grapheSource.namespace_manager.normalizeUri(p)
    if p not in listPropertiesCible:
        listPropertiesCible.append(p)

for x in listPropertiesCible:
    print(x)


