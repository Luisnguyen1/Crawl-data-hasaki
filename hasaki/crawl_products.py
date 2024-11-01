import sys
import os
from crawl_data.hasaki_crawler import HasakiCrawler
import json

menu_links_path = "data/menu_links.json"

# Function to read data from menu_links.json
def read_menu_links():
    with open(menu_links_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

if __name__ == "__main__": 
    # data = read_menu_links()
    # print(data)
    url = "https://hasaki.vn/danh-muc/toner-c1857.html"
    crawler = HasakiCrawler(url, "data/products.json")