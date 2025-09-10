# modules/module2_combine.py
import pandas as pd
import requests
import os
import logging
from urllib.parse import urlparse
import html

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_sources(file_path):
    data = []
    if not os.path.exists(file_path):
        return data
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or ',#genre#' in line:
                continue
            parts = line.split(',', 1)
            name = parts[0].strip()
            url = parts[1].strip() if len(parts) > 1 else ''
            extra = ''
            if '$' in url:
                url, extra = url.split('$', 1)
            data.append([name, url.strip(), extra.strip()])
    return data

def read_subscribe_sources(subscribe_path):
    data = []
    with open(subscribe_path, 'r', encoding='utf-8') as f:
        
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                response = requests.get(line, timeout=10)
                if 'm3u' in urlparse(line).path.lower():
                    logger.info(f"检测到M3U源{line}，即将处理")
                    # M3U 格式解析
                    lines = response.text.splitlines()
                    i = 0
                    while i < len(lines):
                        if lines[i].startswith('#EXTINF'):                           
                            info = lines[i]
                            url = html.unescape(lines[i+1])
                            name = info.split(',')[-1].strip()
                            url, extra = url.split('$', 1)
                            extra=extra.split('#')[0].strip()
                            data.append([name, url.strip(), extra])
                            i += 2
                        else:
                            i += 1
                else:
                    # TXT 格式解析
                    logger.info(f"检测到TXT源{line}，即将处理")
                    for line in response.text.splitlines():
                        line = line.strip()
                        if not line or line.startswith('#') or ',#genre#' in line:
                            continue
                        if '\t' in line:
                            parts = line.split('\t')
                            for part in parts:
                                p = part.strip()
                                if ',' in p:
                                    name, url = p.split(',', 1)
                                    extra = ''
                                    url=html.unescape(url)
                                    if '$' in url:
                                        url, extra = url.split('$', 1)
                                    data.append([name.strip(), url.strip(), extra.strip()])
                        else:
                            if ',' in line:
                                name, url = line.split(',', 1)
                                extra = ''
                                if '$' in url:
                                    url, extra = url.split('$', 1)
                                    extra=extra.split('#')[0].strip()
                                data.append([name.strip(), url.strip(), extra.strip()])
            except Exception as e:
                logger.error(f"订阅源读取失败: {line} - {e}")
        logger.info(f"订阅源已处理完毕")
    return data

def deduplicate(data):
    df = pd.DataFrame(data, columns=['name', 'url', 'extra'])
    df['url'] = df['url'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['url'] = df['url'].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)
    df['name'] = df['name'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['extra'] = df['extra'].str.replace(r'[\r\n,;"\'\t]', '', regex=True)
    df['extra'] = df['extra'].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)
    df.drop_duplicates(subset=['name', 'url'], keep='first', inplace=True)
    return df

def save_df(df, path):
    logger.error(f"有{len(df)}条数据待写出")
    df.to_csv(path, index=False, header=False, encoding='utf-8')
    
def combine_sources():
    logger.info("开始执行模块2：读取订阅源")
    # 读取本地源
    #result_data = read_sources(r'.\config\user_result.txt')
    result_data = read_sources(os.path.join("config", "user_result.txt"))
    #local_data = read_sources(r'.\config\localsource.txt')
    local_data = read_sources(os.path.join("config", "localsource.txt"))
    #own_data = read_sources(r'.\output\ownsource.txt')
    own_data = read_sources(os.path.join("output", "ownsource.txt"))
    
    # 读取在线源
    #net_data = read_subscribe_sources(r'.\config\subscribe.txt')
    net_data = read_subscribe_sources(os.path.join("config", "subscribe.txt"))
    net_df = deduplicate(net_data)
    #save_df(net_df, r'.\output\netsource.txt')
    try:
        save_df(net_df, os.path.join("output", "netsource.txt"))
    except Exception as e: 
        logger.error(f"网络源写出失败:{e}")
        errorflag=True
    
    # 合并所有源
    if errorflag:
        all_data = local_data + own_data + net_data
    else:
        all_data = result_data + local_data + own_data + net_data
    all_df = deduplicate(all_data)
    # all_df['combined'] = all_df.apply(
    # lambda row: f"{row['name']},{row['url']}${row['extra']}",
    # axis=1
    # )
    all_df.drop(columns=['extra'], inplace=True)
    #save_df(all_df, r'.\output\allsource.txt')
    try:
        save_df(all_df, os.path.join("output", "allsource.txt"))
    except Exception as e: 
        logger.error(f"网络源写出失败:{e}")
    logger.info("模块2执行完毕")
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

















