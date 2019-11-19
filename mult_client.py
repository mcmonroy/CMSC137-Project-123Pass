# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) == 1:
        HOST = '0.0.0.0'
    else:
        HOST = sys.argv[1]

    PORT = 8888
    SERVER = (HOST, PORT)
    BUFFER = 5120

    try:
        soc.connect((SERVER))
    except:
        print("Connection error")
        sys.exit()

    print("Waiting for all players to connect...\n")
    data = soc.recv(BUFFER)
    print(str(data, 'utf-8'))

    print("Enter 'quit' to exit")
    message = input("Enter card to be passed: ")

    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        if soc.recv(BUFFER).decode("utf8") == "-":
            pass        # null operation

        message = input(" -> ")

    soc.send(b'--quit--')

if __name__ == "__main__":
    main()