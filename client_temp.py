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

menu = True

while menu:
    print("***************************************")
    print("\t1-2-3-Pass!")
    print("***************************************")
    print("\t[1] How to play\n\t[2] Play Game\n\t[3] Quit")
    
    choice = int(input("Choice: "))

    if choice == 2:
        menu = False
    elif choice == 3:
        print("Bye!")
        exit()
    elif choice == 1:
        print("***************************************")
        print("\tHOW TO PLAY")
        print("***************************************")
        print("* Enter the card you wish to pass. If *")
        print("* you have already completed a set of *")
        print("* the same number and of the four sui-*")
        print("* ts, enter 'F' to signify your fini- *")
        print("* sh. If another player finishes first*")
        print("* enter 'T' to tap. The first to fini-*")
        print("* sh is the winner and the last to tap*")
        print("* loses.                              *")
        print("***************************************")


try:
    soc.connect((SERVER))
except:
    print("Connection error")
    sys.exit()

def main():

    print("Waiting for all players to connect...\n")
    msg = receive_input()
    
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
        
    elif action == "T":
        print("ssf")
        #do something for tapping 

    
def loop(p_id, message):
    while message != 'quit':
        send_to_server(message)
        print(receive_input())
        print("Waiting for other players...")

        # data = soc.recv(BUFFER)
        # print(str(data, 'utf-8'))
        # while (soc.recv())

        # if soc.recv(BUFFER).decode("utf8") == "-":
        #     pass        # null operation

        msg = receive_input()

        d_str = msg[1:].split("|")
        p_id = d_str[0]
        p_hand = d_str[1]
        print(game.get_board(p_id, p_hand))
        message = ask_input("c")

        # soc.sendall(message.encode("utf8"))
       


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