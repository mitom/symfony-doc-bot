import elasticutils
import json

class SectionPipeline(object):
    tags = {}

    def open_spider(self, spider):
        self.es = elasticutils.get_es()

        if self.es.indices.exists(index='doc-index'):
            self.es.indices.delete(index='doc-index')

        self.es.indices.create(
            index='doc-index',
            body={
                'mappings': {
                    'doc-section-type': {
                        'analyzer': 'snowball',
                        'url': {'type': 'string'},
                        'tags': {'type': 'string', 'boost': 1.8},
                        'title': {'type': 'string', 'boost': 1},
                        'content': {'type': 'string'},
                        '_boost': {'name': 'boost', 'null_value': 1.0}
                        }
                }
            }
        )

        f = open('tags.json', 'r')
        self.tags = json.loads(f.read())

    def process_item(self, item, spider):
        # default boost
        item.setdefault('boost', 1)

        # if there is no content it is probably (hopefully) a section with only config/code in it
        if item['content']== '':
            item['content'] = 'config code reference'

        extracted = item.extract()

        if extracted['url'] in self.tags:
            data = self.tags[extracted['url']]
            for tag in data[0]:
                item.add_tag(tag)
            item['boost'] += data[1]

        # extract the new dataset
        extracted = item.extract()

        self.es.index(index='doc-index', doc_type='doc-section-type', body=extracted, id=extracted['url'])

        return item