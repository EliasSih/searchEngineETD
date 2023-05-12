import pysolr
solr = pysolr.Solr('http://localhost:8983/solr/films', always_commit=True)
solr.ping()

#simple query
results = solr.search("comedy", **{"rows":100000}) #To get all results (up to 100000)
print("Saw {0} result(s).".format(len(results)))
for result in results:
    print("Title:", result['name'])
    pass

#Field specific query
results = solr.search("directed_by:mark", **{"rows":100000}) #To get all results (up to 100000)
print("Saw {0} result(s).".format(len(results)))
for result in results:
    #print("Title:", result['name'])
    pass

#___FACETS___
facetOn = "directed_by"
params = {
  'facet': 'on',
  'facet.field': facetOn,
  'rows': '10',
}

query = "comedy"
results = solr.search(query, **params)
#print(results.facets["facet_fields"][facetOn])

#___Multivalue Search___
query = "directed_by:mark comedy"
params = {
    "qop" : "AND",
    "rows" : 10
}
results = solr.search(query, **params)
for result in results:
    #print("Title:", result['name'])
    pass