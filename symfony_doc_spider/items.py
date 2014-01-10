# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SectionItem(Item):
    id = Field()
    title = Field()
    content = Field()
    tags = Field()

    def extract(self):
        doc = {}
        doc['url'] = self['id'].encode('utf8', 'ignore')
        doc['title'] = self['title'].encode('utf8', 'ignore')
        doc['content'] = self['content'].encode('utf8', 'ignore')
        doc['tags'] = self['tags']
        if '#' not in doc['url']:
            doc['boost'] = 1.5

        return doc