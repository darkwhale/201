import os

mask_file = os.path.join("mask","mask")

if not os.path.exists("mask"):
    os.mkdir("mask")

if not os.path.exists(mask_file):
    tmp_creator = open(mask_file, "w")
    tmp_creator.close()


# 写记录文件；
def write_mask(mask_str):
    with open(mask_file, 'a') as writer:
        writer.write(mask_str + '\n')


def is_in_mask(mask_str):
    with open(mask_file, "r") as reader:
        mask_list = reader.readlines()

    mask_files = [file.strip() for file in mask_list]

    return True if mask_str in mask_files else False
