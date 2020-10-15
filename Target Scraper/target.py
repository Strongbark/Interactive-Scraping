'''
Script to scrape any products from Target.com
User provides string of product they want to scrape and receives product info. 
'''

#TODO: pagination

import requests
from bs4 import BeautifulSoup
import json
import ast
import urllib
import os
import csv
import time

class TargetScraper:

    #crawl delay defined in redsky's robot.txt
    crawl_delay = 1

    #returns item id for item user searches for
    def prompt(self):
        item_id = ''
        user_search = input('What item would you like to scrape?')
        if ' ' in user_search:
            user_search = user_search.replace(' ', '+')
        term_page_res = self.fetch(f'https://typeahead.target.com/autocomplete/TypeAheadSearch/v2?q={user_search}&ctgryVal=0%7CALL%7Cmatchallpartial%7Call+categories&channel=web&visitor_id=bleemblam289')
        content = BeautifulSoup(term_page_res.text, 'lxml')
        try:
            page_content = json.loads(content.text)
        except:
            page_content = None
        else:
            try:
                item_id = str(page_content['suggestions'][0]['subResults'][0]['id'])
            except:
                item_id = ''
        return item_id

    #returns item string user is searching for
    def item_prompt(self):
        user_search = input('What item would you like to scrape?')
        if ' ' in user_search:
            user_search = user_search.replace(' ', '+')
        return user_search
    
    #used to get products from a category (item id)
    def get_redsky_products(self, item_id):
        res = self.fetch(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=bleemfdskj8&category={item_id}&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&offset=0&page=%2Fc%2F5xtlx&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Mozilla%2F5.0++cko&visitor_id=8977')
        content = BeautifulSoup(res.text, 'lxml')
        try:
            page_json = json.loads(content.text)
        except:
            page_json = None
        if page_json:
            product_list = page_json['data']['search']['products']
            print(product_list)
            
    #implement extraction logic here... all info on products for search term can be found here.
    def get_products(self, product_name):
        if ' ' in product_name:
            product_name = product_name.replace(' ', '+')

        product_page_res = self.fetch(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=ff373293829fksdl1&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={product_name}&offset=0&page=%2Fs%2F{product_name}&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Safari&visitor_id=01287beelp')
        content = BeautifulSoup(product_page_res.text, 'lxml')
        page_text = content.text
        try:
            page_json = json.loads(page_text)
        
        except:
            page_json = None
            print('error parsing json')
        
        if page_json:
            #check data needed for pagination
            meta_data_list = page_json['data']['search']['search_response']['meta_data']
            if meta_data_list[8]['name'] == 'totalPages':
                total_pages = meta_data_list[8]['value']
            else:
                total_pages = 0
            print(f'Total pages: {str(total_pages)}')

            product_list = page_json['data']['search']['products']
            #print(product_list)
            for product in product_list:
                info = {
                    'Title' : product['item']['product_description']['title'],
                    'Price' : product['price']['formatted_current_price'],
                    'URL' : product['item']['enrichment']['buy_url'],

            }
                self.to_csv(info)
            offset = 0
            for offset in range(24, int(total_pages) * 24, 24):
                print(offset)
                next_page_res = self.fetch(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=ff373293829fksdl1&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={product_name}&offset={offset}&page=%2Fs%2F{product_name}&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Safari&visitor_id=01287beelp')
                next_page_content = BeautifulSoup(next_page_res.text, 'lxml')
                next_page_json = json.loads(next_page_content.text)
                product_list = next_page_json['data']['search']['products']
                for product in product_list:
                    info = {
                    'Title' : product['item']['product_description']['title'],
                    'Price' : product['price']['formatted_current_price'],
                    'URL' : product['item']['enrichment']['buy_url'],

                }
                    self.to_csv(info)
                time.sleep(0.5)
            
    #returns response and prints debug info
    def fetch(self, url):
        res = requests.get(url)
        print(f'HTTP GET request to {res.url} | Status code : {res.status_code}')
        return res

    def to_csv(self, item):
        # Check if "wine.csv" file exists
        wine_exists = os.path.isfile('products.csv')
        # Append data to CSV file
        with open('products.csv', 'a') as csv_file:
            # Init dictionary writer
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            # Write header only ones
            if not wine_exists:
                writer.writeheader()
            # Write entry to CSV file
            writer.writerow(item)

    def run(self):
        while True:
            self.get_products(self.item_prompt())
        
if __name__ == '__main__':
    TS = TargetScraper()
    TS.run()
