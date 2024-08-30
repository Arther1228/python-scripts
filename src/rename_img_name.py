import os
import exifread
import shutil

pic_dir = 'C:/Users/chuang/Desktop/1/'
output_dir = 'C:/Users/chuang/Desktop/output/'
log_file = 'C:/Users/chuang/Desktop/statistics.txt'


# 参考 https://www.cnblogs.com/arnoldlu/p/17219384.html

def is_named_correctly(filename):
    name, ext = os.path.splitext(filename)
    # 检查文件名是否符合 yyyy-mm-dd-HHmmss 格式
    if len(name) == 15 and name[:10].count('-') == 2 and name[11:].isdigit():
        return True
    return False


if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    processed_count = 0
    failed_count = 0

    pic_file_lists = os.listdir(pic_dir)
    for pic_file in pic_file_lists:
        if is_named_correctly(pic_file):
            continue

        with open(os.path.join(pic_dir, pic_file), 'rb') as file_data:
            tags = exifread.process_file(file_data)
            file_date = str(tags.get('EXIF DateTimeDigitized', ''))
            if file_date == '':
                failed_count += 1
                continue

            # 提取日期和时间
            date_part = file_date.split(' ')[0].replace(':', '-')
            time_part = file_date.split(' ')[1].replace(':', '')
            new_filename = f"{date_part}-{time_part}{os.path.splitext(pic_file)[1]}"

            shutil.copy(os.path.join(pic_dir, pic_file), os.path.join(output_dir, new_filename))
            processed_count += 1

    with open(log_file, 'w') as log:
        log.write(f"Processed files: {processed_count}\n")
        log.write(f"Failed files (missing EXIF DateTimeDigitized): {failed_count}\n")

    print(f"Processed files: {processed_count}")
    print(f"Failed files: {failed_count}")