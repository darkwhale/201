from zip_file import create_zip
from ask_computer import get_best_server
from zip_file import get_origin_size
from logs import make_log
from ask_computer import host_list
import threading
import time
import os
import shutil

import mask

# 存放数据的文件夹；
file_folder = "/home/zxy/Documents/test"


# 定义压缩文件线程,压缩文件夹folder；
def compress_folder(folder, in_compress):

    try:
        folder = os.path.abspath(folder)

        # 读取记录文件，获取目标主机；
        host_index = mask.get_mask(folder)

        # 为None表示未找到相关记录，需要重新询问主机；
        if host_index is None:
            # 取文件总大小；
            src_size = get_origin_size(folder)
            host_index = get_best_server(src_size)

            if host_index is None:
                print("未找到合适主机：", folder)
                make_log("WARNING", "未找到合适主机：" + folder)
                exit(1)

            else:
                mask.put_mask(folder, str(host_index))
                print("将向" + host_list[int(host_index)] + "发送数据")
                make_log("INFO", "将向" + (host_list[int(host_index)]) + "发送数据")

        # 压缩文件；
        make_log("INFO", "开始压缩数据：" + folder)
        print("开始压缩数据：", folder)

        create_zip(folder, host_index)

        # 删除该文件夹
        shutil.rmtree(folder)
        mask.remove_mask(folder)

        make_log("INFO", "数据压缩完毕：" + folder)
        print("\n压缩完毕：", folder)

    except Exception as e:
        print(e)

    finally:
        # 在in_compress列表中删除该元素；
        in_compress.remove(folder)


# 获取该类已开启的线程数；
def thread_nums(name='compress'):
    thread_list = [thread for thread in threading.enumerate()
                   if thread.getName().startswith(name)]

    return len(thread_list)


# 开始多线程压缩；
def compress(thread_num=8):
    # 定义三个列表，分别表示正在压缩的文件夹，全部的文件夹，待压缩的文件夹；
    in_compress = []
    all_compress = []

    while True:
        time.sleep(5)

        all_compress.clear()

        # 计算全部需要压缩的文件夹；
        for folder in os.listdir(file_folder):
            if folder.startswith("ok"):
                all_compress.append(os.path.join(file_folder, folder))

        # 去掉已经在处理的，则得到待压缩的文件夹；
        new_compress = [file for file in all_compress if file not in in_compress]

        # 计算最大可新建的线程数；
        free_thread_nums = thread_num - thread_nums("compress")

        # 最后，线程数不应该比文件夹的数量大；
        max_thread_num = free_thread_nums if free_thread_nums \
                                        < len(new_compress) else len(new_compress)

        # 开启max_thread_num个线程用于压缩数据；
        for i in range(max_thread_num):
            compress_thread = threading.Thread(target=compress_folder,
                                               args=(new_compress[i], in_compress),
                                               name="compress")

            # 将该文件夹放入in_compress列表中；
            in_compress.append(new_compress[i])

            compress_thread.start()



