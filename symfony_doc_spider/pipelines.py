import elasticutils
import json
import os

class SectionPipeline(object):
    tags = {}

    def open_spider(self, spider):
        self.es = elasticutils.get_es()

        if self.es.indices.exists(index='doc-index'):
            self.es.indices.delete(index='doc-index')

        self.es.indices.create(
            index='doc-index',
            body={
                'settings': {
                    'analysis': {
                        'filter': {
                            'en_stop_filter': {'type': 'stop', 'stopwords': ['_english_']},
                            'en_stem_filter': {'type': 'stemmer', 'name': 'minimal_english'},
                            'synonym': {'type': 'synonym', 'synonyms_path': os.path.abspath('synonym.txt')}
                        },
                        'analyzer': {
                            'en_analyzer': {
                                'type': 'custom',
                                'tokenizer': 'lowercase',
                                'filter': ['asciifolding', 'word_delimiter', 'en_stop_filter', 'en_stem_filter', 'synonym']
                            }
                        }
                    },
                },
                'mappings': {
                    'doc-section-type': {
                        'analyzer': 'en_analyzer',
                        'url': {'type': 'string'},
                        'category': {'type': 'string'},
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
            item['boost'] += data[0]
            for tag in data[1]:
                item.add_tag(tag)

        # extract the new dataset
        extracted = item.extract()

        self.es.index(index='doc-index', doc_type='doc-section-type', body=extracted, id=extracted['url'])

        return item