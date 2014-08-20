from util import hook
import elasticutils
import re

@hook.command
@hook.command('sf')
def symfony(inp):
    help = "The syntax is: !sf [category] <search term> - Omitted category matches all"
    if not elasticutils.get_es().indices.exists('doc-index'):
        return "Index currently unavailable. Try again in a bit."

    if '' == inp:
        return help

    category = re.compile('\[[a-z]+\]').match(inp)
    search = elasticutils.S().indexes('doc-index').doctypes('doc-section-type')
    if category:
        category = category.group()
        inp = inp.replace(category, '').strip()
        if '' == inp :
            return help
        search = search.query(category__prefix=category.replace('[', '').replace(']', ''))

    # cant fit more than 3 links into 1 irc message
    results = search.query(tags__match=inp, article__match=inp, folder__match=inp, title__match=inp, content__match=inp, should=True)[:3].execute()

    if not len(results):
        return "Sorry, seems like I can't help you with that."

    topScore = results.results[0]['_score']
    matches = []
    for result in results.results:
        if result['_score'] + 0.5 >= topScore:
            matches.append(result['_source']['url'])
        # left in for debug
        #matches.append(str(result['_score']) + ' - ' + result['_source']['url'])

    if len(matches) > 1:
        responseText = "These are the docs I found most relevant for you: %s"
    else:
        responseText = "This is what I found most relevant for you: %s"

    return responseText % ', '.join(matches)