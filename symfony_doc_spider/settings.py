# Scrapy settings for symfony_doc_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'symfony_doc_spider'

SPIDER_MODULES = ['symfony_doc_spider.spiders']
NEWSPIDER_MODULE = 'symfony_doc_spider.spiders'
ITEM_PIPELINES = {
    'symfony_doc_spider.pipelines.SectionPipeline': 300
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'symfony_doc_spider (+http://www.yourdomain.com)'
