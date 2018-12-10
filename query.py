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
import get_wikidata

LIMIT = 100 #this many?
API_KEY = open('.api_key').read()

#prompt user to input topic of interest (easy for debugging)
query = input("Topic of interest: ")
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': LIMIT,
    'indent': True,
    'key': API_KEY,
    'types': 'Person'
}

url = service_url + '?' + urllib.parse.urlencode(params)

#loop until successfully get response (might take some time depending on server)
while True:
    try:
        response = json.loads(urllib.request.urlopen(url).read())
        break
    except Exception: # still allows to quit with KeyboardInterrupt
        continue


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
probs = [score/sum(scores) for score in scores]
n = len(scores)

#stay on topic before user terminates
while True:
    ind = np.random.choice(n, p=probs)
    id = ids[ind]
    get_wikidata.get_wikidata(id)
