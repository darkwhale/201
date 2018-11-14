from zip_file import create_zip
from logs import make_log
import threading
import time
import os

from mask import is_in_mask

from config import file_folder


# 定义压缩文件线程,压缩文件夹folder；
def compress_folder(folder, in_compress):

    try:
        folder = os.path.abspath(folder)

        # 压缩文件；
        make_log("INFO", "开始压缩数据：" + folder)
        print("开始压缩数据：", folder)

        create_zip(folder)

        # 删除该文件夹
        # shutil.rmtree(folder)

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


# 判断文件夹是否合法；
def is_legal(folder):
    symbol = True
    for sub_folder in os.listdir(folder):
        try:
            time.strptime(sub_folder, "%Y%m%d")
            if is_in_mask(os.path.join(folder, sub_folder)):
                print("文件夹已经处理过：", os.path.join(folder, sub_folder))
                symbol = False
        except Exception as e:
            print(e)
            symbol = False

    return symbol


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
            if folder.startswith("ok") and is_legal(os.path.join(file_folder, folder)):
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



