# modules/module3_split.py

# import os
# import pandas as pd

# def split_channels():
#     # 读取频道字典
#     channel_dict = {}
#     with open(r'.\config\othernames.txt', 'r', encoding='utf-8') as f:
#         for line in f:
#             if line.startswith('[') and ':' in line:
#                 channel, names = line.strip().split(':', 1)
#                 channel = channel.strip('[]')
#                 names = [n.strip() for n in names.split(',')]
#                 channel_dict[channel] = names

#     # 创建输出目录
#     os.makedirs(r'.\output\channels', exist_ok=True)

#     # 读取 allsource.txt
#     df = pd.read_csv(r'.\output\allsource.txt', header=None, names=['name', 'url', 'extra'])

#     # 拆分频道
#     for channel, names in channel_dict.items():
#         mask = df['name'].isin(names)
#         sub_df = df[mask]
#         sub_df['name'] = channel
#         sub_df.to_csv(f'.\\output\\channels\\{channel}.txt', index=False, header=False, encoding='utf-8')

# if __name__ == '__main__':
#     split_channels()

# modules/module3_split.py

import os
import pandas as pd

def split_channels():
    # 读取频道字典
    channel_dict = {}
    # --- 假设 othernames.txt 在 config 目录下 ---
    # othernames_path = 'config/othernames.txt' 
    othernames_path = os.path.join("config", "othernames.txt")
    if os.path.exists(othernames_path):
        with open(othernames_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('[') and ':' in line:
                    # 安全地分割，处理可能没有 ':' 的情况
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        channel_part, names_part = parts
                        # 去除 '[' 和 ']' 并 strip
                        channel = channel_part.strip('[]').strip()
                        # 分割名称并去除每个名称的空格
                        names = [n.strip() for n in names_part.split(',') if n.strip()]
                        if channel: # 确保 channel 名称非空
                            channel_dict[channel] = names
    else:
        print(f"警告: 文件 {othernames_path} 未找到。跳过频道拆分。")
        return # 如果文件不存在，直接返回

    # 检查 allsource.txt 是否存在
    #allsource_path = 'output/allsourcecleaned.txt'
    allsource_path = os.path.join("output", "allsourcecleaned.txt")
    if not os.path.exists(allsource_path):
        print(f"警告: 文件 {allsource_path} 未找到。无法进行频道拆分。")
        return

    # 读取 allsource.txt
    try:
        df = pd.read_csv(allsource_path, header=None, names=['name', 'url', 'extra'])
    except pd.errors.EmptyDataError:
        print(f"警告: 文件 {allsource_path} 为空。")
        return
    except Exception as e:
        print(f"错误: 读取文件 {allsource_path} 失败: {e}")
        return

    # 创建输出目录
    #os.makedirs('output/channels', exist_ok=True)
    os.makedirs(os.path.join("output", "channels"), exist_ok=True)
    # --- 核心修改部分：使用 .loc 避免 SettingWithCopyWarning ---
    # 创建一个空的列表来存储所有需要保存的子 DataFrame
    results_to_save = []

    # 遍历频道字典
    for channel, names in channel_dict.items():
        if not names: # 如果 names 列表为空，跳过
            continue
            
        # 创建布尔掩码
        mask = df['name'].isin(names)
        
        # 使用 .loc 和 .copy() 明确创建一个副本
        # 这样可以确保后续操作不会影响原始 df，并且消除警告
        sub_df = df.loc[mask].copy() 
        
        if not sub_df.empty:
            # 在副本上安全地修改 'name' 列
            sub_df.loc[:, 'name'] = channel
            
            # 将处理好的 DataFrame 添加到列表中
            results_to_save.append((channel, sub_df))
        else:
            print(f"信息: 频道 '{channel}' 在 allsource.txt 中未找到对应条目。")

    # 循环结束后，统一保存所有结果
    for channel, sub_df_to_save in results_to_save:
        #output_file_path = f'output/channels/{channel}.txt'
        output_file_path = os.path.join("output", f"channels\\{channel}")
        try:
            # 保存到文件，不包含索引和列头
            sub_df_to_save.drop(columns=['extra'], inplace=True)  # 如果不需要 extra 列，可以删除
            sub_df_to_save.drop_duplicates(subset=['url'], inplace=True)  # 可选：去重
            sub_df_to_save.to_csv(output_file_path, index=False, header=False, encoding='utf-8')
            print(f"信息: 已保存频道 '{channel}' 的条目到 {output_file_path}")
        except Exception as e:
            print(f"错误: 保存文件 {output_file_path} 失败: {e}")

    print("频道拆分完成。")

if __name__ == '__main__':

    split_channels()
