import akshare as ak
import time

def get_stock_price(stock_code):
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    stock_info = stock_zh_a_spot_df[stock_zh_a_spot_df["代码"] == stock_code]
    if not stock_info.empty:
        return stock_info.iloc[0]["最新价"]
    else:
        return "未找到股票信息"

if __name__ == "__main__":
    stock_code = "002078"  # 例如太阳纸业
    while True:
        try:
            price = get_stock_price(stock_code)
            print(f"股票代码 {stock_code} 的当前价格是: {price}")
        except Exception as e:
            print(f"查询失败: {e}")

        # 每 3 分钟查询一次
        time.sleep(180)  # 180 秒 = 3 分钟