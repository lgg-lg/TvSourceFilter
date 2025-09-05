# modules/module6_result.py

import os
import shutil
import logging

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def replace_user_channels(user_demo_path, channels_dir, output_path):
    """
    根据 user_demo.txt 中的频道名，替换为 channels 目录下对应文件的内容。
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(user_demo_path):
        logger.error(f"用户模板文件 {user_demo_path} 未找到。")
        return

    # 1. 读取 user_demo.txt 的所有行
    try:
        with open(user_demo_path, 'r', encoding='utf-8') as f:
            user_lines = f.readlines()
    except Exception as e:
        logger.error(f"读取用户模板文件 {user_demo_path} 时出错: {e}")
        return

    logger.info(f"读取到 {len(user_lines)} 行用户模板内容。")

    # 2. 处理每一行
    final_lines = []
    replacements_made = 0
    for i, line in enumerate(user_lines):
        original_line = line
        line = line.rstrip('\n\r') # 去掉行尾换行符，方便处理

        # 跳过注释行和分类行
        if line.startswith('#') or ',#genre#' in line:
            final_lines.append(original_line) # 保留原始行（包括换行符）
            continue

        # 假设有效行是频道名，或者频道名在第一个逗号前
        # 例如 "CCTV1" 或 "CCTV1,其他信息"
        parts = line.split(',', 1)
        channel_name = parts[0].strip()

        if not channel_name:
             # 如果频道名为空，也保留原行
             final_lines.append(original_line)
             continue

        # 3. 查找对应的频道文件
        channel_file_path = os.path.join(channels_dir, f"{channel_name}_picked.txt")
        
        if os.path.exists(channel_file_path):
            try:
                # 读取频道文件的全部内容
                with open(channel_file_path, 'r', encoding='utf-8') as cf:
                    channel_content = cf.read()
                # 将频道文件的内容（通常包含换行符）添加到最终列表
                # channel_content 末尾通常已有换行符，如果没有，可能需要添加
                final_lines.append(channel_content)
                replacements_made += 1
                logger.debug(f"第 {i+1} 行 '{line}' 已替换为 '{channel_name}.txt' 的内容。")
            except Exception as e:
                logger.error(f"读取频道文件 {channel_file_path} 时出错: {e}")
                # 如果读取出错，保留原行
                final_lines.append(original_line)
        else:
            # 如果找不到对应的频道文件，保留原行
            logger.debug(f"未找到频道文件 '{channel_name}.txt'，保留原行: {line}")
            final_lines.append(original_line)

    # 4. 写入最终结果
    try:
        # 写入到新的输出文件，保留原文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        logger.info(f"用户频道列表替换完成。共进行了 {replacements_made} 次替换。")
        logger.info(f"最终结果已保存至 {output_path}")
        
        # --- 可选：如果你想直接覆写原文件 ---
        # backup_path = user_demo_path + ".bak"
        # shutil.copy2(user_demo_path, backup_path) # 创建备份
        # logger.info(f"原文件已备份至 {backup_path}")
        # with open(user_demo_path, 'w', encoding='utf-8') as f:
        #     f.writelines(final_lines)
        # logger.info(f"最终结果已直接覆写至 {user_demo_path}")

    except Exception as e:
        logger.error(f"写入最终文件 {output_path} 时出错: {e}")

def main():
    """模块6的入口函数"""
    user_demo_file = os.path.join("config", "user_demo.txt")
    channels_directory = os.path.join("output", "channels")
    # 输出到新文件，避免覆盖原模板
    output_file = os.path.join("output", "new_result.txt") 

    logger.info("开始执行模块6：替换用户频道列表")
    replace_user_channels(user_demo_file, channels_directory, output_file)
    logger.info("模块6执行完毕。")

# 如果直接运行此脚本，则执行 main 函数
if __name__ == "__main__":
    main()