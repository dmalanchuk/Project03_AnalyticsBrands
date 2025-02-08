import requests
import pandas as pd
import json
from bs4 import BeautifulSoup



url = "https://ua.puma.com/uk/sportivnye-tovary-dlja-muzhchin.html"

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

# url_categories = "https://ua.puma.com/uk/sportivnye-tovary-dlja-muzhchin.html?article_type="

categories_word_arr = ["sneakers", "hoodies", "pants", "jacket", "down", "boots"]
# full_req_arr = []

# for i in categories_word_arr:
#     full_req = url_categories + i
#     full_req_arr.append(full_req)
    
# with open("data_sources/raw_data/index.json", "w") as file:
#     json.dump(full_req_arr, file, indent=4)

# categories = []
 
# req = requests.get(url, headers=headers)
# if req.status_code == 200:
#     soup = BeautifulSoup(req.text, "html.parser")
    
    
#     category_list = soup.find("div", class_="filter-block filter-type-article_type _active")
#     if category_list:
#         order_list_categories = category_list.find("ol", class_="items filter-items")        
        
#         if order_list_categories:
#             all_li_category = order_list_categories.find_all("li", class_="item filter-items__item")
            
#             for li in all_li_category:
#                 link = li.find("a", class_="filter-items__item-link")
#                 if link:
#                     category_name = link.find("span", class_="filter-items__item-input-text checkbox-block__text")
#                     src = category_name.text.strip()
#                     categories.append(src)
                        
    
# if categories:
#     df = pd.DataFrame(categories, columns=["categories"])
#     df.to_excel("data_sources/raw_data/categories.xlsx", index=False)
    
# products_data = []

# for url in urls_category:
#     req = requests.get(url, headers=headers)
#     req.raise_for_status() 

#     if req.status_code == 200:
#         soup = BeautifulSoup(req.text, "html.parser")

#         main_block_all_items = soup.find_all("div", class_='grid__item image-sv01')

#         if main_block_all_items:
#             for item in main_block_all_items:
#                 name_item = item.find("div", class_="product-item__name-w")
#                 price_item = item.find("span", class_="price")

#                 if name_item and price_item:
#                     products_data.append({
#                         "Назва товару": name_item.text.strip(),
#                         "Ціна": price_item.text.strip(),
#                         "URL сторінки": url
#                     })
                        
# if products_data:
#     df = pd.DataFrame(products_data)
#     df.to_excel("data_sources/raw_data/products_data.xlsx", index=False) 
#     print("Дані успішно збережені у файл 'products_data.xlsx'!")

with open("data_sources/raw_data/index.json") as f:
    urls_category = json.load(f)
    
    
all_item_categories = []    
for idx, urls in enumerate(urls_category):
    respone = requests.get(urls, headers=headers)
    
    if respone.status_code == 200:
        soup = BeautifulSoup(respone.text, "html.parser")
        
        main_block = soup.find("div", class_="grid")
        
        if main_block:
            all_block_item = main_block.find_all("div", class_="grid__item")
                
            if all_block_item:
                category = categories_word_arr[idx % len(categories_word_arr)]
                
                for item in all_block_item:
                    name_item = item.find("a", class_="product-item__name")
                    price_item = item.find("span", class_="price")
                    
                    if name_item and price_item:
                        # print(f"{name_item.text.strip()} - {price_item.text.strip()}")
                        
                        all_item_categories.append({
                            "category": category,
                            "name": name_item.text.strip(),
                            "price": price_item.text.strip()
                        })
                    else:
                        print("item is not find")
                        
if all_item_categories:
    df = pd.DataFrame(all_item_categories)
    df.to_excel("data_sources/raw_data/all_products.xlsx",  index=False)
    print("successfuly!")
