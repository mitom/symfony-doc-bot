import elasticutils

class SectionPipeline(object):
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

    def process_item(self, item, spider):
        # if there is no content it is probably (hopefully) a section with only config/code in it
        if item['content']== '':
            item['content'] = 'config code reference'

        self.es.index(index='doc-index', doc_type='doc-section-type', body=item.extract(), id=item.extract()['url'])

        return item