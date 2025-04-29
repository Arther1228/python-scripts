import pandas as pd
from datetime import datetime, timedelta

# 读取CSV文件
df1 = pd.read_csv('1.csv')
df2 = pd.read_csv('2.csv')

# 转换时间格式 - 解析多种可能的日期格式
def parse_datetime(dt_str):
    try:
        # 尝试解析ISO 8601格式（带Z时区）
        return pd.to_datetime(dt_str, format='ISO8601')
    except ValueError:
        try:
            # 尝试解析"Apr 29, 2025 @ 17:46:49.000"格式
            return pd.to_datetime(dt_str, format='%b %d, %Y @ %H:%M:%S.%f')
        except ValueError:
            # 尝试其他可能的格式
            return pd.to_datetime(dt_str)

df1['createTime'] = df1['createTime'].apply(parse_datetime)
df2['createTime'] = df2['createTime'].apply(parse_datetime)

# 计算时间差（2.csv最后一行 - 1.csv最后一行）
time_diff = df2['createTime'].iloc[-1] - df1['createTime'].iloc[-1]

# 调整df1的时间戳
df1['createTime'] += time_diff

# 合并并排序（降序：最新时间在前）
merged = pd.concat([df1, df2]).sort_values('createTime', ascending=False)

# 交叉合并（interleave）两个数据集
def interleave_dfs(df1, df2):
    # 确保df1是最早开始的（调整后的df1时间应该比df2早）
    min1, min2 = df1['createTime'].min(), df2['createTime'].min()
    if min1 > min2:
        df1, df2 = df2, df1

    # 初始化结果DataFrame
    result = pd.DataFrame(columns=df1.columns)
    i, j = 0, 0
    len1, len2 = len(df1), len(df2)

    while i < len1 and j < len2:
        # 比较当前行的时间戳
        if df1.iloc[i]['createTime'] >= df2.iloc[j]['createTime']:
            result = pd.concat([result, df1.iloc[[i]]])
            i += 1
        else:
            result = pd.concat([result, df2.iloc[[j]]])
            j += 1

    # 添加剩余行
    if i < len1:
        result = pd.concat([result, df1.iloc[i:]])
    if j < len2:
        result = pd.concat([result, df2.iloc[j:]])

    return result.reset_index(drop=True)

# 执行交叉合并
final_merged = interleave_dfs(df1, df2)

# 修正时间格式化：毫秒只保留3位
def format_datetime(dt):
    if pd.isna(dt):
        return ""
    # 格式化为ISO格式，然后处理毫秒部分
    iso_str = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    # 保留3位毫秒
    if '.' in iso_str:
        date_part, ms_part = iso_str.split('.')
        ms_part = ms_part[:3]  # 只取前3位
        iso_str = f"{date_part}.{ms_part}"
    return iso_str + 'Z'

final_merged['createTime'] = final_merged['createTime'].apply(format_datetime)

# 保存结果
final_merged.to_csv('merged_interleaved.csv', index=False)
print("已生成交叉合并的CSV文件：merged_interleaved.csv")