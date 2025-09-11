# modules/module2_combine.py
import pandas as pd
import requests
import os
import logging
from urllib.parse import urlparse
import urllib.request
import html
import opencc
import re

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines=[]
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                lines.append(line)
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

#简繁转换
def traditional_to_simplified(text: str) -> str:
    # 初始化转换器，"t2s" 表示从繁体转为简体
    converter = opencc.OpenCC('t2s')
    simplified_text = converter.convert(text)
    return simplified_text
#M3U格式判断
def is_m3u_content(text):
    lines = text.splitlines()
    first_line = lines[0].strip()
    return first_line.startswith("#EXTM3U")
    
def convert_m3u_to_txt(m3u_content):
    # 分行处理
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http") or line.startswith("rtmp") or line.startswith("p3p") :
            txt_lines.append(f"{channel_name},{line.strip()}")
        
        # 处理后缀名为m3u，但是内容为txt的文件
        if "#genre#" not in line and "," in line and "://" in line:
            # 定义正则表达式，匹配频道名称,URL 的格式，并确保 URL 包含 "://"
            # xxxx,http://xxxxx.xx.xx
            pattern = r'^[^,]+,[^\s]+://[^\s]+$'
            if bool(re.match(pattern, line)):
                txt_lines.append(line)
    
    # 将结果合并成一个字符串，以换行符分隔
    return '\n'.join(txt_lines)
# 添加channel_name前剔除部分特定字符
removal_list = ["「IPV4」","「IPV6」","[ipv6]","[ipv4]","_电信", "电信","（HD）","[超清]","高清","超清", "-HD","(HK)","AKtv","@","IPV6","🎞️","🎦"," ","[BD]","[VGA]","[HD]","[SD]","(1080p)","(720p)","(480p)"]
def clean_channel_name(channel_name, removal_list):
    for item in removal_list:
        channel_name = channel_name.replace(item, "")
        channel_name = channel_name.replace("CCTV-", "CCTV")
        channel_name = channel_name.replace("CCTV0","CCTV")
        channel_name = channel_name.replace("PLUS", "+")
        channel_name = channel_name.replace("NewTV-", "NewTV")
        channel_name = channel_name.replace("iHOT-", "iHOT")
        channel_name = channel_name.replace("NEW", "New")
        channel_name = channel_name.replace("New_", "New")
    return channel_name
# 处理带$的URL，把$之后的内容都去掉（包括$也去掉） 【2024-08-08 22:29:11】
def clean_url(url):
    last_dollar_index = url.rfind('$')  # 安全起见找最后一个$处理
    if last_dollar_index != -1:
        return url[:last_dollar_index]
    return url
    
def process_channel_line(line):
    if  "#genre#" not in line and "#EXTINF:" not in line and "," in line and "://" in line:
        channel_name = line.split(',')[0]
        channel_name = traditional_to_simplified(channel_name)  #繁转简
        channel_name = clean_channel_name(channel_name, removal_list)  #分发前清理channel_name中特定字符
        channel_address = clean_url(line.split(',')[1]).strip()  #把URL中$之后的内容都去掉
        line=channel_name+","+channel_address #重新组织line
    return line

def process_url(url):
    logger.info(f"处理URL: {url}")
    result = []
    try:
        #other_lines.append(url+",#genre#")  # 存入other_lines便于check 2024-08-02 10:41
        
        # 创建一个请求对象并添加自定义header
        headers = {
            'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0',
        }
        req = urllib.request.Request(url, headers=headers)
        # 打开URL并读取内容
        with urllib.request.urlopen(req,timeout=10) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            try:
                # 先尝试 UTF-8 解码
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # 若 UTF-8 解码失败，尝试 GBK 解码
                    text = data.decode('gbk')
                except UnicodeDecodeError:
                    try:
                        # 若 GBK 解码失败，尝试 ISO-8859-1 解码
                        text = data.decode('iso-8859-1')
                    except UnicodeDecodeError:
                        print("无法确定合适的编码格式进行解码。")
                        
            #处理m3u提取channel_name和channel_address
            if is_m3u_content(text):
                text=convert_m3u_to_txt(text)

            # 逐行处理内容
            lines = text.split('\n')
            print(f"行数: {len(lines)}")
            for index, line in enumerate(lines):
                if index % 5000 == 0 and index > 0:  # 每5000行提示一次（跳过第0行）
                    print(f"已处理 {index} 行...")

                line = line.strip()
                if not line:
                    continue
                if  "#genre#" not in line and "," in line and "://" in line and not line.startswith('#'):
                    # 拆分成频道名和URL部分
                    channel_name, channel_address = line.split(',', 1)
                    #需要加处理带#号源=予加速源
                    if "#" not in channel_address:
                        processedline=process_channel_line(line) # 如果没有井号，则照常按照每行规则进行分发
                        name, url = processedline.split(',', 1)
                        result.append([name, url.strip(), ''])
                    else: 
                        # 如果有“#”号，则根据“#”号分隔
                        url_list = channel_address.split('#')
                        for channel_url in url_list:
                            newline=f'{channel_name},{channel_url}'
                            processedline=process_channel_line(newline)
                            name, url = processedline.split(',', 1)
                            result.append([name, url.strip(), ''])
            return result
    except Exception as e:
        print(f"处理URL时发生错误：{e}")
