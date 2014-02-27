Symfony documentation bot
===============
It uses an elastic search backend with the symfony docs re-indexed to allow searching per paragraph and yield more exact results, the solr query however still has room for improvement.


It consists of 2 parts, the scraper, which is a spider written for Scrapy and a plugin for CloudBot. 

##Tagging/boosting results
Specific urls can be tagged by editing the [tags.json](symfony_doc_spider/tags.json), it will be loaded and consumed at *indexing* time.
The format is:
````json
{"url": [0.00, ["tag 1","tag n"]]}
````

Where `url` is the exact link to the section (including the # part), the value assigned to it is an array
that has exactly 2 keys. The first is the `boost` **to be added** to the default/computed one, the second is an array of the `tags` (tags may contain spaces).

The smallest step for boost is 0.05. The boost is applied regardess of the tags, which means if the index is matched for a different reason, the boost specified here will still apply. The `boost` should only be used for articles that are important to show up in their topic.

Changes are welcome to the tags, but will only be accepted if well reasoned and formatted. The tags can not contain
duplicates, including the tags extracted by the scraper (the filename of the link, underscores replaced by spaces).

##Vagrant up!
To run it in Vagrant just cd into the directory and run `vagrant up`. It will try to use `192.168.100.2` as a private ip.
After the vm is up, you will have to edit the config for the bot in `/opt/cloudbot/config`, it is pretty straightforward.
To run the scraping cd into `/vagrant/symfony_doc_spider` and run `scrapy crawl doc`, you can add `-L INFO` for a less verbose output

#####Contributors
- Lumbendil
