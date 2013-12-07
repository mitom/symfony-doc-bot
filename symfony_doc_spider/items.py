# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SectionItem(Item):
    id = Field()
    title = Field()
    content = Field()

    pass
