"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib
import urllib.parse
import urllib.request

api_key = open('.api_key').read()
query = 'Taylor Swift'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
    'types': 'Person'
}
url = service_url + '?' + urllib.parse.urlencode(params)
response = json.loads(urllib.request.urlopen(url).read())
for element in response['itemListElement']:
    print(element.keys())
    print(element['result'].keys())
    print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')
