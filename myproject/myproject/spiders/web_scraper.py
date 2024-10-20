import os
import scrapy
import csv

class LawyerScraperSpider(scrapy.Spider):
    name = 'lawyer_scraper'

    def start_requests(self):
        # Use the absolute path to the CSV file
        csv_file_path = os.path.join(os.getcwd(), 'lawyers_websites_short.csv')
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['Website']  # Extract the website URL
                lawyer_name = row['Name']  # Extract the lawyer's name
                
                if url:
                    # Add 'https://' if the URL is missing the scheme
                    if not url.startswith('http'):
                        url = 'https://' + url
                    
                    yield scrapy.Request(url=url, callback=self.parse, meta={'lawyer_name': lawyer_name})

    def parse(self, response):
        # Extract the text content from the website
        lawyer_name = response.meta['lawyer_name']
        page_text = response.xpath('//body//text()').getall()
        page_text = ' '.join(page_text).strip()

        yield {
            'lawyer_name': lawyer_name,
            'url': response.url,
            'text': page_text
        }
