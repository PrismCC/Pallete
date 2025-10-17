import json

# 定义排序顺序
TAG_ORDER = ['红', '橘', '黄', '绿', '青', '蓝', '紫', '棕', '粉', '白', '灰', '黑']

def sort_tags(tags):
    """按照指定顺序对tags进行排序"""
    return sorted(tags, key=lambda x: TAG_ORDER.index(x) if x in TAG_ORDER else len(TAG_ORDER))

def process_json_file(input_file, output_file):
    """处理JSON文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 对每个颜色项的tags进行排序
    for color_name, color_data in data.items():
        if 'tags' in color_data:
            color_data['tags'] = sort_tags(color_data['tags'])
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 使用示例
input_file = 'colors.json'  # 输入JSON文件路径
output_file = 'colors_sorted.json'  # 输出JSON文件路径
process_json_file(input_file, output_file)
