from util import hook
from elasticutils import S


@hook.command
@hook.command('sf')
def symfony(inp):
    search = S()
    results = search.query(content__text=inp)[:5].execute()

    if not len(results):
        return "Sorry, seems like I can't help you with that."

    topScore = results.results[0]['_score']
    matches = []
    print topScore
    for result in results:
        if result._score + 1 >= topScore:
            matches.append(result.id)
    
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