def process_local(url):
    logger.info(f"处理URL: {url}")
    result = []
    try:
        if os.path.exists(url):
            with open(url, 'r', encoding='utf-8') as file:
                text = file.read()
            # 逐行处理内容
            lines = text.split('\n')
            print(f"行数: {len(lines)}")
            for index, line in enumerate(lines):
                if index % 1000 == 0 and index > 0:  # 每1000行提示一次（跳过第0行）
                    print(f"已处理 {index} 行...")

                line = line.strip()
                if not line:
                    continue
                if  "#genre#" not in line and "," in line and "://" in line and not line.startswith('#'):
                    # 拆分成频道名和URL部分
                    channel_name, channel_address = line.split(',', 1)
                    #需要加处理带#号源=予加速源
                    if "#" not in channel_address:
                        processedline=process_channel_line(line) # 如果没有井号，则照常按照每行规则进行分发
                        name, url = processedline.split(',', 1)
                        result.append([name, url.strip(), ''])
                    else: 
                        # 如果有“#”号，则根据“#”号分隔
                        url_list = channel_address.split('#')
                        for channel_url in url_list:
                            newline=f'{channel_name},{channel_url}'
                            processedline=process_channel_line(newline)
                            name, url = processedline.split(',', 1)
                            result.append([name, url.strip(), ''])
            return result
    except Exception as e:
        print(f"处理URL时发生错误：{e}")


def deduplicate(data):
    df = pd.DataFrame(data, columns=['name', 'url', 'extra'])
    df['url'] = df['url'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['url'] = df['url'].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)
    df['name'] = df['name'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['extra'] = df['extra'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['extra'] = df['extra'].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)
    df.drop_duplicates(subset=['name', 'url'], keep='first', inplace=True)
    return df

# def save_df(df, path):
#     logger.info(f"有{len(df)}条数据待写出")
#     df.to_csv(path, index=False, header=False, encoding='utf-8')
#     logger.info(f"数据已写出到 {path}")

def save_df(df, path):
    chunk_size = 50000
    total_rows = len(df)
    logger.info(f"有 {total_rows} 条数据待写出")

    # 如果文件已存在，先删除（确保从头开始写）
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"已删除旧文件 {path}")

    # 分块写入
    num_chunks = (total_rows + chunk_size - 1) // chunk_size  # 向上取整
    for i in range(num_chunks):
        start_row = i * chunk_size
        end_row = min(start_row + chunk_size, total_rows)
        chunk = df.iloc[start_row:end_row]

        # 第一块写入时，不写 header（因为 header=False）；后续块追加写入
        write_header = False  # 你原需求是 header=False，所以始终不写 header
        write_mode = 'w' if i == 0 else 'a'  # 第一块覆盖写，后续块追加写

        chunk.to_csv(
            path,
            index=False,
            header=write_header,
            encoding='utf-8',
            mode=write_mode
        )

        logger.info(f"数据分段 {i+1}/{num_chunks} 已追加写入到 {path}")

    logger.info(f"全部数据已写出到 {path}")

def combine_sources():
    logger.info("开始执行模块2：读取订阅源")
    urls=read_txt_to_array(os.path.join("config", "subscribe.txt"))
    net_data=[]
    for url in urls:
        if url.startswith("http"):        
            net_data+=process_url(url)
    net_df = deduplicate(net_data)

    # 读取本地源
    result_data = process_local(os.path.join("config", "user_result.txt"))
    local_data = process_local(os.path.join("config", "localsource.txt"))
    own_data = process_local(os.path.join("output", "ownsource.txt"))
    errorflag=False

    
    try:
        save_df(net_df, os.path.join("output", "netsource.txt"))
    except Exception as e: 
        logger.error(f"网络源写出失败:{e}")
        errorflag=True
        with open(os.path.join("output", "netsource_log.csv"), 'w', encoding='gbk', errors='replace') as f:
            for _, row in net_df.iterrows():
                f.write(f"{row['name']},{row['url']},{row['extra']}\n")
        
    
    # 合并所有源
    if errorflag:
        all_data = result_data + local_data + own_data
    else:
        all_data = result_data + local_data + own_data + net_data
        
    all_df = deduplicate(all_data)
    all_df.drop(columns=['extra'], inplace=True)
    try:
        save_df(all_df, os.path.join("output", "allsource.txt"))
    except Exception as e: 
        logger.error(f"网络源写出失败:{e}")
        with open(os.path.join("output", "allsource_log.txt"), 'w', encoding='gbk', errors='replace') as f:
            for _, row in all_df.iterrows():
                f.write(f"{row['name']},{row['url']}\n")
    logger.info("模块2执行完毕")
    return errorflag
if __name__ == '__main__':

    combine_sources()


# import pandas as pd
# import requests
# import os
# import logging
# from urllib.parse import urlparse

