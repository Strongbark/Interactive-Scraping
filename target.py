import requests
from bs4 import BeautifulSoup
import json

#category matters and thats it
'''
https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=bleemblam&category=5xtlx&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&offset=0&page=%2Fc%2F5xtlx&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Mozilla%2F5.0++Gecko&visitor_id=jklykhj

'''

class TargetScraper:

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

    def item_prompt(self):
        user_search = input('What item would you like to scrape?')
        if ' ' in user_search:
            user_search = user_search.replace(' ', '+')
        return user_search

    '''
    https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=bleemfdskj8&category={item_id}&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&offset=0&page=%2Fc%2F5xtlx&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Mozilla%2F5.0++cko&visitor_id=8977
    '''
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

    '''
    https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=ff373293829fksdl1&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword=toilet+paper&offset=0&page=%2Fs%2F{product_name}&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Safari&visitor_id=01287beelp
    '''
    def get_products(self, product_name):
        if ' ' in product_name:
            product_name = product_name.replace(' ', '+')
    
        product_page_res = self.fetch(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?key=ff373293829fksdl1&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={product_name}&offset=0&page=%2Fs%2F{product_name}&platform=desktop&pricing_store_id=2105&store_ids=2105%2C1971%2C922%2C350%2C1465&useragent=Safari&visitor_id=01287beelp')
        content = BeautifulSoup(product_page_res.text, 'lxml')
        try:
            page_json = json.loads(content.text)
        except:
            page_json = None
        if page_json:
            product_list = page_json['data']['search']['products']
            print(product_list)
    
    def fetch(self, url):
        res = requests.get(url)
        print(f'HTTP GET request to {res.url} | Status code : {res.status_code}')
        return res

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        pch = content.find('div', {'data-test' : 'product-card-hardlines'})
        print(pch)

    def run(self):
        while True:
            self.get_products(self.item_prompt())
        
if __name__ == '__main__':
    TS = TargetScraper()
    TS.run()