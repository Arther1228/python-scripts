import requests
from bs4 import BeautifulSoup
import time
## 2025年1月16日，没有解析出来stock-current节点

def get_stock_price(stock_code):
    url = f"https://quote.eastmoney.com/{stock_code}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find('div', class_='stock-current').text
    return price


if __name__ == "__main__":
    stock_code = "002078"  # 例如贵州茅台
    while True:
        try:
            price = get_stock_price(stock_code)
            print(f" {stock_code} current price: {price}")
        except Exception as e:
            print(f"查询失败: {e}")

        # 每 3 分钟查询一次
        time.sleep(180)  # 180 秒 = 3 分钟