# # --- 配置日志 ---
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def read_sources(file_path):
#     data = []
#     if not os.path.exists(file_path):
#         return data
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             line = line.strip()
#             if not line or line.startswith('#') or ',#genre#' in line:
#                 continue
#             parts = line.split(',', 1)
#             name = parts[0].strip()
#             url = parts[1].strip() if len(parts) > 1 else ''
#             extra = ''
#             if '$' in url:
#                 url, extra = url.split('$', 1)
#             data.append([name, url.strip(), extra.strip()])
#     return data

# def read_subscribe_sources(subscribe_path):
#     data = []
#     with open(subscribe_path, 'r', encoding='utf-8') as f:
        
#         for line in f:
#             line = line.strip()
#             if not line or line.startswith('#'):
#                 continue
#             try:
#                 response = requests.get(line, timeout=10)
#                 if 'm3u' in urlparse(line).path.lower():
#                     logger.info(f"检测到M3U源{line}，即将处理")
#                     # M3U 格式解析
#                     lines = response.text.splitlines()
#                     i = 0
#                     while i < len(lines):
#                         if lines[i].startswith('#EXTINF'):
#                             info = lines[i]
#                             url = lines[i+1]
#                             name = info.split(',')[-1].strip()
#                             data.append([name, url.strip(), ''])
#                             i += 2
#                         else:
#                             i += 1
#                 else:
#                     # TXT 格式解析
#                     for line in response.text.splitlines():
#                         line = line.strip()
#                         if not line or line.startswith('#') or ',#genre#' in line:
#                             continue
#                         if '\t' in line:
#                             parts = line.split('\t')
#                             for part in parts:
#                                 p = part.strip()
#                                 if ',' in p:
#                                     name, url = p.split(',', 1)
#                                     extra = ''
#                                     if '$' in url:
#                                         url, extra = url.split('$', 1)
#                                     data.append([name.strip(), url.strip(), extra.strip()])
#                         else:
#                             if ',' in line:
#                                 name, url = line.split(',', 1)
#                                 extra = ''
#                                 if '$' in url:
#                                     url, extra = url.split('$', 1)
#                                 data.append([name.strip(), url.strip(), extra.strip()])
#             except Exception as e:
#                 logger.error(f"订阅源读取失败: {line} - {e}")
#         logger.info(f"订阅源已处理完毕")
#     return data

# def deduplicate(data):
#     df = pd.DataFrame(data, columns=['name', 'url', 'extra'])
#     #df['url'] = df['url'].str.replace('\r', '', regex=False).str.replace('\n', '', regex=False).str.replace(',', '', regex=False).str.replace('"', '', regex=False).str.replace("'", '', regex=False)
#     #df['name'] = df['name'].str.replace('\r', '', regex=False).str.replace('\n', '', regex=False).str.replace(',', '', regex=False).str.replace('"', '', regex=False).str.replace("'", '', regex=False)
#     #df['extra'] = df['extra'].str.replace('\r', '', regex=False).str.replace('\n', '', regex=False).str.replace(',', '', regex=False).str.replace('"', '', regex=False).str.replace("'", '', regex=False)
#     df.drop_duplicates(subset=['name', 'url'], keep='first', inplace=True)
#     return df

# def save_df(df, path):
#     df.to_csv(path, index=False, header=False, encoding='utf-8')
    
# def combine_sources():
#     logger.info("开始执行模块2：读取订阅源")
#     # 读取本地源
#     #result_data = read_sources(r'.\config\user_result.txt')
#     result_data = read_sources(os.path.join("config", "user_result.txt"))
#     #local_data = read_sources(r'.\config\localsource.txt')
#     local_data = read_sources(os.path.join("config", "localsource.txt"))
#     #own_data = read_sources(r'.\output\ownsource.txt')
#     own_data = read_sources(os.path.join("output", "ownsource.txt"))
    
#     # 读取在线源
#     #net_data = read_subscribe_sources(r'.\config\subscribe.txt')
#     net_data = read_subscribe_sources(os.path.join("config", "subscribe.txt"))
#     net_df = deduplicate(net_data)
#     #save_df(net_df, r'.\output\netsource.txt')
#     text = '\n'.join(net_df.apply(lambda row: f"{row['name']}|{row['url']}|{row['extra']}", axis=1))
#     with open(os.path.join("output", "netsource_log.txt"), 'w', encoding='utf-8') as f:
#         f.write(text)
#     save_df(net_df, os.path.join("output", "netsource.txt"))

    
#     # 合并所有源
#     all_data = result_data + local_data + own_data + net_data
#     all_df = deduplicate(all_data)
#     # all_df['combined'] = all_df.apply(
#     # lambda row: f"{row['name']},{row['url']}${row['extra']}",
#     # axis=1
#     # )
#     all_df.drop(columns=['extra'], inplace=True)
#     #save_df(all_df, r'.\output\allsource.txt')
#     save_df(all_df, os.path.join("output", "allsource.txt"))
#     logger.info("模块2执行完毕")
# if __name__ == '__main__':

#     combine_sources()

































