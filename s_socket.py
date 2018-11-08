# -*- coding: UTF-8 -*-
# 单线程传输数据；
import socket
import os
import struct
import process_bar
from ask_computer import host_list
from ask_computer import port
from zip_file import zip_dir
from zip_file import get_abspath_without_separator
from logs import make_log


def sending_process(file_name, host_index):
    # 建立连接；
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定服务器IP地址；
    host = host_list[host_index]

    sock.connect((host, port))

    file_size = os.stat(file_name).st_size

    file_head = struct.pack('128sl',
                            os.path.basename(file_name).encode(),
                            file_size)

    sock.send(file_head)

    print("开始传输文件:", file_name)

    read_file = open(file_name, "rb")

    sended_size = 0
    while True:
        process_bar.process_bar(float(sended_size) / file_size)

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


# 传输文件，file_dir为待传输的文件夹；为压缩文件；
def sending_file(file_dir, host_index):
    # 取绝对路径，防止和相对路径重复；
    file_dir = os.path.abspath(file_dir)

    # 定位到二级目录；
    file_dir = os.path.join(zip_dir, get_abspath_without_separator(file_dir))

    if not os.path.exists(file_dir):
        print("file not exists")
        exit(1)

    print("建立连接中----------------------------")
    print(file_dir)
    for file in os.listdir(file_dir):
        file = os.path.join(file_dir, file)
        # print(file)
        sending_process(file, host_index)

    # 传输完成；
    print("传输完成------------------------------")
    # noinspection PyBroadException
    try:
        os.rmdir(file_dir)
    except Exception:
        print("文件未发送完毕")


