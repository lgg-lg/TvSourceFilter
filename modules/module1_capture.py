# import urllib.parse
# import time
# from requests_html import HTMLSession
# from bs4 import BeautifulSoup
# import time
# import requests
# import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from playwright.sync_api import sync_playwright, TimeoutError


# def extract_onclick_content(onclick_text):
#     """
#     从onclick属性中提取括号内的内容
#     """
#     # 找到第一个 "(" 和最后一个 ")" 之间的内容
#     start = onclick_text.find('(')
#     end = onclick_text.rfind(')')
    
#     if start != -1 and end != -1 and start < end:
#         content = onclick_text[start+1:end]
#         # 移除首尾的引号（如果有的话）
#         content = content.strip().strip('"\'')
#         return content
#     return ""

# def search_and_extract(search_term,type=1):
#     """
#     搜索并提取符合条件的内容
#     """
#     results = []
    
#     try:
#         # 构建搜索URL
#         encoded_term = urllib.parse.quote(search_term)
#         if type == 1:
#             url = f"http://tonkiang.us/?iptv={encoded_term}"
#         elif type == 2:
#             url = f"http://www.foodieguide.com/iptvsearch/?iptv={encoded_term}"
#         print(f"正在访问: {url}")
        
#         # 发送请求
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         response = requests.get(url, headers=headers, timeout=10)
#         #response = requests.get(url, timeout=10)
#         #response.encoding = 'utf-8'
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # 找到所有的 <div class="imgw"> 元素
#             imgw_divs = soup.find_all('div', class_='imgw')
            
#             print(f"找到 {len(imgw_divs)} 个 imgw 元素")
            
#             for div in imgw_divs:

#                 try:
#                     # 找到当前 'imgw' div 的祖父元素
#                     grandparent = div.parent.parent
#                     if grandparent:
#                         # 找到祖父元素的前一个同级元素，并确保它是一个标签而不是文本节点
#                         previous_sibling = grandparent.find_previous_sibling()
#                         while previous_sibling and not getattr(previous_sibling, 'name', None):
#                             previous_sibling = previous_sibling.find_previous_sibling()

#                         # 如果找到了前一个同级元素，就在其中查找 class="tip" 的 div
#                         if previous_sibling:
#                             tip_div = previous_sibling.find('div', class_='tip')
#                             if tip_div:
#                                 # 获取并清理文本内容
#                                 tip_text = tip_div.get_text(strip=True)
#                                 print(f"提取到 tip 内容: {tip_text}")
#                 except Exception as e:
#                     print(f"查找 tip 内容时出错: {e}")


                
#                 # 查找 img 元素，src 属性为 "copy.png"
#                 img_elements = div.find_all('img', src='copy.png')
                
#                 for img in img_elements:
#                     # 找到包含这个 img 的父元素中的 onclick 属性
#                     parent = img.parent
#                     onclick_value = None
                    
#                     # 向上查找包含 onclick 属性的元素
#                     while parent and parent != div:
#                         if parent.has_attr('onclick'):
#                             onclick_value = parent.get('onclick')
#                             break
#                         parent = parent.parent
                    
#                     # 如果在当前元素上没找到，检查同级元素
#                     if not onclick_value:
#                         # 检查同级元素的 onclick 属性
#                         siblings = div.find_all(attrs={'onclick': True})
#                         for sibling in siblings:
#                             if sibling.get('src') == 'copy.png' or sibling.find('img', src='copy.png'):
#                                 onclick_value = sibling.get('onclick')
#                                 break
                    
#                     # 如果还是没找到，检查 div 本身
#                     if not onclick_value and div.has_attr('onclick'):
#                         onclick_value = div.get('onclick')
                    
#                     # 如果找到了 onclick 属性，提取其中的内容
#                     if onclick_value:
#                         extracted_content = extract_onclick_content(onclick_value)
#                         if extracted_content:
#                             if tip_text!= None:
#                                 results.append([tip_text, extracted_content])
#                             else:
#                                 results.append([search_term, extracted_content])
#                             print(f"提取到内容: {extracted_content}")
                    
#         else:
#             print(f"请求失败，状态码: {response.status_code}")
            
#     except Exception as e:
#         print(f"处理搜索词 '{search_term}' 时出错: {str(e)}")
    
#     return results

