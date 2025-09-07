import json
import os

def merge_datasets(base_path):
    """合并多层级数据集"""
    # 定义目标文件路径
    output_path = os.path.join(base_path, "dataset_train.json")
    
    # 配置需要合并的文件结构
    dataset_map = {
        "first": "dataset_first.json",
        "second": "dataset_second.json",
        "third": "dataset_third.json",
        "fourth": "dataset_fourth.json"
    }

    merged_data = []
    
    # 遍历所有目标文件夹
    for folder, filename in dataset_map.items():
        file_path = os.path.join(base_path, folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"🔍 正在加载：{folder}/{filename}")
                data = json.load(f)
                
                # 数据格式验证
                if not isinstance(data, list):
                    raise ValueError(f"文件格式错误：{file_path} 不是JSON数组")
                
                merged_data.extend(data)
                print(f"✅ 成功加载 {len(data)} 条记录")
                
        except Exception as e:
            print(f"⚠️ 加载失败：{folder}/{filename} - {str(e)}")
            continue

    # 写入合并文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 合并完成！总样本量：{len(merged_data)}")
    print(f"输出文件：{output_path}")

# 使用示例
base_dir = r"C:\Users\朱权海\Desktop\llm\dataset"
merge_datasets(base_dir)
