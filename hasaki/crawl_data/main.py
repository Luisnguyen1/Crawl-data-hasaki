import sys
import os
from hasaki_crawler import HasakiCrawler
import json

if __name__ == "__main__": 
    # data = read_menu_links()
    # print(data)
    url = "https://hasaki.vn/thuong-hieu/kiehl-s.html"
    crawler = HasakiCrawler(url, "products.json")
    product = []
    print(crawler.extract_product_data(product))
    
    crawler.close()