# def new_search_and_extract(search_term,type=1):
#     """
#     搜索并提取符合条件的内容
#     """
#     results = []
    
#     try:
#         # 构建搜索URL
#         encoded_term = urllib.parse.quote(search_term)
#         if type == 1:
#             url = f"http://tonkiang.us/?iptv={encoded_term}"
#         elif type == 2:
#             url = f"http://www.foodieguide.com/iptvsearch/?iptv={encoded_term}"
#         print(f"正在访问: {url}")
        
#         # 发送请求
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         response = requests.get(url, headers=headers, timeout=10)
#         #response = requests.get(url, timeout=10)
#         #response.encoding = 'utf-8'
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # 1. 直接找到所有包含 onclick 功能的 copy.png 图片
#             # 这是我们每次循环处理的基点
#             all_copy_images = soup.find_all('img', src='copy.png')
#             print(f"找到 {len(all_copy_images)} 个 copy.png 图片")
            
#             for img in all_copy_images:
#                 # 初始化本次循环的结果变量
#                 tip_text = None
#                 extracted_content = None

#                 # --- 任务A: 提取 onclick 内容 ---
#                 onclick_value = None
#                 # 向上查找最近的带有 onclick 属性的父元素，或者图片本身就有
#                 clickable_element = img.find_parent(attrs={'onclick': True})
#                 if img.has_attr('onclick'): # 优先检查img标签自身
#                     onclick_value = img['onclick']
#                 elif clickable_element: # 否则检查其父元素
#                     onclick_value = clickable_element['onclick']
                
#                 if onclick_value:
#                     # 使用你已有的函数来提取内容
#                     extracted_content = extract_onclick_content(onclick_value)
                
#                 # --- 任务B: 查找对应的 tip_text ---
#                 # 从当前 img 标签的位置，向前搜索最近的 <div class="channel">
#                 # find_previous() 是实现这个逻辑的关键
#                 channel_div = img.find_previous('div', class_='channel')
                
#                 if channel_div:
#                     # 在找到的 channel_div 内部，查找 class="tip" 的 div
#                     tip_div = channel_div.find('div', class_='tip')
#                     if tip_div:
#                         tip_text = tip_div.get_text(strip=True)

#                 # --- 任务C: 存储结果 ---
#                 # 确保我们同时找到了有用的 tip 和 onclick 内容再存入
#                 if tip_text and extracted_content:
#                     results.append([tip_text, extracted_content])
#                     print(f"关联成功: [Tip: '{tip_text}', Content: '{extracted_content}']")
#                 else:
#                     # 打印日志，方便调试为什么没有成功关联
#                     print(f"关联失败: Tip={'找到' if tip_text else '未找到'}, Content={'找到' if extracted_content else '未找到'}")

#         else:
#             print(f"请求失败，状态码: {response.status_code}")
                
#     except Exception as e:
#         print(f"处理搜索词 '{search_term}' 时出错: {str(e)}")

#     return results



# def get_decrypted_links(search_term):
#     """
#     Launches a browser using Playwright to scrape dynamically loaded content.
#     """
#     #encoded_term = urllib.parse.quote(search_term)
#     url = f"https://iptv-search.com/zh-hans/search/?q={search_term}"
#     results = []
#     with sync_playwright() as p:
#         # Launch a browser. 'headless=True' means the browser runs in the background.
#         # Set 'headless=False' if you want to see the browser window.
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()

#         try:
#             print(f"Navigating to: {url}")
#             # Navigate to the page
#             page.goto(url, timeout=60000) # Increase timeout to 60 seconds

#             print("Waiting for dynamic content to load...")
#             # Wait for the first element with the class 'decrypted-link' to appear.
#             # This is a reliable way to wait for the JavaScript to execute.
#             page.wait_for_selector('span.decrypted-link', state='visible', timeout=30000)
#             print("Content loaded. Extracting links...")

#             # Locate all span elements with the specified class
#             link_spans = page.locator('span.decrypted-link').all()

#             if not link_spans:
#                 print("No elements with class 'decrypted-link' were found.")
#                 return []

#             # Loop through all found elements and extract their text content
#             for span in link_spans:
#                 link_text = span.text_content()
#                 if link_text:
#                     results.append([search_term,link_text.strip()])

#         except TimeoutError:
#             print("Timed out waiting for the 'decrypted-link' elements to appear.")
#             print("The page might have changed, or the content did not load as expected.")
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#         finally:
#             # Always close the browser
#             browser.close()

