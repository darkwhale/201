"""
总文件，检测待发送文件，传输文件；
"""
from transport import transport
from compress import compress
from logs import make_log
import threading

if __name__ == '__main__':

    # 开启压缩数据线程，用于压缩数据；
    compress_thread = threading.Thread(target=compress, args=(5, ))
    compress_thread.start()
    print("数据压缩进程已启动，准备压缩数据")
    make_log("INFO", "数据压缩进程已启动，准备压缩数据")

    # 开启传输数据线程，用于传输数据；
    transport_thread = threading.Thread(target=transport, args=(5, ))
    transport_thread.start()
    print("数据传输进程已启动，准备传输数据")
    make_log("INFO", "数据传输进程已启动，准备压缩数据")


