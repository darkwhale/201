# -*- coding: UTF-8 -*-
import zipfile
import os
import process_bar
import platform
import time

batch_size = "1M"
zip_dir = "zips"

# 创建zips文件夹；
if not os.path.exists(zip_dir):
    os.mkdir(zip_dir)


# 判断系统位数；
def get_system_bytes():
    bite, system = platform.architecture()
    if bite.startswith('3'):
        return False
    if bite.startswith('6'):
        return True
    return True


# 去掉路径中的分隔符；
def get_abspath_without_separator(path):
    system = platform.system()

    if system == "Linux":
        path = path.replace('/', '')
    if system == "Windows":
        path = path[2:].replace('\\', '')
    return path


# 标准化块大小到字节；
def decode_batch_size(batch_str):
    if batch_str.endswith("K"):
        return int(batch_str[:-1])*1024

    if batch_str.endswith("M"):
        return int(batch_str[:-1])*1024*1024

    if batch_str.endswith("G"):
        return int(batch_str[:-1])*1024*1024*1024


# 获取文件夹下所有的文件路径；
def get_file_list(file_dir):
    file_list = []

    for root, dirs, files in os.walk(file_dir):
        for name in files:
            file_list.append(os.path.join(root, name))

    return file_list


def get_origin_size(file_dir):
    file_size = 0

    for file in get_file_list(file_dir):
        file_size += os.path.getsize(file)

    return file_size


# 获取文件月份，将添加到压缩文件名；
def get_month(basename):
    # 解析文件日期；
    return basename[:6]


def get_database(basename):
    return basename[6:]


# 分块创建压缩文件，返回压缩的小文件列表；
def create_zip(file_dir, host_index):

    # 用于返回所有的压缩好的文件名；
    name_list = []

    file_list = get_file_list(file_dir)

    basename = os.path.basename(file_dir)
    print(basename)

    for index, file in enumerate(file_list):
        # print(file)
        # 显示压缩进度；
        process_bar.process_bar(float(index) / len(file_list))
        # 判断是否已定义part_zip对象；
        if index == 0:
            old_zip_file_name = os.path.join(zip_dir, "tmp" + host_index + basename + str(time.time())+'.zip')
            part_zip = zipfile.ZipFile(old_zip_file_name,
                                       'w', zipfile.ZIP_DEFLATED)

        part_zip.write(file, os.path.basename(file))

        if os.path.getsize(part_zip.filename) >= decode_batch_size(batch_size)\
                or index + 1 == len(file_list):
            # 插入到列表中；
            name_list.append(part_zip.filename)

            # 关闭旧的zip对象；
            part_zip.close()

            # 压缩完毕重命名文件，表示压缩完毕，可以进行传输，并删除原文件；
            # 注意，该语句需要放置在上一句后面，避免windows上的文件保护；
            os.rename(old_zip_file_name, old_zip_file_name[:5] + old_zip_file_name[8:])

            # 当不为最后一个文件时，创建新的压缩文件；
            if index + 1 != len(file_list):
                old_zip_file_name = os.path.join(zip_dir, "tmp" + host_index + basename + str(time.time()) + '.zip')
                part_zip = zipfile.ZipFile(old_zip_file_name, 'w', zipfile.ZIP_DEFLATED)

        # 删除原文件；避免重复压缩；
        os.remove(file)

    process_bar.process_bar(1)

    return name_list









