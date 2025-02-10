# parsejson.py
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python parsejson.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]  # 输入文件路径
output_file = sys.argv[2] # 输出JSON文件路径

parsed_entries = []  # 存储解析后的条目
with open(input_file, "r", encoding="utf-8") as lines:
    for line_index, line in enumerate(lines):
        # 跳过特殊行
        if line.startswith("#") or line.startswith("translate") or line.startswith("game"):
            continue
        line = line.strip()
        if not line.startswith("#") and not line.startswith("old"):
            continue
         
        line = line.strip("# ")
        if line.startswith("game"):
            continue
        
        # 解析文本行
        if not line.startswith('"'):
            # 处理 name "text" 格式
            space_pos = line.index(" ")
            speaker_name = line[:space_pos]
            message_text = line[space_pos + 1:].strip('"')
        else:
            # 处理 "name" "text" 格式
            parts = line.split('"')
            if len(parts) == 3:
                message_text = parts[1]
                speaker_name = None
            elif len(parts) == 5:
                speaker_name = '"' + parts[1] + '"'
                message_text = parts[3]
                
        entry = {
            "name": speaker_name,
            "message": message_text,
            "originMessage": message_text,
            "line": line_index + 1
        }
        
        parsed_entries.append(entry)
        speaker_name = None
        
# 写入JSON文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(parsed_entries, f, indent=4, ensure_ascii=False)
