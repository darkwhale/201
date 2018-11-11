# -*- coding: UTF-8 -*-
import zipfile
import os
import process_bar
import platform

batch_size = "200M"
zip_dir = "zips"

# 创建zips文件夹；
if not os.path.exists(zip_dir):
    os.mkdir(zip_dir)


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
def create_zip(file_dir):
    # 转换为绝对路径，防止重复；
    file_dir = os.path.abspath(file_dir)
    # 创建二级目录
    zip_file_dir = os.path.join(zip_dir, get_abspath_without_separator(file_dir))
    if not os.path.exists(zip_file_dir):
        os.mkdir(zip_file_dir)

    # 用于返回所有的压缩好的文件名；
    name_list = []

    file_list = get_file_list(file_dir)

    zip_index = 0

    basename = os.path.basename(file_dir)

    for index, file in enumerate(file_list):
        # print(file)
        # 显示压缩进度；
        process_bar.process_bar(float(index) / len(file_list))
        # 判断是否已定义part_zip对象；
        if index == 0:
            part_zip = zipfile.ZipFile(os.path.join(zip_file_dir, basename +
                                                    str(zip_index)+'.zip'),
                                       'w', zipfile.ZIP_DEFLATED)

        part_zip.write(file, os.path.basename(file))

        if os.path.getsize(part_zip.filename) >= decode_batch_size(batch_size)\
                or index + 1 == len(file_list):
            # 插入到列表中；
            name_list.append(part_zip.filename)

            # 关闭旧的zip对象；
            part_zip.close()

            # 当不为最后一个文件时，创建新的压缩文件；
            if index + 1 != len(file_list):
                zip_index += 1
                part_zip = zipfile.ZipFile(
                    os.path.join(zip_file_dir, basename + str(zip_index)+'.zip'),
                    'w', zipfile.ZIP_DEFLATED)

    process_bar.process_bar(1)

    return name_list









