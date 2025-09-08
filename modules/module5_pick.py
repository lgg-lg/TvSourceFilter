# modules/module5_pick.py

import os
import logging

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_whitelist(whitelist_path):
    """从文件加载白名单"""
    whitelist = set()
    if not os.path.exists(whitelist_path):
        logger.warning(f"白名单文件 {whitelist_path} 未找到，将不执行任何优选。")
        return whitelist

    try:
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if line and not line.startswith('#'):
                    # 存入小写形式，方便不区分大小写的匹配
                    whitelist.add(line.lower())
        logger.info(f"已从 {whitelist_path} 加载 {len(whitelist)} 个白名单关键词。")
    except Exception as e:
        logger.error(f"读取白名单文件 {whitelist_path} 时出错: {e}")
    return whitelist

def is_line_wanted(line, whitelist):
    """检查一行是否包含白名单词汇"""
    if not whitelist:
        logger.debug("白名单为空，所有行都将被丢弃。")
        return False # 如果白名单为空，则没有行是“想要的”

    line_lower = line.lower()
    for keyword in whitelist:
        if keyword in line_lower:
            return True # 找到一个白名单词，此行是我们想要的
    return False # 遍历完所有白名单词都没找到，此行不想要

def pick_sources_for_channel(channel_name, whitelist, channels_dir):
    """对单个频道进行优选"""
    input_file = os.path.join(channels_dir, f"{channel_name}.txt")
    output_file = os.path.join(channels_dir, f"{channel_name}_picked.txt")

    if not os.path.exists(input_file):
        logger.info(f"频道文件 {input_file} 不存在，跳过。")
        return

    picked_lines = []
    total_lines = 0
    picked_lines_count = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                total_lines += 1
                # 去除行尾换行符进行处理
                line_content = line.rstrip('\n\r')
                # 检查行是否为空
                if not line_content:
                     continue

                # 应用白名单筛选
                if is_line_wanted(line_content, whitelist):
                    picked_lines.append(line) # 保留原始换行符
                    picked_lines_count += 1

        # 写入选优后的文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(picked_lines)

        logger.info(f"频道 '{channel_name}' 优选完成: 处理 {total_lines} 行，保留 {picked_lines_count} 行。")

    except Exception as e:
        logger.error(f"处理频道 '{channel_name}' 时出错: {e}")

def load_channels_list(channels_path):
    """从 channels.txt 加载频道列表"""
    channels = []
    if not os.path.exists(channels_path):
        logger.error(f"频道列表文件 {channels_path} 未找到。")
        return channels

    try:
        with open(channels_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if line and (not line.startswith('#') and (not (',#genre#' in line)) :
                    channels.append(line)
        logger.info(f"已从 {channels_path} 加载 {len(channels)} 个频道。")
    except Exception as e:
        logger.error(f"读取频道列表文件 {channels_path} 时出错: {e}")
    return channels

def main():
    """模块5的入口函数"""
    whitelist_file = os.path.join("config", "whitelist.txt")
    #channels_list_file = os.path.join("config", "channels.txt")
    channels_list_file = os.path.join("config", "user_demo.txt")
    channels_output_dir = os.path.join("output", "channels")

    logger.info("开始执行模块5：优选频道信号源")

    # 1. 加载白名单
    whitelist = load_whitelist(whitelist_file)
    if not whitelist:
        logger.warning("白名单为空，所有频道的信号源将被丢弃。")
    # 2. 加载频道列表
    channel_names = load_channels_list(channels_list_file)

    if not channel_names:
        logger.warning("没有有效的频道需要处理。")
        return

    # 3. 对每个频道执行优选
    for channel in channel_names:
        pick_sources_for_channel(channel, whitelist, channels_output_dir)

    logger.info("模块5执行完毕。")

# 如果直接运行此脚本，则执行 main 函数
if __name__ == "__main__":

    main()

