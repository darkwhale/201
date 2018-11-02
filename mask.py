# -*- coding: UTF-8 -*-
import os
from zip_file import get_abspath_without_separator

mask_dir = "mask"

if not os.path.exists(mask_dir):
    os.mkdir(mask_dir)


# 获取标志记录文件状态；
# 返回0表示从未处理过；
# 返回"0","1","2"表示压缩完成；直接进行选择对应的主机索引传输即可；
# 2表示传输完成；即本机工作已实现；
def get_mask(file_dir):
    # 去掉文件名中的分隔符，因为分隔符不能存在于文件名中；
    file_dir = os.path.abspath(file_dir)
    file_dir = get_abspath_without_separator(file_dir)

    if not os.path.exists(os.path.join(mask_dir, file_dir)):
        return 0

    with open(os.path.join(mask_dir, file_dir), 'r') as mask_file:
        return mask_file.read().strip()


# 写入标志记录文件；
def put_mask(file_dir, symbol):
    file_dir = os.path.abspath(file_dir)

    file_dir = get_abspath_without_separator(file_dir)

    with open(os.path.join(mask_dir, file_dir), 'w') as mask_file:
        mask_file.write(str(symbol))


