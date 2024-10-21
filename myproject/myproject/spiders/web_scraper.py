import os
import scrapy
import csv
import logging

class LawyerScraperSpider(scrapy.Spider):
    name = 'lawyer_scraper'

    def start_requests(self):
        # Use a set to store visited URLs and ensure unique requests
        visited_urls = set()
        
        # Use the absolute path to the CSV file
        csv_file_path = os.path.join(os.getcwd(), 'lawyers_websites.csv')
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['Website']  # Extract the website URL
                lawyer_name = row['Name']  # Extract the lawyer's name
                
                if url and url not in visited_urls:
                    # Add 'https://' if the URL is missing the scheme
                    if not url.startswith('http'):
                        url = 'https://' + url
                    
                    # Mark the URL as visited
                    visited_urls.add(url)
                    
                    # Send the request
                    yield scrapy.Request(url=url, callback=self.parse, meta={'lawyer_name': lawyer_name})

    def parse(self, response):
        lawyer_name = response.meta['lawyer_name']
        try:
            # Extract the page content
            page_text = response.xpath('//body//text()').getall()
            page_text = ' '.join(page_text).strip()

            yield {
                'lawyer_name': lawyer_name,
                'url': response.url,
                'text': page_text
            }
        except Exception as e:
            logging.error(f"Error scraping {response.url}: {e}")
