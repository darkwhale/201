"""
该文将将所有位于file_folder文件夹下的文件前面加"ok"，表示可以进行压缩；
"""
import os
from compress import file_folder


if __name__ == '__main__':

    for file in os.listdir(file_folder):
        dir_path = os.path.join(file_folder, file)
        os.rename(dir_path, os.path.join(file_folder, "ok" + file))