#     return results


# def main(input_file, output_file):
#     # input_file = r"E:\TV\扒源代码\channel.txt"  # 输入文件名
#     # output_file = r"E:\TV\扒源代码\results.txt"      # 输出文件名

#     all_results = []
    
#     try:
#         # 读取搜索词文件
#         with open(input_file, 'r', encoding='utf-8') as f:
#             search_terms = [line.strip() for line in f if line.strip()]
        
#         print(f"共读取到 {len(search_terms)} 个搜索词")
        
#         # 逐个处理每个搜索词
#         for i, term in enumerate(search_terms, 1):
#             print(f"\n处理第 {i}/{len(search_terms)} 个: {term}")
            
#             # 搜索并提取内容
#             results = new_search_and_extract(term,1)
#             all_results.extend(results)
#             # 添加延时避免请求过于频繁
#             if i < len(search_terms):
#                 time.sleep(1)
#         # 逐个处理每个搜索词,这个方法是用requests_html的，不太稳定而且需要翻墙
#         for i, term in enumerate(search_terms, 1):
#             print(f"\n处理第 {i}/{len(search_terms)} 个: {term}")
            
#             # 搜索并提取内容
#             results2 = get_decrypted_links(term)
#             if len(results2) > 0:
#                 #取第一个结果
#                 all_results.extend(results2[0])
#             # 添加延时避免请求过于频繁
#             if i < len(search_terms):
#                 time.sleep(1)


#         # 将结果写入输出文件
#         with open(output_file, 'w', encoding='utf-8') as f:
#             for search_term, extracted_content in all_results:
#                 f.write(f"{search_term},{extracted_content}\n")
#         dictionary = {}
#         with open (output_file, 'r', encoding='utf-8') as f:
#             for line in f:
#                 fields = line.strip().split(',')
#                 if len(fields) == 2:   
#                     key, value = fields
#                     if key not in dictionary:
#                         dictionary[key] = list()
#                     dictionary[key].append(value)
#                     dictionary[key] = list(set(dictionary[key]))  # 去重
#         #将output_file中的内容清除后写入新的文件
#         with open(output_file, 'w', encoding='utf-8') as f:
#             for key, values in dictionary.items():
#                 for value in values:
#                     f.write(f"{key},{value}\n")
        
#         print(f"\n处理完成！共提取到 {len(all_results)} 条结果")
#         print(f"结果已保存到 {output_file}")
        
#     except FileNotFoundError:
#         print(f"错误：找不到输入文件 {input_file}")
#     except Exception as e:
#         print(f"程序执行出错: {str(e)}")





# if __name__ == "__main__":
#     # input_file = r"E:\TV\扒源代码\channel.txt"  # 输入文件名
#     # output_file = r"E:\TV\扒源代码\results.txt"      # 输出文件名
#     input_file = r".\config\channels.txt"  # 输入文件名
#     output_file = r".\config\ownsource.txt"      # 输出文件名
#     main(input_file,output_file)

# # results = []  
# # try:
# #     # 构建搜索URL
# #     #encoded_term = urllib.parse.quote(search_term)
# #     url = f"https://iptv-search.com/zh-hans/search/?q=中国大陆&page=1"
# #     print(f"正在访问: {url}")
    
# #     # 发送请求
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# #     }
    
# #     response = requests.get(url, headers=headers, timeout=10)
    
# #     if response.status_code == 200:
# #         soup = BeautifulSoup(response.text, 'html.parser')
# #         with open(r"E:\TV\扒源代码\11.txt", 'w', encoding='utf-8') as f:
# #             f.write(soup.prettify())
                
# #     else:
# #         print(f"请求失败，状态码: {response.status_code}")
        
# # except Exception as e:
# #     print(f"处理出错: {str(e)}")



# # # 设置 Selenium WebDriver
# # # 您需要根据您的 Chrome 版本下载对应的 chromedriver
# # # 并将其路径配置好，或者使用 webdriver-manager 自动管理
# # options = webdriver.ChromeOptions()
# # options.add_argument('--headless')  # 无头模式，不打开浏览器界面
# # driver = webdriver.Chrome(options=options)

# # try:
# #     # 访问网页
# #     url = "https://iptv-search.com/zh-hans/search/?q=中国大陆&page=1"
# #     driver.get(url)

