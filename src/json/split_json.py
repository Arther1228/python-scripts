import json
import os


def split_json(input_file, output_dir, num_parts=10):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取整个 JSON 文件（适用于可以加载到内存的情况）
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 假设 data 是一个列表

    if not isinstance(data, list):
        print("❌ JSON 不是数组格式，无法分割！")
        return

    total_records = len(data)
    records_per_file = total_records // num_parts

    print(f"📊 总数据条数: {total_records}")
    print(f"✂️ 分割成 {num_parts} 个子文件，每个约 {records_per_file} 条数据...")

    for i in range(num_parts):
        start = i * records_per_file
        end = (i + 1) * records_per_file if i < num_parts - 1 else total_records

        chunk = data[start:end]
        output_file = os.path.join(output_dir, f"part_{i + 1}.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)

        print(f"✅ 已生成: {output_file} (数据: {start + 1}-{end})")


if __name__ == "__main__":
    input_file = "bundled_uav_data.json"  # 你的 JSON 文件路径
    output_dir = "split_output"  # 输出目录

    split_json(input_file, output_dir, num_parts=10)