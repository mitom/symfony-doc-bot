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
        boost = 1

        # hard code hack to return this for "asset"
        if doc['url'] == 'http://symfony.com/doc/current/book/templating.html#linking-to-assets' and 'asset' not in self['tags']:
            self['tags'].append('asset')
            boost += 0.25

        doc['title'] = self['title'].encode('utf8', 'ignore')
        doc['content'] = self['content'].encode('utf8', 'ignore')
        doc['tags'] = self['tags']
        if '#' not in doc['url']:
            boost += 0.2
        doc['boost'] = boost
        return doc