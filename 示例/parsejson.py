# parsejson.py
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python parsejson.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]  # 输入文件路径
output_file = sys.argv[2] # 输出JSON文件路径

def find_next_quote(start_pos, text_line):
    """查找下一个未被转义的引号位置"""
    quote_pos = text_line.find('"', start_pos)
    if text_line[quote_pos - 1] == '\\':
        return find_next_quote(quote_pos + 1, text_line)
    return quote_pos

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
            message_text = line[space_pos + 1:]
        else:
            # 处理 "name" "text" 格式
            text_blocks = []
            current_pos = 0
            prev_pos = -1
            while current_pos != -1:
                current_pos = line.find('"', current_pos) + 1
                if prev_pos > current_pos:
                    break
                prev_pos = current_pos
                quote_end = find_next_quote(current_pos, line)
                text_blocks.append(line[current_pos:quote_end])
                current_pos = quote_end + 1
            
            if len(text_blocks) == 1:
                message_text = text_blocks[0]
                speaker_name = None
            elif len(text_blocks) == 2:
                speaker_name = '"' + text_blocks[0] + '"'
                message_text = text_blocks[1]
                
        # 处理转义字符
        message_text = message_text.strip('"').replace('\\"','"').replace("\n","\\n").replace("\\\\","\\")
        
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
