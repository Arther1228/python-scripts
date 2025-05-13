import os
import json
from pathlib import Path


def extract_json_from_logs(input_dir, output_dir):
    """
    从日志文件中提取JSON数据

    :param input_dir: 输入目录(包含.log文件)
    :param output_dir: 输出目录(保存提取的JSON)
    """
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 获取所有日志文件
    log_files = [f for f in Path(input_dir).glob('*.log') if f.is_file()]

    if not log_files:
        print(f"在目录 {input_dir} 中未找到任何.log文件")
        return

    print(f"找到 {len(log_files)} 个日志文件")

    all_json_data = []

    for log_file in log_files:
        print(f"正在处理文件: {log_file}")

        with open(log_file, 'r', encoding='gbk') as f:
            for line in f:
                # 查找JSON数据的起始和结束位置
                json_start = line.find('{"SensorId"')
                if json_start == -1:
                    continue

                json_end = line.rfind('}') + 1
                if json_end <= json_start:
                    continue

                json_str = line[json_start:json_end]

                try:
                    # 验证JSON是否有效
                    json_obj = json.loads(json_str)
                    all_json_data.append(json_obj)
                except json.JSONDecodeError as e:
                    print(f"无效JSON数据(已跳过): {json_str}")
                    continue

    # 保存提取的JSON数据
    output_file = Path(output_dir) / 'extracted_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_json_data, f, indent=2, ensure_ascii=False)

    print(f"成功提取 {len(all_json_data)} 条JSON数据，已保存到: {output_file}")


if __name__ == "__main__":
    # 配置路径
    input_dir = "data2"  # 日志文件目录
    output_dir = "output"  # 输出目录

    extract_json_from_logs(input_dir, output_dir)