# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys
import game

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) == 1:
        print("Proper usage: python/python3 mult_client.py <ip_address_of_server>")
        print("Type 'ifconfig' in the terminal of the server to know its ip address.")
        exit()
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
    d_str = str(data, 'utf-8') 
    d_str = d_str.split("|")
    
    p_id = d_str[0]
    p_hand = d_str[1]
    print(game.get_board(p_id, p_hand))
    # print(str(data, 'utf-8'))

    print("Enter 'quit' to exit")
    message = input("Enter card to be passed: ")

    # message = get_data() return input

    while message != 'quit':
        soc.send(bytes(message, 'utf-8'))
        print("Waiting for other players...")

        data = soc.recv(BUFFER)
        print(str(data, 'utf-8'))

        print("Enter 'quit' to exit")
        message = input("Enter card to be passed: ")


        # soc.sendall(message.encode("utf8"))
        if soc.recv(BUFFER).decode("utf8") == "-":
            pass        # null operation

    soc.send(b'--quit--')

if __name__ == "__main__":
    main()