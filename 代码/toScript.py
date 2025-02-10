# toScript.py
import json
import sys

if len(sys.argv) != 4:
    print("Usage: python toScript.py <input_file> <injson_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]     # 原始文本文件
json_file = sys.argv[2]      # JSON翻译文件
output_file = sys.argv[3]    # 输出文件

def count_leading_spaces(text_line):
    """计算行首空格数"""
    space_count = 0
    for char in text_line:
        if char == " ":
            space_count += 1
        else:
             break
    return space_count
            
# 读取JSON数据
with open(json_file, "r", encoding="utf-8") as f:
    translations = json.load(f)
    line_mapping = {}  # 行号到翻译的映射
    for translation in translations:
        line_mapping[translation["line"]] = translation
    
# 处理文本文件
with open(input_file, "r", encoding="utf-8") as input_f:
    with open(output_file, "w", encoding="utf-8") as output_f:
        for line_num, line in enumerate(input_f):
            speaker_name = None
            if line_num in line_mapping:
                # 获取该行的翻译
                current_translation = line_mapping[line_num]
                output_text = current_translation["message"]
                
                speaker_name = current_translation["name"]
                
                if speaker_name == "old":
                    speaker_name = "new"
                
                if speaker_name is not None:
                    output_text = speaker_name + ' "' + output_text + '"'
                else:
                    output_text = '"' + output_text + '"'
                    
                # 保持原有缩进
                space_count = count_leading_spaces(line)
                spaces = ' ' * space_count
                output_f.write(spaces + output_text + "\n")
            else:
                output_f.write(line)
