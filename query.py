"""Example of Python client calling Knowledge Graph Search API."""
#types allowed:
#EducationalOrganization, Event, GovernmentOrganization, LocalBusiness, Movie, MovieSeries, MusicAlbum,
#MusicGroup, MusicRecording, Organization,Periodical,Person,Place,SportsTeam,TVEpisode,TVSeries,VideoGame,
#VideoGameSeries,WebSite

import json
import numpy as np
import requests
import sys
import urllib
import urllib.parse
import urllib.request
import time
import q_generator
import random
#import get_wikidata

LIMIT = 100 #this many?
N_CHOICES = 4
API_KEY = open('.api_key').read()

general = True
if "-specific" in sys.argv:
    general = False

if "-type" in sys.argv:
    t = sys.argv[sys.argv.index("-type") + 1]
else:
    t = 'Thing'

#prompt user to input topic of interest (easy for debugging)
#query = input("Topic of interest: ")
query = sys.argv[1]
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': LIMIT,
    'indent': True,
    'key': API_KEY,
    'types': t
}

url = service_url + '?' + urllib.parse.urlencode(params)

#loop until successfully get response (might take some time depending on server)
begin = time.time()
while True:
    try:
        response = json.loads(urllib.request.urlopen(url).read())
        break
    except Exception: # still allows to quit with KeyboardInterrupt
        if time.time() - begin > 30:
            raise Exception('No matching entities found')
        continue

if len(response['itemListElement'])==0:
    raise Exception('No matching entities found')

#array of all search results
ids = []
names = []
scores = []
for element in response['itemListElement']:
    if 'name' in element['result'].keys():
        names.append(element['result']['name'])
        ids.append(element['result']['@id'][3:]) #this gets freebase id
        scores.append(element['resultScore'])

#define probability distribution over search results
if general:
    probs = [score/sum(scores) for score in scores]
else:
    probs = [0]*len(scores)
    probs[0] = 1

n = len(scores)

#stay on topic before user terminates
while True:
    url = 'https://query.wikidata.org/sparql'
    data = []
    begin = time.time()
    while len(data) == 0:
        if time.time() - begin > 30:
            raise Exception('Wikidata has nothing to quiz you on about a ' + params['types'] + ' called ' + sys.argv[1] + ' :(')
        ind = np.random.choice(n, p=probs)
        id = ids[ind]
        #print('Probabilistically selected entity: ' + names[ind])
        query = """
        SELECT ?prop_id ?prop_label ?prop_val ?interested_item WHERE {
          ?interested wdt:P646 \"""" + ids[ind] + """\". 
          ?interested ?prop_id ?interested_item.
          ?wd wikibase:directClaim ?prop_id.
          ?wd rdfs:label ?prop_label.
          OPTIONAL {
            ?interested_item rdfs:label ?prop_val.
            FILTER((LANG(?prop_val)) = "en")
          }
          FILTER((LANG(?prop_label)) = "en")
        }
        """
        r = requests.get(url, params = {'format': 'json', 'query': query})
        if (r.ok):
          data = r.json()['results']['bindings'] 

    data = [dat for dat in data if len(dat.keys())==4]
    #for dat in data:
    #    #print(dat['prop_label']['value'] + ': ' + dat['prop_val']['value'])

    property_ind = np.random.choice(len(data))
    prop_id = data[property_ind]['prop_id']['value'][36:] #for property
    prop_name = data[property_ind]['prop_label']['value']
    #print('Selected property: ' + prop_name)
    correct_answer = data[property_ind]['prop_val']['value']

    #generate distractors:
    #current way: get entities of that property type
    #write sparql code
    choices = set([correct_answer])

    #first way: prop values in other entries
    cand_ind = 0
    begin = time.time()
    while len(choices) < N_CHOICES and cand_ind < len(ids):
        cand_id = ids[cand_ind]
        query = """
        SELECT ?thing ?thingLabel ?value ?valueLabel WHERE {
            ?thing wdt:P646 \"""" + cand_id + """\".
            ?thing wdt:""" + prop_id + """ ?value.
            ?value rdfs:label ?valueLabel.
            FILTER((LANG(?valueLabel)) = "en")
        }
        LIMIT """ + str(N_CHOICES)
        
        r = requests.get(url, params = {'format': 'json', 'query': query})
        if (r.ok):
            data = r.json()['results']['bindings'] 
            if len(data) == 0:
                ##print('candidate ' + str(cand_ind) + 'does not have the associated property')
                cand_ind += 1
                continue
            for i in range(len(data)):
                #print('candidate ' + str(cand_ind) + ' has property value ' + data[i]['valueLabel']['value'])
                if data[i]['valueLabel']['value'] not in choices:
                  choices.add(data[i]['valueLabel']['value']) 
                if len(choices) == N_CHOICES:
                    break      
            cand_ind += 1
        else:
            #print('Could not get properties of selected thing')
            break

    #second way: things of the same instance
    if len(choices) < N_CHOICES:
        query = """
        SELECT DISTINCT ?name ?nameLabel WHERE {
          ?other wdt:""" + str(prop_id) + """ ?name.
          ?other rdfs:label ?otherLabel.
          ?name rdfs:label ?nameLabel.
          FILTER(LANG(?nameLabel) = "en").
          FILTER(LANG(?otherLabel) = "en").
        }
        LIMIT """ + str(N_CHOICES)
        r = requests.get(url, params = {'format': 'json', 'query': query})
        if (r.ok):
            data = r.json()['results']['bindings']
            for i in range(len(data)):
                if data[i]['nameLabel']['value'] not in choices:
                    #print('In method 2: distractor ' + str(i) + ' has ' + prop_name + data[i]['nameLabel']['value'])
                    choices.add(data[i]['nameLabel']['value']) 
                if len(choices) == N_CHOICES:
                    break

    #print('Entity:')
    #print(names[ind])

    #print('Property:')
    #print(prop_name)

    #print('Choices:')
    #print(choices)

    #print('Correct answer:')
    #print(correct_answer)

    #print(choices)
    unnumbered = list(choices)
    random.shuffle(unnumbered)
    numbered = [str(i+1) + '. ' + unnumbered[i] for i in range(len(unnumbered))]

    q_generator.q_generate(names[ind], prop_name)

    print(numbered)
    response = input("Enter correct number: ")
    if unnumbered[int(response) - 1] == correct_answer:
        print("Correct!\n")
    else:
        print("Incorrect: answer was " + correct_answer + "\n")
