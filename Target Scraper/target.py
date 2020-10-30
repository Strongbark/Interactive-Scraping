'''
Script to scrape any products from Target.com
User providesv product they want to scrape and receives product prices. 
'''
import requests
import os
import csv
import time

class TargetScraper:

    #crawl delay defined in redsky's robot.txt
    crawl_delay = 1

    #returns response and prints debug info
    def fetch(self, url):
        res = requests.get(url)
        print(f'HTTP GET request to {res.url} | Status code : {res.status_code}')
        return res

    #returns item string user is searching for
    def item_prompt(self):
        user_search = input('What item would you like to scrape?')
        if ' ' in user_search:
            user_search = user_search.replace(' ', '+')
        return user_search
            
    #implement extraction logic here... all info on products for search term can be found here.
    def get_products(self, product_name):
        #TODO: implement conditional ratings_and_reviews extraction logic
        if ' ' in product_name:
            product_name = product_name.replace(' ', '+')

        product_page_res = self.fetch(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=ff373293829fksdl1&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={product_name}&offset=0&page=%2Fs%2F{product_name}&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Safari&visitor_id=01287beelp')
        try:
            page_json = product_page_res.json()
        except:
            page_json = None
            print('error parsing json')
        
        if page_json:
            #print(page_json)
            #check data needed for pagination
            meta_data_list = page_json['data']['search']['search_response']['meta_data']
            print(meta_data_list)
            try:
                pages_slot = meta_data_list[8]['name']
            except IndexError:
                pages_slot = ''
            print(str(pages_slot))
            if str(pages_slot) == 'totalPages':
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
                next_page_json = next_page_res.json()
                product_list = next_page_json['data']['search']['products']
                for product in product_list:
                    info = {
                    'Title' : product['item']['product_description']['title'],
                    'Price' : product['price']['formatted_current_price'],
                    'URL' : product['item']['enrichment']['buy_url'],

                }
                    self.to_csv(info)
                time.sleep(self.crawl_delay)
            
    def to_csv(self, item):
        # Check if "products.csv" file exists
        csv_exists = os.path.isfile('products.csv')
        # Append data to CSV file
        with open('products.csv', 'a') as csv_file:
            # Init dictionary writer
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            # Write header only ones
            if not csv_exists:
                writer.writeheader()
            # Write entry to CSV file
            writer.writerow(item)

    def run(self):
        while True:
            self.get_products(self.item_prompt())
        
if __name__ == '__main__':
    TS = TargetScraper()
    TS.run()
