# 导入所有模块
from modules import module1_capture, module2_combine, module3_clean, module4_split # 注意导入顺序
import os

if __name__ == '__main__':
    print("开始执行模块1：捕获信号源")
    input_file = os.path.join("config", "channels.txt")
    output_file = os.path.join("output", "ownsource.txt")
    module1_capture.main(input_file, output_file)

    print("开始执行模块2：组合信号源")
    module2_combine.combine_sources()

    print("开始执行模块3：清理信号源") # <<< 新增 >>>
    module3_clean.main() # <<< 新增 >>>

    print("开始执行模块4：拆分信号源")
    # 注意：模块3现在应该读取清理后的文件
    # 需要修改 module3_split.py 中读取的文件路径
    module4_split.split_channels()

    print("✅ 所有模块执行完成")