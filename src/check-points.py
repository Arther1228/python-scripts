import cx_Oracle

# Oracle数据库连接信息
oracle_username = 'your_username'
oracle_password = 'your_password'
oracle_host = 'your_host'
oracle_port = 'your_port'
oracle_service_name = 'your_service_name'

# 连接到Oracle数据库
connection = cx_Oracle.connect(
    user=oracle_username,
    password=oracle_password,
    dsn=f"{oracle_host}:{oracle_port}/{oracle_service_name}"
)

# 创建游标
cursor = connection.cursor()

# 指定表名
table_name = 'your_table_name'

# 查询数据
query = f"SELECT camera_name, camera_code, longitude, latitude FROM {table_name}"
cursor.execute(query)

# 定义安徽省合肥市的经纬度范围
anhui_range = {
    'min_longitude': 115.5,
    'max_longitude': 117.5,
    'min_latitude': 31.5,
    'max_latitude': 33.5
}

# 打开输出文件
output_file = open('output.txt', 'w')

# 遍历数据并判断经纬度范围
for row in cursor:
    camera_name, camera_code, longitude, latitude = row
    if (
        anhui_range['min_longitude'] <= longitude <= anhui_range['max_longitude'] and
        anhui_range['min_latitude'] <= latitude <= anhui_range['max_latitude']
    ):
        # 在安徽省合肥市经纬度范围内
        continue
    else:
        # 不在范围内，写入输出文件
        output_str = f"{camera_name}, {camera_code}, {longitude}, {latitude}\n"
        output_file.write(output_str)

# 关闭文件和数据库连接
output_file.close()
cursor.close()
connection.close()
