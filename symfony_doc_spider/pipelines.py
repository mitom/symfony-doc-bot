import elasticutils

class SectionPipeline(object):
    def __init__(self):
        self.es = elasticutils.get_es()


    def open_spider(self, spider):
        if not self.es.indices.exists('doc-index'):
            self.es.indices.create(
                index='doc-index',
                body={
                    'mappings': {
                        'doc-section-type': {
                            'id': {'type': 'string', 'boost': 5},
                            'tags': {'type': 'string', 'boost': 4, 'index_name': 'tag'},
                            'title': {'type': 'string', 'boost': 3},
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

    def close_spider(self, spider):
        self.es.flush()
