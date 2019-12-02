#!/usr/bin/env python3
# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys
import os
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

def main():
    choice = game_menu()
    while choice != 3:
        if choice == 1:
            print("Lam mo na yon")
        elif choice == 2:
            connect()
            start_game()
        elif choice == 3:
            print("Bye!")
            exit()

        choice = game_menu()


def game_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("***************************************")
    print("\t1-2-3-Pass!")
    print("***************************************")
    print("\t[1] How to play\n\t[2] Play Game\n\t[3] Quit")
    
    choice = int(input("Choice: "))
    return choice


def connect():
    try:
        soc.connect((SERVER))
    except:
        print("Connection error")
        sys.exit()


def start_game():
    in_game = True
    # not_ready = True     
    # msg =''
    print("Waiting for all players to connect...\n")
    # while not_ready:
    #     msg = receive_input()
    #     # print(msg)
    #     if msg == "C": #complete players
    #         not_ready = False
    
    while in_game:
        message = receive_input()
        print(message)
        action = message[0]
        print(action)
        # message = ""
    
        if action == "E":
            print(message[1:])
            client_input = ask_input("Enter card to be passed: ")
            if client_input == 'F' or client_input == 'T':
                send_to_server(client_input, p_id)
            else:
                send_to_server("P", p_id + client_input)
            
        #B-display board
        elif action == "B": 
            os.system('cls' if os.name == 'nt' else 'clear')
    
            print("askfnkn")
            d_str = message[1:].split("|")
            p_id = d_str[0]
            p_hand = d_str[1]
            print(game.get_board(p_id, p_hand))

            client_input = ask_input("Enter card to be passed: ")
            if client_input == 'F' or client_input == 'T':
                send_to_server(client_input, p_id)
            else:
                send_to_server("P", p_id + client_input)
                
            # loop(p_id, message)
            print("Waiting for other players...")
 
            
        elif action == "T":
            print("ssf")
        else:
            print(message)
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
        # while (soc.recv())

        d = soc.recv(BUFFER).decode("utf8")
        d = d.split("|")
        if d[0] == "-":
            pass        # null operation
   
        # print(game.get_board(d[1], d[2]))
        message = ask_input("c")
       

        # soc.sendall(message.encode("utf8"))
       


    soc.send(b'--quit--')


def receive_input():
    msg = str(soc.recv(BUFFER), 'utf-8')
    return msg

def ask_input(input_msg):
    client_input = input(input_msg)
    return client_input

def send_to_server(action, message):
    soc.sendall(bytes(action + "|" + message, 'utf-8'))

if __name__ == "__main__":
    main()
