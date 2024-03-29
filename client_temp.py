    # server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/

import socket
import sys
import game

def show_menu():
    print("***************************************")
    print("\t1-2-3-Pass!")
    print("***************************************")
    print("\t[1] How to play\n\t[2] Play Game\n\t[3] Quit")
    
    choice = int(input("Choice: "))

    if choice == 2:
        return False
    elif choice == 3:
        print("Bye!")
        exit()
    elif choice == 1:
        how_to_play()
        return True
    else:
        print("Invalid choice!")
        return True

def how_to_play():
    print("***************************************")
    print("\tHOW TO PLAY")
    print("***************************************")
    print("* Enter the card you wish to pass. If *")
    print("* you have already completed a set of *")
    print("* the same rank and of the four suits,*")
    print("* enter 'F' to indicate your finish.  *")
    print("* If another player finishes first,   *")
    print("* enter 'T' to tap. The first player  *")
    print("* to finish is the winner and the last*")
    print("* player to tap loses.                *")
    print("***************************************")

def receive_input():
    msg = str(soc.recv(BUFFER), 'utf-8')
    return msg

def ask_input():
    client_input = str(input("Enter card to be passed: "))
    send_to_server(client_input)
    return client_input

def send_to_server(message):
    soc.sendall(bytes(message, 'utf-8'))

def start_game():
    in_game = True
    message = ""
    validate = ""
    validate_quit = ""

    while in_game:
        # print("jet ammo")
        msg = receive_input() #prints board for every turn
        #1rcv
        print(msg)

        while True: #loop asking for input until client gives the correct input
            message = ask_input().upper() #2send
            print("Passed " + message + "\n")

            if message == "QUIT":
                print("Bye!")
                exit()
            else:
                msg = receive_input() #3rcv
                # print("beep boop")
                print(msg)
                validate = msg.split("|")
                print(validate[1]) #message to be displayed
                # print("owh baket?")

                # if ("Congratulations" in validate[1]) or ("successful" in validate[1]) or ("you lose" in validate[1]):
                #     in_game = False

                if "True" in validate[0]: # gets out of loop if true is in received input
                    break

                msg = receive_input() #prints board if input is invalid
                print(msg)
                

        print("Waiting for other players...")
        # print("pabalik-balik?")

        # if "Someone already finished, enter 'T' to tap" in validate[1]:
        #     message = ask_input().upper()

        message = receive_input()#4rcv
        print(message)
        validate_quit = message.split("|")
        print(validate_quit[1])

        if "Quit" in validate_quit[0]:
            print("Game finished, quitting game... Bye!")
            send_to_server("QUIT")
            exit()
        # print("talaga?")

    # print("client out of while loop")
    soc.send(b'quit')

def main():
    print("Waiting for all players to connect...\n")
    start_game()



soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 1:
    print("Proper usage: python/python3 mult_client.py <ip_address_of_server>")
    print("Type 'ifconfig' in the terminal of the server to know its ip address.")
    exit()
else:
    HOST = sys.argv[1]

#-------- printing of menu ----------
menu = True
while menu:
    menu = show_menu()

#-------- start of socket connection -------
PORT = 8888
SERVER = (HOST, PORT)
BUFFER = 5120

try:
    soc.connect((SERVER))
except:
    print("Connection error")
    sys.exit()


if __name__ == "__main__":
    main()