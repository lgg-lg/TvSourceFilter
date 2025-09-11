# 导入所有模块
from modules import module1_capture, module2_combine, module3_clean, module4_split, module5_pick,module6_result # 注意导入顺序
import os

if __name__ == '__main__':
    print("开始执行模块1：捕获信号源")
    input_file = os.path.join("config", "channels.txt")
    output_file = os.path.join("output", "ownsource.txt")
    module1_capture.main(input_file, output_file)

    print("开始执行模块2：组合信号源")
    flag=module2_combine.combine_sources()

    print("开始执行模块3：清理信号源") # <<< 新增 >>>
    module3_clean.main() # <<< 新增 >>>

    print("开始执行模块4：拆分信号源")
    # 注意：模块3现在应该读取清理后的文件
    module4_split.split_channels()

    print("开始执行模块5：优选频道信号源") # <<< 新增 >>>
    module5_pick.main() # <<< 新增 >>>

    print("开始执行模块6：替换用户频道列表") # <<< 新增 >>>
    module6_result.main() # <<< 新增 >>>

    print("✅ 所有模块执行完成")




