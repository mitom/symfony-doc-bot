#!/usr/bin/env bash

echo "--> Installing dependencies for scrapy/elasticutils"
sudo apt-get install -y zlib1g-dev libxslt1-dev libxml2-dev python-pip python-dev

echo "--> Installing scrapy"
sudo pip install scrapy

echo "--> Installing elasticutils"
sudo pip install elasticutils