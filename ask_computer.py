import socket

# port用于传输数据，ask_port用于发送请求获取系统状态；
port = 12345
ask_port = 12346

# 测试使用为本机host；
# host_list = ['192.168.100.47', '192.168.100.48', '192.168.100.49', ]
host_list = [socket.gethostname(), ]


# 询问获取状态最好的可用主机；
def get_best_server(src_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    best_server = None
    best_cpu = 100

    # 请求用字符串
    ask_symbol = "0" + str(src_size)

    for index, host in enumerate(host_list):
        sock.connect((host, ask_port))
        sock.send(ask_symbol.encode())

        status = sock.recv(1024).decode()

        if status.startswith("1"):
            cpu = float(status[1:])
            if cpu < best_cpu:
                best_cpu = cpu
                best_server = index

    # 关闭连接；
    sock.close()

    return best_server





