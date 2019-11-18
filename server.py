# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys
import traceback
from threading import Thread
import game


def main():
    start_server()


def start_server():
    host = "127.0.0.1"
    port = 8888         # arbitrary non-privileged port
    players = []

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        players.append(game.create_p(len(players) ,[],connection))
        print(players)
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port, players)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, players, max_buffer_size = 5120):
    is_active = True

    while is_active:
        if (len(players)==2):
            is_active = start_game(connection, players, ip, port, max_buffer_size, is_active)

        # if (len(players)==2):
        #     data = "----cards-------"
        #     connection.sendall(bytes(data, 'utf8'))

        #     client_input = receive_input(connection, max_buffer_size)

        #     if "--QUIT--" in client_input:
        #         print("Client is requesting to quit")
        #         connection.close()
        #         print("Connection " + ip + ":" + port + " closed")
        #         is_active = False
        #     else:
        #         print("{}".format(client_input))
        #         connection.sendall("-".encode("utf8"))


def start_game(connection, players, ip, port, max_buffer_size, is_active):
    data = "----cards-------"
    connection.sendall(bytes(data, 'utf8'))

    client_input = receive_input(connection, max_buffer_size)


    if "--QUIT--" in client_input:
        print("Client is requesting to quit")
        connection.close()
        print("Connection " + ip + ":" + port + " closed")
        is_active = False
    else:
        print("{}".format(client_input))
        connection.sendall("-".encode("utf8"))

    return is_active

def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    # print("Processing the input received from client")

    return str(input_str).upper()

if __name__ == "__main__":
    main()