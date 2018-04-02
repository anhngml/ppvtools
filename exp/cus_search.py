import json
import urllib
import urllib.parse
import urllib.request

# AIzaSyC6sUvsaqB7GW7U8xmhKegpWfyLAcXVs1g


def showsome(searchfor):
    query = urllib.parse.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read()
    print(search_results)
    results = json.loads(search_results)
    data = results['responseData']
    print('Total results: %s' % data['cursor']['estimatedResultCount'])
    hits = data['results']
    print('Top %d hits:' % len(hits))
    for h in hits:
        print(' ', h['url'])
    print('For more results, see %s' % data['cursor']['moreResultsUrl'])


showsome('ermanno olmi')
