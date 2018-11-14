import socket
import time
import struct
import os
import threading

from ask_computer import host_list
from ask_computer import get_best_server
from logs import make_log
from ask_computer import port
from zip_file import zip_dir
from zip_file import get_system_bytes
from compress import thread_nums


# 发送单个文件；
def sending_process(file_name, in_transport):

    try:
        # 先询问查找最合适的主机；
        src_size = os.path.getsize(file_name)
        host_index = get_best_server(src_size)

        if host_index is None:
            print("未找到合适主机：", file_name)
            make_log("WARNING", "未找到合适主机：" + file_name)
            raise NotImplementedError

        # 建立连接；
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务器IP地址；
        host = host_list[host_index]

        sock.connect((host, port))

        file_size = os.stat(file_name).st_size

        # 发送文件大小和文件名，注意这里不发送文件名的标志位，在本地表示为目标主机的编号；
        bite_format = '128sl' if get_system_bytes() else '128sq'
        file_head = struct.pack(bite_format,
                                os.path.basename(file_name).encode(),
                                file_size)

        sock.send(file_head)

        print("\n开始传输文件:", file_name)

        read_file = open(file_name, "rb")

        sended_size = 0
        while True:
            # process_bar(float(sended_size) / file_size)

            file_data = read_file.read(10240)

            if not file_data:
                break

            sock.send(file_data)

            sended_size += len(file_data)

        read_file.close()

        # 传输完毕后删除原压缩文件；
        os.remove(file_name)
        print()
        print("sending over:", file_name, '\n')

        make_log("INFO", "数据发送完毕： %s" % file_name)
        sock.close()
    except Exception as e:
        print(e)
    finally:
        in_transport.remove(file_name)


# 开始多线程传输；
def transport(thread_num):
    # 定义三个列表，分别表示正在压缩的文件夹，全部的文件夹，待压缩的文件夹；
    in_transport = []
    all_transport = []

    while True:
        time.sleep(5)

        all_transport.clear()

        # 计算全部需要压缩的文件夹；
        for folder in os.listdir(zip_dir):
            if not folder.startswith("tmp"):
                all_transport.append(os.path.join(zip_dir, folder))

        # 去掉已经在处理的，则得到待压缩的文件夹；
        new_transport = [file for file in all_transport if file not in in_transport]

        # 计算最大可新建的线程数；
        free_thread_nums = thread_num - thread_nums("transport")

        # 最后，线程数不应该比文件夹的数量大；
        max_thread_num = free_thread_nums if free_thread_nums \
                                             < len(new_transport) else len(new_transport)

        for i in range(max_thread_num):
            compress_thread = threading.Thread(target=sending_process,
                                               args=(new_transport[i], in_transport),
                                               name="transport")

            in_transport.append(new_transport[i])

            compress_thread.start()
