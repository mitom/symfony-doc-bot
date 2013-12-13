import elasticutils

class SectionPipeline(object):
    def open_spider(self, spider):
        self.es = elasticutils.get_es()
        if not self.es.indices.exists('doc-index'):
            self.es.indices.create(
                index='doc-index',
                body={
                    'mappings': {
                        'doc-section-type': {
                            'id': {'type': 'string', 'boost': 10},
                            'tags': {'type': 'string', 'boost': 8},
                            'title': {'type': 'string', 'boost': 4},
                            'content': {'type': 'string'},
                            }
                    }
                }
            )

    def process_item(self, item, spider):
        # if there is no content it is probably (hopefully) a section with only config/code in it
        if item['content']== '':
            item['content'] = 'config code reference'

        self.es.index(index='doc-index', doc_type='doc-section-type', body=item.extract(), id=item.extract()['id'])

        return item