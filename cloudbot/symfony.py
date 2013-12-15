from util import hook
import elasticutils
from elasticutils import S

@hook.command
@hook.command('sf')
def symfony(inp):
    if not elasticutils.get_es().indices.exists('doc-index'):
        return "Index currently unavailable. Try again in a bit."

    search = S().indexes('doc-index').doctypes('doc-section-type')
    # cant fit more than 3 links into 1 irs message
    results = search.query(tags__match=inp, title__match=inp, content__match=inp, should=True)[:3].execute()

    if not len(results):
        return "Sorry, seems like I can't help you with that."

    topScore = results.results[0]['_score']
    matches = []
    print topScore
    for result in results:
        if result._score + 1 >= topScore:
            matches.append(result.id)
    
    if len(matches) > 1:
        responseText = "These are the docs I found most relevant for you: %s"
    else:
        responseText = "This is what I found most relevant for you: %s"

    return responseText % ', '.join(matches)