# #     # 等待 JavaScript 执行完成，这里简单地等待几秒
# #     # 更稳健的方法是使用 WebDriverWait 等待特定元素加载完成
# #     time.sleep(5)

# #     # 获取渲染后的页面源码
# #     page_source = driver.page_source

# #     # 使用 BeautifulSoup 解析
# #     soup = BeautifulSoup(page_source, 'html.parser')

# #     # 现在您可以正常查找元素了
# #     decrypted_links = soup.find_all('span', class_='decrypted-link')
# #     for link_span in decrypted_links:
# #         # 假设链接是作为文本内容或者在某个属性中
# #         link = link_span.get_text(strip=True)
# #         if not link:
# #              # 有时内容可能在子标签中，或者需要更复杂的解析
# #              # 根据实际情况调整
# #              if link_span.a:
# #                  link = link_span.a['href']
# #         print(link)


# # except Exception as e:
# #     print(f"处理出错: {str(e)}")

# # finally:
# #     # 关闭浏览器
# #     driver.quit()

# modules/module1_capture.py

import urllib.parse
import time
import os
from bs4 import BeautifulSoup
import requests
import logging
from playwright.sync_api import sync_playwright, TimeoutError

# --- 配置日志 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_onclick_content(onclick_text):
    """
    从onclick属性中提取括号内的内容
    """
    if not onclick_text:
        return ""
    # 找到第一个 "(" 和最后一个 ")" 之间的内容
    start = onclick_text.find('(')
    end = onclick_text.rfind(')')
    
    if start != -1 and end != -1 and start < end:
        content = onclick_text[start+1:end]
        # 移除首尾的引号（如果有的话）
        content = content.strip().strip('"\'')
        return content
    return ""

def new_search_and_extract(search_term, type=1):
    """
    搜索并提取符合条件的内容 (优化版)
    """
    results = []
    
    try:
        # 构建搜索URL
        encoded_term = urllib.parse.quote(search_term)
        if type == 1:
            url = f"http://tonkiang.us/?iptv={encoded_term}"
        elif type == 2:
            url = f"http://www.foodieguide.com/iptvsearch/?iptv={encoded_term}"
        logger.info(f"正在访问: {url}")
        
        # 发送请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15) # 增加超时时间
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. 直接找到所有包含 onclick 功能的 copy.png 图片
            all_copy_images = soup.find_all('img', src='copy.png')
            logger.info(f"找到 {len(all_copy_images)} 个 copy.png 图片")
            
            for img in all_copy_images:
                tip_text = None
                extracted_content = None

                # --- 任务A: 提取 onclick 内容 ---
                onclick_value = None
                # 向上查找最近的带有 onclick 属性的父元素，或者图片本身就有
                clickable_element = img.find_parent(attrs={'onclick': True})
                if img.has_attr('onclick'): # 优先检查img标签自身
                    onclick_value = img['onclick']
                elif clickable_element: # 否则检查其父元素
                    onclick_value = clickable_element['onclick']
                
                if onclick_value:
                    # 使用你已有的函数来提取内容
                    extracted_content = extract_onclick_content(onclick_value)
                
                # --- 任务B: 查找对应的 tip_text ---
                # 从当前 img 标签的位置，向前搜索最近的 <div class="channel">
                channel_div = img.find_previous('div', class_='channel')
                
                if channel_div:
                    # 在找到的 channel_div 内部，查找 class="tip" 的 div
                    tip_div = channel_div.find('div', class_='tip')
                    if tip_div:
                        tip_text = tip_div.get_text(strip=True)

                # --- 任务C: 存储结果 ---
                if tip_text and extracted_content:
                    results.append([tip_text, extracted_content])
                    logger.debug(f"关联成功: [Tip: '{tip_text}', Content: '{extracted_content}']")
                else:
                    logger.debug(f"关联失败: Tip={'找到' if tip_text else '未找到'}, Content={'找到' if extracted_content else '未找到'}")

        else:
            logger.warning(f"请求失败，状态码: {response.status_code} for {url}")
                
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求错误 (搜索词 '{search_term}'): {e}")
    except Exception as e:
        logger.error(f"处理搜索词 '{search_term}' 时出错: {e}")

    return results

