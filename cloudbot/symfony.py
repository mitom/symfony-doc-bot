from solr import Solr
from util import hook

@hook.command
@hook.command('sf')
def symfony(inp):
    si = Solr("http://localhost:8080/solr")
    query = createQuery(inp)
    results = si.select('title:%s^20 OR content:%s^10' % (query, query), rows=3).results
    
    if not len(results):
        return "Sorry, seems like I can't help you with that."

    topScore = results[0]['score']
    matches = []
    for result in results:
        if result['score'] + 1 >= topScore:
            matches.append(result['id'])
    
    if len(matches) > 1:
        responseText = "These are the docs I found most relevant to you: %s"
    else:
        responseText = "This is what I found most relevant to you: %s"

    return responseText % ', '.join(matches)

def createQuery(string):
    words = string.split()
    fuzzy = []
    wildcard = []

    for word in words:
        wildcard.append('*%s*' % word)
        fuzzy.append('%s~0.9' % word)

    return '("%s"^10 OR (%s)^8 OR "%s"~4)' % (string, ' AND '.join(fuzzy), string)



