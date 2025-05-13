import json
import sys


def analyze_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # 加载整个 JSON 数据

        # 检查是否是列表/数组
        if not isinstance(data, list):
            print("✅ JSON 格式正确，但不是数组，无法统计条数。")
            return

        total_records = len(data)
        print(f"✅ JSON 格式正确，总共有 {total_records} 条数据。")

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        # 如果是大文件，尝试逐行检查错误位置
        print("\n尝试逐行检查错误位置...")
        with open(file_path, 'r', encoding='utf-8') as f:
            buffer = ""
            line_num = 0
            for line in f:
                line_num += 1
                buffer += line.strip()
                try:
                    json.loads(buffer)
                    buffer = ""
                except json.JSONDecodeError as e:
                    if len(buffer) > 10000:
                        print(f"⚠ 可能在第 {line_num} 行附近发现错误：")
                        print(f"错误行内容（片段）: {line[:200]}...")
                        print(f"完整错误信息: {e}")
                        break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供 JSON 文件路径，例如：python analyze_json.py bundled_uav_data.json")
    else:
        analyze_json(sys.argv[1])