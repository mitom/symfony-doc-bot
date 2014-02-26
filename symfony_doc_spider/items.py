# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import re

class SectionItem(Item):
    id = Field()
    title = Field()
    content = Field()
    tags = Field()
    boost = Field()

    def add_tag(self, tag):
        if tag not in self['tags']:
            self['tags'].append(tag)

    def extract(self):
        doc = {}
        doc['url'] = self['id'].encode('utf8', 'ignore')
        doc['category'] = re.compile('/current/[a-z]+/').search(doc['url']).group().split('/')[2]
        doc['boost'] = self['boost']
        doc['title'] = self['title'].encode('utf8', 'ignore')
        doc['content'] = self['content'].encode('utf8', 'ignore')
        doc['tags'] = self['tags']
        if '#' not in doc['url']:
            doc['boost'] += 0.2
        return doc