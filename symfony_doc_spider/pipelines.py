from solr import Solr

class SectionPipeline(object):
    def __init__(self):
        self.db = Solr("http://localhost:8080/solr")

    def process_item(self, item, spider):
        # if there is no content it is probably (hopefully) a section with only config/code in it
        if item['content']== '':
            item['content'] = 'config code reference'
        self.db.add(item)

        return item

    def close_spider(self, spider):
        self.db.commit()