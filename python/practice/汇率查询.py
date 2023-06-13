# import requests
# import json

# def get_exchange_rate():
#     url = "https://api.exchangerate-api.com/v4/latest/USD"
#     response = requests.get(url)
#     data = json.loads(response.text)
#     exchange_rate = data["rates"]["CNY"]
#     return exchange_rate

# usd_cny_rate = get_exchange_rate()

# print("美元兑人民币汇率：1美元 = " + str(usd_cny_rate) + "人民币")


import requests
from bs4 import BeautifulSoup

def get_stock_index():
    url = 'https://www.sse.com.cn/market/sseindex/indexlist/index.shtml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    index_table = soup.find('table', class_='table-index')
    
    index_name = index_table.find('td', string='上证指数').find_next_sibling('td').text
    index_value = index_table.find('td', string='上证指数').find_next_sibling('td').find_next_sibling('td').text
    
    return index_name, index_value

index_name, index_value = get_stock_index()
print(f'{index_name}: {index_value}')
