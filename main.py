"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib
import urllib.parse
import urllib.request

api_key = 'AIzaSyATcPty0pvfHl5ro5durFu7cGzjmu0WD90'
query = 'Taylor Swift'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
}
url = service_url + '?' + urllib.parse.urlencode(params)
response = json.loads(urllib.request.urlopen(url).read())
for element in response['itemListElement']:
  print element['result']['name'] + ' (' + str(element['resultScore']) + ')'