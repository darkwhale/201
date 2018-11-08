"""
总文件，检测待发送文件，传输文件；
"""
from transport import transport
import os
import time

file_folder = "/home/zxy/Documents/test"


if __name__ == '__main__':
    # 设置标示位，当上一次有文件时，将不等待直接开始下一次循环；否则等待；
    no_file = True
    # 循环检测新文件；
    while True:
        if no_file:
            time.sleep(5)

        try:
            dir_list = os.listdir(file_folder)
            no_file = True

            for dirs in dir_list:
                no_file = False
                dirs = os.path.abspath(dirs)
                database_name = os.path.basename(dirs)
                transport(dirs)

        except Exception as e:
            print(e)



