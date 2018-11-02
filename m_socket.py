# -*- coding: UTF-8 -*-
# 有点问题，多线程发送数据会出现连接失败；目前只能使用s_socket发送数据；
# 尝试使用多进程代替多线程；
# 最后发现问题竟然是发送端和接收端port不一致导致的，wtf???
import socket
import os
# import time
import struct
import process_bar
from multiprocessing import Process
from ask_computer import host_list
from ask_computer import port
from zip_file import zip_dir
from zip_file import get_abspath_without_separator


def sending_process(file_name, host_index):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定服务器IP地址；
    host = host_list[host_index]

    sock.connect((host, port))

    file_size = os.stat(file_name).st_size

    file_head = struct.pack('128sl',
                            os.path.basename(file_name).encode(),
                            file_size)

    sock.send(file_head)

    print("start sending file:", file_name)

    read_file = open(file_name, "rb")

    sended_size = 0
    while True:
        process_bar.process_bar(float(sended_size) / file_size)

        file_data = read_file.read(1024)

        if not file_data:
            break

        sock.send(file_data)

        sended_size += len(file_data)

    read_file.close()

    print("sending over:", file_name, '\n')


# 传输文件，file_dir为待传输的文件夹；为压缩文件；
def sending_file(file_dir, host_index):
    # 取绝对路径，防止和相对路径重复；
    file_dir = os.path.abspath(file_dir)

    # 定位到二级目录；
    file_dir = os.path.join(zip_dir, get_abspath_without_separator(file_dir))

    if not os.path.exists(file_dir):
        print("file not exists")
        exit(1)

    processes = []

    for file in os.listdir(file_dir):
        file = os.path.join(file_dir, file)
        new_process = Process(target=sending_process, args=(file, host_index, ))
        new_process.start()
        processes.append(new_process)

    for process in processes:
        process.join()

        # 传输完成；
        print("传输完成------------------------------")
        # noinspection PyBroadException
        try:
            os.rmdir(file_dir)
        except Exception:
            print("文件未发送完毕")


