from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from symfony_doc_spider.items import SectionItem

class DocSpider(CrawlSpider):
    def parseLink(value):
        # only follow links to the current link
        if (value.startswith('../')):
            return None
        return value

    name = "doc"

    allowed_domains = ["symfony.com"]
    start_urls = [
        "http://symfony.com/doc/current/reference/index.html",
        "http://symfony.com/doc/current/book/index.html",
        "http://symfony.com/doc/current/cookbook/index.html"
    ]
    items = []

    rules = (
        Rule(SgmlLinkExtractor(
            process_value=parseLink,
            restrict_xpaths="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' doc_page ')]//a[@class='reference internal']"
        ), callback='parseArticle', follow=True, process_links=True),
    )

    def parseArticle(self, response):
        sel = Selector(response)
        # Select the document holder
        sel = sel.css('div.doc_page')
        # Needed to properly match the section headers (h1, h2...)
        depth = 1

        # Traverse every first level section
        for section in sel.xpath('div[@class="section"]'):
            self.parseSection(response, section, depth)
            break

        return self.items

    def parseSection(self, response, section, depth):
        item = SectionItem()

        # absolute url to the section (granted to be unique)
        item["id"] = response.url+ '#' + section.xpath('@id').extract()[0]
        # header of the section
        item["title"] = section.xpath("h%d//text()" % depth).extract()[0]
        # The text of the section html, whitespace stripped and single lined
        content = ' '.join(section.xpath('p//text()').extract()).strip().replace('\n', ' ')
        # The text of the notes html, whitespace stripped and single lined
        content += ' '.join(section.xpath('div[@class="admonition-wrapper"]//p[@class="last"]//text()').extract()).strip().replace('\n', ' ')
        item["content"] = content

        # add the section to the items
        self.items.append(item)

        # Traverse every next level section
        depth += 1
        for subSection in section.xpath('div[@class="section"]'):
            self.parseSection(response, subSection, depth)
            return
