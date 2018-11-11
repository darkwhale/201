from zip_file import create_zip
from ask_computer import get_best_server
from zip_file import get_origin_size
from logs import make_log
from ask_computer import host_list
import time
import os

import mask

# 存放数据的文件夹；
file_folder = "/home/zxy/Documents/test"


# 定义压缩文件线程；
def compress_thread():
    # 循环检测；
    while True:
        time.sleep(5)

        try:
            for file_sub_dir in os.listdir(file_folder):

                # 若文件不以ok开头，则不处理；
                if not file_sub_dir.startswith('ok'):
                    continue

                # 取绝对路径；
                file_sub_dir = os.path.abspath(os.path.join(file_folder, file_sub_dir))

                # 读取记录文件，获取目标主机；
                host_index = mask.get_mask(file_sub_dir)

                # 为None表示未找到相关记录，需要重新询问主机；
                if host_index is None:
                    # 取文件总大小；
                    src_size = get_origin_size(file_sub_dir)
                    host_index = get_best_server(src_size)

                    if host_index is None:
                        print("未找到合适主机：", file_sub_dir)
                        make_log("WARNING", "未找到合适主机：" + file_sub_dir)

                    else:
                        mask.put_mask(file_sub_dir, str(host_index))
                        print("将向" + host_list[int(host_index)] + "发送数据")
                        make_log("INFO", "将向" + (host_list[int(host_index)]) + "发送数据")

                # 压缩文件；
                make_log("INFO", "开始压缩数据：" + file_sub_dir)
                print("开始压缩数据：", file_sub_dir)

                create_zip(file_sub_dir, host_index)

                os.rmdir(file_sub_dir)

                make_log("INFO", "数据压缩完毕：" + file_sub_dir)
                print("\n压缩完毕：", file_sub_dir)

        except Exception as e:
            print(e)
            pass





