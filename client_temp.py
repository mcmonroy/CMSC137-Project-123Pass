# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys
import game

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

def main():


    print("Waiting for all players to connect...\n")
    # data = soc.recv(BUFFER)
    # d_str = str(data, 'utf-8') 
    msg = receive_input()
    # print(msg, msg[0])
    action = msg[0]
    message = ""
    #B-display board
    if action == "B": 
        print("askfnkn")
        d_str = msg[1:].split("|")
        p_id = d_str[0]
        p_hand = d_str[1]
        print(game.get_board(p_id, p_hand))
        message = ask_input("c")
        loop(p_id, message)

        # print(str(data, 'utf-8'))
    elif action == "T":
        print("ssf")
        #do something for tapping 

    
    


    
def loop(p_id, message):
    while message != 'quit':
        msg = ''
        if message != 'f' and message != 't':
            msg = 'p'+p_id+message

        soc.send(bytes(msg, 'utf-8'))
        print("Waiting for other players...")

        # data = soc.recv(BUFFER)
        # print(str(data, 'utf-8'))

        message = ask_input("c")

        # soc.sendall(message.encode("utf8"))
        if soc.recv(BUFFER).decode("utf8") == "-":
            pass        # null operation


    soc.send(b'--quit--')


def receive_input():
    msg = str(soc.recv(BUFFER), 'utf-8')
    return msg

def ask_input(i_type):
    if i_type == "c":
        client_input = input("Enter card to be passed: ")
    send_to_server(client_input)
    return client_input

def send_to_server(message):
    soc.sendall(bytes(message, 'utf-8'))

if __name__ == "__main__":
    main()