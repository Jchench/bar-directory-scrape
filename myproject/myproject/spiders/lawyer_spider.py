import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LawyerSpider(CrawlSpider):
    name = "lawyer_spider"
    start_urls = ['https://gerstein-harrow.com/charlie-gerstein'] 
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    

    def parse_item(self, response):
        license_number = response.xpath('//div[@class="license"]/text()').get()  
        html_content = response.body.decode('utf-8')

        yield {
            'LicenseNumber': license_number,
            'HTML': html_content,
            'URL': response.url
        }
