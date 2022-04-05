import html
import re

import scrapy
from question_3.items import ArtItem, clean_list, find_dim_element, find_media
from scrapy.loader import ItemLoader


class BearspaceSpider(scrapy.Spider):
    name = 'bearspace'
    allowed_domains = ['bearspace.co.uk']
    start_urls = ['http://bearspace.co.uk/purchase?page=1000']

    def parse(self, response):
        '''Extracts and iterates through all product links from expanded product
            purchase page and calls parse listing function'''

        links = response.xpath(
            '//a[@data-hook="product-item-container"]/@href').getall()
        for url in links:
            yield scrapy.Request(url, callback=self.parse_listing)

    def parse_listing(self, response):
        '''Extracts target data from product listing page and yields loaded item'''

        # parse text from description collect all items in list
        desc_sel = response.xpath('//pre[@data-hook="description"]')
        if '<div>' in desc_sel:
            raw_list = desc_sel.xpath('.//div/div/p/text()').getall()
        elif '<p>' in desc_sel:
            raw_list = desc_sel.xpath('.//p/text()').getall()
        elif '<span>' in desc_sel:
            raw_list = desc_sel.xpath('.//p/span/text()').getall()
        else:
            raw_list = desc_sel.xpath('.//text()').getall()

        # clean and reduce description text
        text_list = clean_list(raw_list)

        # compile regex to find dimensions
        search_dmns = re.compile(r'(\d\s*[cCxX]+)')
        find_dmsn = re.compile(r'[^\d+]*(\d+\.*\d*)+')

        # find dimensions
        dimensions, position = find_dim_element(
            search_dmns, find_dmsn, text_list)

        # assign height/width dimensions
        if len(dimensions) > 1:
            height_cm = dimensions[0]
            width_cm = dimensions[1]
        else:
            # width == height for diameter
            height_cm = dimensions[0]
            width_cm = dimensions[0]

        # find media data relative to dimensions in text_list
        media = find_media(position, text_list)

        # initiate ArtItem, load and yield data
        art_item = ItemLoader(item=ArtItem(), response=response)
        art_item.add_value('url', response.url)
        art_item.add_xpath('title', '//h1[@data-hook="product-title"]/text()')
        art_item.add_value('media', media)
        art_item.add_value('height_cm', height_cm)
        art_item.add_value('width_cm', width_cm)
        art_item.add_xpath(
            'price_gbp', '//meta[@property="product:price:amount"]/@content')

        yield art_item.load_item()
