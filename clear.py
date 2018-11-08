import shutil
import sys
import os
from mask import mask_dir
from zip_file import get_abspath_without_separator
from zip_file import zip_dir
from logs import make_log


if __name__ == '__main__':
    file_dir = sys.argv[1]
    file_dir = os.path.abspath(file_dir)

    make_log("WARNING", "清除数据记录" + file_dir)

    file_dir = get_abspath_without_separator(file_dir)

    if os.path.exists(os.path.join(mask_dir, file_dir)):
        os.remove(os.path.join(mask_dir, file_dir))

    if os.path.exists(zip_dir):
        shutil.rmtree(zip_dir)
        os.mkdir(zip_dir)

