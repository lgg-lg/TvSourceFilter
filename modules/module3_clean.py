# modules/module4_clean.py

import os
import logging

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_blacklist(blacklist_path):
    """从文件加载黑名单"""
    blacklist = set()
    if not os.path.exists(blacklist_path):
        logger.warning(f"黑名单文件 {blacklist_path} 未找到，将不执行任何过滤。")
        return blacklist

    try:
        with open(blacklist_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if line and not line.startswith('#'):
                    # 存入小写形式，方便不区分大小写的匹配
                    blacklist.add(line.lower())
        logger.info(f"已从 {blacklist_path} 加载 {len(blacklist)} 个黑名单关键词。")
    except Exception as e:
        logger.error(f"读取黑名单文件 {blacklist_path} 时出错: {e}")
    return blacklist

def is_line_clean(line, blacklist):
    """检查一行是否不包含黑名单词汇"""
    if not blacklist:
        return True # 如果黑名单为空，则所有行都“干净”

    line_lower = line.lower()
    for keyword in blacklist:
        if keyword in line_lower:
            return False # 找到一个黑名单词，此行不干净
    return True # 遍历完所有黑名单词都没找到，此行干净

def clean_sources(input_path, blacklist_path, output_path):
    """主清理函数"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. 加载黑名单
    blacklist = load_blacklist(blacklist_path)

    # 2. 读取源文件并过滤
    cleaned_lines = []
    total_lines = 0
    cleaned_lines_count = 0

    if not os.path.exists(input_path):
        logger.error(f"输入文件 {input_path} 未找到，无法进行清理。")
        # 创建一个空的输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            pass
        return

    try:

        with open(input_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                total_lines += 1
                # 去除行尾换行符进行处理
                line_content = line.rstrip('\n\r')
                # 检查行是否为空或注释（虽然 allsource.txt 通常不会有）
                if not line_content or line_content.startswith('#'):
                     # 如果源文件有注释或空行，也保留
                     cleaned_lines.append(line) # 保留原始换行符
                     cleaned_lines_count += 1
                     continue

                # 3. 应用黑名单过滤
                if is_line_clean(line_content, blacklist):
                    cleaned_lines.append(line) # 保留原始换行符
                    cleaned_lines_count += 1
                # else: 行被过滤掉，不添加到 cleaned_lines

        # 4. 写入清理后的文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_lines)

        logger.info(f"清理完成: 总共处理 {total_lines} 行，保留 {cleaned_lines_count} 行，过滤掉 {total_lines - cleaned_lines_count} 行。")
        logger.info(f"清理后的文件已保存至 {output_path}")

    except Exception as e:
        logger.error(f"处理文件 {input_path} 时出错: {e}")

def main():
    """模块3的入口函数"""

    input_file = os.path.join("output", "allsource.txt")
    blacklist_file = os.path.join("config", "blacklist.txt")
    output_file = os.path.join("output", "allsourcecleaned.txt")

    logger.info("开始执行模块3：清理信号源")
    clean_sources(input_file, blacklist_file, output_file,flag)
    logger.info("模块3执行完毕。")

# 如果直接运行此脚本，则执行 main 函数
if __name__ == "__main__":

    main()


