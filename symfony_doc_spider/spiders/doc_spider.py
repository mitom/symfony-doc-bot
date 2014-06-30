from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
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
        "http://symfony.com/doc/current/cookbook/index.html",
        "http://symfony.com/doc/current/components/index.html",
        "http://symfony.com/doc/current/bundles/index.html"
    ]

    rules = (
        Rule(SgmlLinkExtractor(
            process_value=parseLink,
            restrict_xpaths="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' page ')]//a[@class='reference internal']"
        ), callback='parseArticle', follow=True, process_links=True),
    )

    def parseArticle(self, response):
        sel = Selector(response)
        # Select the document holder
        sel = sel.css('div.page')
        # Needed to properly match the section headers (h1, h2...)
        depth = 1
        items = []

        # Traverse every first level section
        for section in sel.xpath('div[@class="section"]'):
            items = items + self.parseSection(response, section, depth)

        return items
descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' doc_page ')]//a[@class='reference internal']
    def parseSection(self, response, section, depth):
        item = SectionItem()
        items = []

        # split the url to get the *.html part then split it again to remove everything after the last dot
        parsedUrl = response.url.replace('http://symfony.com/doc/current/', '').split('/')
        # remove the category
        parsedUrl.pop(0)
        if "index.html" == parsedUrl[-1]:
            return []

        if parsedUrl[-1] != parsedUrl[0]:
            item['folder'] = parsedUrl[0]
            if "introduction.html" == parsedUrl[-1]:
                item.add_tag(parsedUrl[0])

        item['article'] = parsedUrl[-1].rsplit('.', 1)[0]

        # When the depth is 1 we are parsing the main header of the page,
        # therefore we don't need the # part
        if depth == 1:
            item['id'] = response.url
        else:
            # absolute url to the section (granted to be unique)
            item['id'] = response.url+ '#' + section.xpath('@id').extract()[0]


        # header of the section
        item['title'] = section.xpath("h%d//text()" % depth).extract()[0]

        # The text of the section html, whitespace stripped and single lined
        content = ' '.join(section.xpath('p//text()').extract()).strip().replace('\n', ' ')
        # The text of the notes html, whitespace stripped and single lined
        content += ' '.join(section.xpath('div[@class="admonition-wrapper" and not(@id)]//p//text()').extract()).strip().replace('\n', ' ')
        item['content'] = content

        items = items + self.parseAdmonitionAnchors(response.url, item, section)
        # add the section to the items
        items.append(item)

        # Traverse every next level section
        depth += 1
        for subSection in section.xpath('div[@class="section"]'):
            items = items + self.parseSection(response, subSection, depth)

        return items

    def parseAdmonitionAnchors(self, baseUrl, parent, section):
        items = []

        for admonition in section.xpath('div[@class="admonition-wrapper" and @id]'):
            item = SectionItem()
            # absolute url to the section (granted to be unique)
            item['id'] = baseUrl+ '#' + admonition.xpath('@id').extract()[0]
            item['article'] = parent['article']
            if 'folder' in parent:
                item['folder'] = parent['folder']
            # header of the section, it must be joined due to the tags inside it
            item['title'] = ''.join(admonition.xpath('*/p[contains(@class, "sidebar-title")]//text()').extract()).strip()
            # The text of the section html, whitespace stripped and single lined
            item['content'] = ' '.join(admonition.xpath('*/p[not(contains(@class, "title"))]//text()').extract()).strip().replace('\n', ' ')
            items.append(item)

        return items
