import json
import re
import os

def read_va_content(file_path):
    """读取VerilogA文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️ 警告：未找到参考文件 {file_path}")
        return ""
    except Exception as e:
        print(f"⚠️ 文件读取错误：{str(e)}")
        return ""

def process_folder(folder_path):
    """处理单个文件夹"""
    # 生成系统提示
    va_path = os.path.join(folder_path, "correct.va")
    code_content = read_va_content(va_path)
    system_prompt = {
        "role": "system",
        "content": f"You are a Verilog-A hardware modeling expert. Below is a reference code snippet:\n```\n{code_content}\n```\n Please correct the code based on the input error code, paying attention to functional and syntactic accuracy."
    }

    # 处理数据文件
    merged_data = []
    file_names = ['responseFUNCTION.txt', 'responseSYNTAX.txt']
    
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 引号处理
                content = content.replace('"', "'")
                for keyword in ['original_line', 'bug_line', 'error_description']:
                    content = re.sub(r"'(%s)':" % keyword, r'"\1":', content)
                
                # 数据提取
                pattern = re.compile(
                    r'{\s*'
                    r'"original_line":\s*(?P<original>\'.*?\'),\s*'
                    r'"bug_line":\s*(?P<bug>\'.*?\'),\s*'
                    r'"error_description":\s*(?P<desc>\'.*?\')'
                    r'\s*}', 
                    re.DOTALL
                )
                
                for match in pattern.finditer(content):
                    original = match.group("original").strip("'")
                    bug = match.group("bug").strip("'")
                    desc = match.group("desc").strip("'")
                    
                    merged_data.append({
                        "messages": [
                            system_prompt,
                            {
                                "role": "user",
                                "content": f"Please correct the problematic Verilog-A code below:\n{bug} Please provide the corrected code and the Correction Criteria."
                            },
                            {
                                "role": "assistant",
                                "content": f"corrected code：\n{original}\n\n Correction Criteria：{desc}"
                            }
                        ]
                    })
    
    # 保存单个文件夹数据集
    output_path = os.path.join(folder_path, "training_dataset.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    return merged_data

def batch_process(base_path):
    """批量处理所有文件夹"""
    all_data = []
    
    # 遍历1-40号文件夹
    for folder_num in range(1, 42):
        folder_path = os.path.join(base_path, str(folder_num))
        
        if not os.path.exists(folder_path):
            print(f"⏩ 跳过不存在文件夹：{folder_path}")
            continue
        
        print(f"\n🔨 正在处理文件夹：{folder_path}")
        folder_data = process_folder(folder_path)
        all_data.extend(folder_data)
        print(f"✅ 已完成处理，本文件夹样本数：{len(folder_data)}")
    
    # 保存合并数据集
    combined_path = os.path.join(base_path, "dataset_fifth.json")
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 全部处理完成！总样本数：{len(all_data)}")
    print(f"合并文件路径：{combined_path}")

# 执行批量处理
base_directory = r"C:\Users\朱权海\Desktop\llm\dataset\fifth"
batch_process(base_directory)
