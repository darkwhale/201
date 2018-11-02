# -*- coding: UTF-8 -*-
import sys
import zip_file
import mask
import ask_computer
from ask_computer import host_list
from logs import make_log

# m_socket为多线程，s_socket为单线程；需要测试在实际环境中使用多线程是否会加速；
# from m_socket import sending_file
from s_socket import sending_file


if __name__ == '__main__':
    # 待传输的文件夹；
    file_dir = sys.argv[1]
    database_name = sys.argv[2]

    # 记录日志文件
    make_log("INFO", "running" + file_dir + " " + database_name)

    # src_size为未压缩之前的文件夹大小；
    src_size = zip_file.get_origin_size(file_dir)
    symbol = mask.get_mask(file_dir)

    if src_size == 0:
        print("文件夹为空")
        make_log()
        exit(1)

    # noinspection PyBroadException
    try:

        # 未处理；则需要完成压缩-传输的工作；
        if symbol == 0:
            # 第一步，请求获得最适合的主机ip地址；
            make_log("INFO", "请求主机------------")
            best_server = ask_computer.get_best_server(src_size)

            if best_server is None:
                print("no available server can be found!")
                make_log("ERROR", "未找到合适的主机")
                make_log()
                exit(1)

            make_log("INFO", "将向%s发送数据" % host_list[best_server])
            print("将向 %s 传输数据----------" % host_list[best_server])

            # 获得即将得到的压缩文件；
            print("压缩文件------------------------------")
            make_log("INFO", "压缩文件".ljust(20, '-'))

            file_list = zip_file.create_zip(file_dir, database_name)
            print("压缩完成------------------------------")
            make_log("INFO", "压缩完成".ljust(20, '-'))

            # 压缩完毕则将标志位设置为目标主机的索引，有3种值；表示压缩完成，可以进行后续工作；
            mask.put_mask(file_dir, best_server)

            # 传输文件；
            make_log("INFO", "准备发送文件---------")
            sending_file(file_dir, best_server)

            make_log("INFO", "文件传输完毕---------")
            mask.put_mask(file_dir, 3)

            make_log()
            exit()

        # 压缩完成，则直接进行传输即可；
        if symbol in ["0", "1", "2"]:
            print("压缩已完成，准备传输文件".ljust(20, '-'))
            make_log("INFO", "压缩已完成，将向%s发送数据" % host_list[int(symbol)])

            print("将向 %s 传输数据----------" % host_list[int(symbol)])
            sending_file(file_dir, int(symbol))

            mask.put_mask(file_dir, 3)
            make_log("INFO", "数据传输完毕".ljust(20, '-'))
            make_log()
            exit()

        # 所有工作完成，则提示并返回；
        if symbol == "3":
            print('all work are finished, '
                  'you may want to try "python clear.py folder" '
                  'to clear all the masks')
            make_log("WARNING", "该数据已处理过！".ljust(20, '-'))
            exit()

    except Exception:
        pass




