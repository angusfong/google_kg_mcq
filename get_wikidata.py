#input: variable id

url = 'https://query.wikidata.org/sparql'
query = """
SELECT ?prop_id ?prop_label ?prop_val ?prop_val_label WHERE {
  ?interested wdt:P646 \"""" + id + """\". 
  ?interested ?prop_id ?interested_item.
  ?wd wikibase:directClaim ?prop_id.
  ?wd rdfs:label ?prop_label.
  OPTIONAL {
    ?interested_item rdfs:label ?prop_val.
    FILTER((LANG(?prop_val)) = "en")
  }
  BIND(COALESCE(?prop_val, ?interestedItem) AS ?prop_val_label)
  FILTER((LANG(?prop_label)) = "en")
}
"""
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()['results']['bindings'] 
data = [dat for dat in data if len(dat.keys())==4]

property_ind = np.random.choice(len(data))
data[property_ind]
