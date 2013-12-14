symfony-doc-bot
===============
It uses an elastic search backend with the symfony docs re-indexed to allow searching per paragraph and yield more exact results, the solr query however still has room for improvement.


It consists of 2 parts, the scraper, which is a spider written for Scrapy and a plugin for CloudBot.

Vagrant up!
===========
To run it in Vagrant just cd into the directory and run `vagrant up`. It will try to use `192.168.100.2` as a private ip.
After the vm is up, you will have to edit the config for the bot in `/opt/cloudbot/config`, it is pretty straightforward.
To run the scraping cd into `/vagrant/symfony_doc_spider` and run `scrapy crawl doc`, you can add `-L INFO` for a less verbose output