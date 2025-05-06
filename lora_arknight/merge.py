import os
import chardet  # 需要安装: pip install chardet


def detect_encoding(file_path):
    """检测文件的编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def merge_txt_files(input_folder, output_file):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 打开输出文件以写入模式
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)

                encoding = detect_encoding(file_path)

                try:
                    with open(file_path, 'r', encoding=encoding, errors='replace') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n")
                except Exception as e:
                    print(f"无法读取文件 {file_path}: {e}")


# 指定输入文件夹和输出文件
input_folder = r'D:\me\arknight\主线\14.慈悲灯塔'  # 替换为你的TXT文件所在文件夹
output_file = './out/merged.txt'  # 替换为你希望输出的合并文件路径

# 合并文件
merge_txt_files(input_folder, output_file)