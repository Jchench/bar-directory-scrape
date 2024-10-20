import os
import scrapy
import csv

class LawyerScraperSpider(scrapy.Spider):
    name = 'lawyer_scraper'

    def start_requests(self):
        csv_file_path = os.path.join(os.getcwd(), 'lawyers_websites_short.csv')
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['Website']
                lawyer_name = row['Name']
                
                if url:
                    if not url.startswith('http'):
                        url = 'https://' + url
                    
                    yield scrapy.Request(url=url, callback=self.parse, meta={'lawyer_name': lawyer_name})

    def parse(self, response):
        lawyer_name = response.meta['lawyer_name']
        page_text = response.xpath('//body//text()').getall()
        page_text = ' '.join(page_text).strip()

        yield {
            'lawyer_name': lawyer_name,
            'url': response.url,
            'text': page_text
        }
