from typing import Iterable

import scrapy
from curl_cffi import requests as curl_requests
from scrapy import Request
from app.products.models import Product, Brand
from twisted.internet import reactor, defer
from scrapy.http import HtmlResponse

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'max-age=0',
  'device-memory': '8',
  'downlink': '9.5',
  'dpr': '1',
  'ect': '4g',
  'priority': 'u=0, i',
  'rtt': '200',
  'sec-ch-device-memory': '8',
  'sec-ch-dpr': '1',
  'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-ch-viewport-width': '1920',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
  'viewport-width': '1920'
}



class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 2,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 60,
        "CONCURRENT_REQUESTS": 1,
        "COOKIES_ENABLED":True
    }

    def __init__(self, start_urls=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.urls = start_urls if start_urls else []

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url,headers=headers)

    def parse(self, response):
        products = response.xpath(
            '//div[@class="s-main-slot s-result-list s-search-results sg-row"]//div[@data-component-type="s-search-result"]')
        brand = Brand.objects.get(url=response.url)
        for product in products:
            product_url = product.xpath(
                './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//@href').get()
            product_data = {
                "title": product.xpath('.//h2//text()').get(),
                "asin": product_url.split('/')[-1],
                "image_url": product.xpath(
                    './/div[@class="a-section aok-relative s-image-square-aspect"]//img/@src').get(),
                "product_url": 'https://www.amazon.com' + product_url
            }
            created, _ = Product.objects.get_or_create(asin=product_data['ASIN'], defaults={**product_data, "brand": brand})
            yield created, product_data
        next_page = response.xpath(
            '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()

        # if next_page:
        #     yield response.follow(next_page, headers=headers)

    def parse_listing(self, response):
        pass




