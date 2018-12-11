import json
import numpy as np
import requests
import sys
import urllib
import urllib.parse
import urllib.request

def get_wikidata(ids, ind):
  url = 'https://query.wikidata.org/sparql'
  query = """
  SELECT ?prop_id ?prop_label ?prop_val ?prop_val_label WHERE {
    ?interested wdt:P646 \"""" + ids[ind] + """\". 
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
  if (r.ok):
    data = r.json()['results']['bindings'] 
  else:
    raise Exception('Could not get properties of selected thing')
  data = [dat for dat in data if len(dat.keys())==4]

  property_ind = np.random.choice(len(data))
  prop_id = data[property_ind]['prop_id']['value'][36:] #seems ok for now?
  correct_answer = data[property_ind]['prop_val']['value']

  #generate distractors:
  #current way: get entities of that property type
  #write sparql code
  choices = set([correct_answer])
  
  #first way: prop values in other entries
  cand_ind = 0
  while len(choices) < 4 and cand_ind < len(ids):
    cand_id = ids[cand_ind]
    query = """
    SELECT ?thing ?thingLabel ?value ?valueLabel WHERE {
      ?thing wdt:P646 \"""" + cand_id + """\".
      ?thing wdt:P264 ?value.
      ?value rdfs:label ?valueLabel.
      FILTER((LANG(?valueLabel)) = "en")
    }
    """
    r = requests.get(url, params = {'format': 'json', 'query': query})
    if (r.ok):
      data = r.json()['results']['bindings'] 
    else:
      raise Exception('Could not get properties of selected thing')
    for i in range(len(data)):
      if data[i]['valueLabel']['value'] not in choices:
        choices.add(data[i]['valueLabel']['value'])
      if len(choices) == 4:
        break       
    cand_ind += 1
    
