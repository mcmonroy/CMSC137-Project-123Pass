#!/usr/bin/env python3
# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/
import signal
import socket
import sys
import traceback
from threading import Thread
import game
import atexit


if len(sys.argv) == 1:
    HOST = '0.0.0.0'
else:
    HOST = sys.argv[1]

PORT = 8888         # arbitrary non-privileged port
SERVER = (HOST, PORT)
BUFFER = 5120

players = []
turn_cards = {} # will hold the cards to be passed
win_flag = False
passed_already = False

max_players = int(input("Enter max no. of players: "))

def main():
    start_server()


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind(SERVER)
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(max_players)    # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        try:
            connection, address = soc.accept()
            # print("len:", len(players))
            players.append(game.create_p(len(players) ,[], connection, address))
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)

            if (len(players)==max_players):  #all expected players have connected
                # soc.sendall(bytes("C", 'utf'))
                # send_data(player[i], "C", "")
                    
                deck = game.generate_deck(max_players)
                # print(deck)
              
                #creating threads
                for i in range (len(players)):
                    try:
                        players[i]['hand']=game.generate_hand(deck) #cards per player
                        # print(players[i])
                        Thread(target=client_thread, args=(players[i],)).start()
                    except:
                        print("Thread did not start.")
                        traceback.print_exc()                
        except KeyboardInterrupt:
            print("W: interrupt received, stopping…")
            break
        atexit.register(close_socket, soc)                    
    
    soc.close()

def close_socket(soc):
    soc.close()

def client_thread(player, max_buffer_size=5120):
    global passed_already
    is_active = True
   
    while is_active:
        is_active = start_game(player, max_buffer_size, is_active)
        passed_already = False


def pass_cards():

    for player in players:
        p_id = int(player.get("id"))
        index = str((p_id % max_players) + 1) #id ng pagkukuhaan nung pinasang card sa kanya
        player.get("hand").append(turn_cards.get(index))

def send_data(player, action, data):
    message = action + data
    player.get("conn").send(bytes(message, 'utf8'))

def start_game(player, max_buffer_size, is_active):
    global win_flag
    global passed_already
    in_game = True
    # passing of board to players
    #data = game.get_board(player)
    # send_data(player, "C", "")
   
    send_data(player, "B", player.get("id") + "|" + str(player.get("hand")))

    while in_game:
        client_input = process_input2(receive_input(player.get("conn")))
        if "QUIT" in client_input:
            print("Client is requesting to quit")
            player.get("conn").close()
            print("Connection " + str(player.get("address")[0]) + ":" + str(player.get("address")[1]) + " closed")
            is_active = False
            in_game = False
        else:
            if 'P' in client_input:
                client_input = client_input.split("|")
                turn_cards.update({ client_input[1][0] : client_input[1][1:] })
                
                print(turn_cards)
                player.get("hand").remove(client_input[1][1:])
                print(player.get("hand"))

                if len(turn_cards) == max_players and not passed_already:
                    pass_cards()
                    passed_already = True
                    turn_cards.clear()
                
                    # print("{}".format(client_input))
                if passed_already:
                    send_data(player, "B", player.get("id") + "|" + str(player.get("hand")))
                    # player.get("conn").sendall("-".encode("utf8"))

            elif 'F' in client_input:
                if win_flag == True:
                    data = "Boo"
                    player.get("conn").send(bytes(data, 'utf8'))
                else:
                    win_flag = game.check_win(player.get("hand"))

                    if win_flag == True:
                        data = "Grats"
                        player.get("conn").send(bytes(data, 'utf8'))
                        player["win"] = 1
                        print(player.get("win"))
                    else:
                        data = "Boo"
                        player.get("conn").send(bytes(data, 'utf8'))

                print("{}".format(client_input))
                player.get("conn").sendall("-".encode("utf8"))
            elif 'T' in client_input:
                if win_flag == True:
                    data = "Grats"
                    player.get("conn").send(bytes(data, 'utf8'))
                else:
                    data = "Boo"
                    player.get("conn").send(bytes(data, 'utf8'))

                print("{}".format(client_input))
                d = "-" + "|" + player.get("id") + "|" + str(player.get("hand"))
                player.get("conn").sendall(d.encode("utf8"))

        #---------------------------------------------------------------
    # board_data = "B" + player.get("id") + "|" + str(player.get("hand"))
    # player.get("conn").send(bytes(board_data, 'utf8'))

    # client_input = process_input(player, receive_input(player.get("conn"), max_buffer_size))

    # if "--QUIT--" in client_input:
    #     print("Client is requesting to quit")
    #     player.get("conn").close()
    #     print("Connection " + str(player.get("address")[0]) + ":" + str(player.get("address")[1]) + " closed")
    #     is_active = False
    # else:
    #     if 'P' in client_input:
    #         turn_cards.update({ client_input[1] : client_input[2:] })
            
    #         print(turn_cards)
    #         player.get("hand").remove(client_input[2:])
    #         print(player.get("hand"))

    #         if len(turn_cards) == max_players and not passed_already:
    #             pass_cards()
    #             passed_already = True
    #             turn_cards.clear()
            
    #             print("{}".format(client_input))
    #             player.get("conn").sendall("-".encode("utf8"))

    #     elif 'F' in client_input:
    #         if win_flag == True:
    #             data = "Boo"
    #             player.get("conn").send(bytes(data, 'utf8'))
    #         else:
    #             win_flag = game.check_win(player.get("hand"))

    #             if win_flag == True:
    #                 data = "Grats"
    #                 player.get("conn").send(bytes(data, 'utf8'))
    #                 player["win"] = 1
    #                 print(player.get("win"))
    #             else:
    #                 data = "Boo"
    #                 player.get("conn").send(bytes(data, 'utf8'))

    #         print("{}".format(client_input))
    #         player.get("conn").sendall("-".encode("utf8"))
    #     elif 'T' in client_input:
    #         if win_flag == True:
    #             data = "Grats"
    #             player.get("conn").send(bytes(data, 'utf8'))
    #         else:
    #             data = "Boo"
    #             player.get("conn").send(bytes(data, 'utf8'))

    #         print("{}".format(client_input))
    #         d = "-" + "|" + player.get("id") + "|" + str(player.get("hand"))
    #         player.get("conn").sendall(d.encode("utf8"))

    return is_active

def receive_input(connection):
    client_input = connection.recv(BUFFER)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > BUFFER:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line

    return decoded_input
def process_input2(input_str):
    input_str = input_str.upper()
    return input_str

def process_input(player, input_str):
    # print("Processing the input received from client")
    card_flag = False
    message = ''

    client_message = str(input_str).upper()
    print(client_message)

    if client_message == 'F' or client_message == 'T' or client_message == "--QUIT--":
        return client_message
    elif client_message != 'F' and client_message != 'T' and client_message != "--QUIT--":
        card_flag = game.check_card(player.get("hand"), client_message)

        if card_flag == True:
            message = "P" + str(player.get("id")) + client_message
        else:
            data = "The code does not match with any of your cards on hand"
            player.get("conn").send(bytes(data, 'utf8'))
    else:
        data = "Invalid input!"
        player.get("conn").send(bytes(data, 'utf8'))

    return message

if __name__ == "__main__":
    main()