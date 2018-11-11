import socket
import time
import struct
import os

from ask_computer import host_list
from logs import make_log
from ask_computer import port
from process_bar import process_bar
from zip_file import get_file_list
from zip_file import zip_dir
from zip_file import get_system_bytes


def sending_process(file_name, host_index):
    # 建立连接；
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定服务器IP地址；
    host = host_list[host_index]

    sock.connect((host, port))

    file_size = os.stat(file_name).st_size

    # 发送文件大小和文件名，注意这里不发送文件名的标志位，在本地表示为目标主机的编号；
    bite_format = '128sl' if get_system_bytes() else '128sq'
    file_head = struct.pack(bite_format,
                            os.path.basename(file_name)[1:].encode(),
                            file_size)

    sock.send(file_head)

    print("开始传输文件:", file_name)

    read_file = open(file_name, "rb")

    sended_size = 0
    while True:
        process_bar(float(sended_size) / file_size)

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


# 传输数据线程；
def transport_thread():

    while True:
        time.sleep(5)

        try:
            # 获得压缩的文件列表；
            file_list = get_file_list(zip_dir)
            for file in file_list:
                file_basename = os.path.basename(file)

                # 以tmp开头表示还未压缩完毕；
                if file_basename.startswith('tmp'):
                    continue

                host_index = int(file_basename[0])
                sending_process(file, host_index)

        except Exception as e:
            print(e)