def get_decrypted_links(search_term):
    """
    使用 Playwright 抓取动态加载的内容。
    """
    url = f"https://iptv-search.com/zh-hans/search/?q={urllib.parse.quote(search_term)}"
    results = []
    logger.info(f"启动 Playwright 访问: {url}")
    try:
        with sync_playwright() as p:
            # Launch browser in headless mode
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the page
            page.goto(url, timeout=60000) # 60 seconds timeout

            # Wait for the first element with the class 'decrypted-link' to appear.
            page.wait_for_selector('span.decrypted-link', state='visible', timeout=30000)
            logger.info("内容加载完成，开始提取链接...")

            # Locate all span elements with the specified class
            link_spans = page.locator('span.decrypted-link').all()

            if not link_spans:
                logger.info("未找到 class 为 'decrypted-link' 的元素。")
                browser.close()
                return []

            # Loop through all found elements and extract their text content
            for span in link_spans:
                link_text = span.text_content()
                if link_text:
                    results.append([search_term, link_text.strip()])
            
            browser.close()

    except TimeoutError:
        logger.error("等待 'decrypted-link' 元素超时。页面可能未按预期加载。")
    except Exception as e:
        logger.error(f"Playwright 执行过程中发生错误: {e}")
        
    if results:
        logger.info(f"Playwright 成功提取到 {len(results)} 条结果。")
    else:
        logger.info("Playwright 未提取到任何结果。")
    return results

def deduplicate_and_save(results, output_file):
    """对结果进行去重并保存到文件"""
    if not results:
        logger.warning("没有结果需要保存。")
        return

    # 使用字典进行去重，键为频道名，值为URL集合
    dictionary = {}
    for item in results:
        if len(item) >= 2:
            key, value = item[0], item[1]
            if key not in dictionary:
                dictionary[key] = set()
            dictionary[key].add(value)
        else:
            logger.debug(f"跳过格式不正确的结果项: {item}")

    # 写入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for key, values in dictionary.items():
                for value in values:
                    f.write(f"{key},{value}\n")
        logger.info(f"结果已去重并保存到 {output_file}, 共 {len(dictionary)} 个唯一频道。")
    except IOError as e:
        logger.error(f"写入文件 {output_file} 时出错: {e}")


def main(input_file, output_file, exflag=False):
    """主函数"""
    all_results = []
    
    # 确保 output 目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    search_terms = []
    try:
        # 读取搜索词文件
        with open(input_file, 'r', encoding='utf-8') as f:
            #search_terms = [line.strip() for line in f if line.strip()]
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if line and not line.startswith('#'):
                    search_terms.append(line)
        logger.info(f"共读取到 {len(search_terms)} 个搜索词")
        
        # --- 处理每个搜索词 (Tonkiang/foodieguide) ---
        for i, term in enumerate(search_terms, 1):
            logger.info(f"\n处理第 {i}/{len(search_terms)} 个: {term}")
            
            # 搜索并提取内容 (Tonkiang)
            results = new_search_and_extract(term, 1)
            all_results.extend(results)
            
            # 添加延时避免请求过于频繁
            if i < len(search_terms):
                time.sleep(1)
        
        # --- 处理每个搜索词 (iptv-search.com) ---
        # 注意：此网站可能需要翻墙或不稳定，可根据需要启用/禁用
        if exflag:
            for i, term in enumerate(search_terms, 1):
                logger.info(f"\n[Playwright] 处理第 {i}/{len(search_terms)} 个: {term}")
                results2 = get_decrypted_links(term)
                if  len(results2) > 0:
                    all_results.extend(results2[0])
                if i < len(search_terms):
                    time.sleep(2) # Playwright 请求间隔可稍长

        # 去重并保存结果
        deduplicate_and_save(all_results, output_file)
        
        logger.info(f"\n✅ 模块1处理完成！共尝试提取到 {len(all_results)} 条结果 (去重后保存)。")
        
    except FileNotFoundError:
        logger.error(f"❌ 错误：找不到输入文件 {input_file}")
    except Exception as e:
        logger.error(f"❌ 程序执行出错: {e}")


# 如果直接运行此脚本，则执行 main 函数
# 注意：在 main.py 中调用时，应使用 module1_capture.main(...)
if __name__ == "__main__":
    # 使用相对于项目根目录的路径
    input_file = os.path.join("config", "channels.txt")
    output_file = os.path.join("output", "ownsource.txt")
    main(input_file, output_file)

