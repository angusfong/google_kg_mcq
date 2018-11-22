"""Example of Python client calling Knowledge Graph Search API."""
#types allowed:
#EducationalOrganization, Event, GovernmentOrganization, LocalBusiness, Movie, MovieSeries, MusicAlbum,
#MusicGroup, MusicRecording, Organization,Periodical,Person,Place,SportsTeam,TVEpisode,TVSeries,VideoGame,
#VideoGameSeries,WebSite

import json
import urllib
import urllib.parse
import urllib.request

LIMIT = 100
API_KEY = open('.api_key').read()

query = 'chess'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': LIMIT,
    'indent': True,
    'key': API_KEY,
    'types': 'Movie'
}

url = service_url + '?' + urllib.parse.urlencode(params)
response = json.loads(urllib.request.urlopen(url).read())
for element in response['itemListElement']:
    print(element['result'].keys())
    print(element['result']['@id'])
    print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')

    
