# -*- coding: utf-8 -*-
import requests

def download_cnblogs_bookmarks(api_url, page_index, page_size, output_file):
    # 构建请求URL
    url = f'{api_url}?pageIndex={page_index}&pageSize={page_size}'

    # 发送GET请求
    response = requests.get(url)

    # 获取收藏列表
    bookmarks = response.json()

    # 写入文件
    with open(output_file, 'a') as file:
        for index, bookmark in enumerate(bookmarks, start=1):
            title = bookmark['Title']
            link_url = bookmark['LinkUrl']
            line = f'{index}.{title} {link_url}\n'
            file.write(line)

if __name__ == "__main__":
    # 替换成你的API地址、页码、页容量
    api_url = 'https://api.cnblogs.com/api/Bookmarks'
    page_index = 1
    page_size = 10

    # 替换成你希望保存的文件名
    output_filename = 'output.txt'

    # 分页下载收藏列表并写入文件
    while True:
        download_cnblogs_bookmarks(api_url, page_index, page_size, output_filename)
        page_index += 1

        # 假设每页都有数据，如果一页不满 pageSize 条，表示已经获取完所有收藏
        if len(bookmarks) < page_size:
            break
