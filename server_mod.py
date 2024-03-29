#!/usr/bin/env python3
# server-client code reference: https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/
import signal
import socket
import sys
import traceback
from threading import Thread
import game
import atexit

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
                deck = game.generate_deck(max_players) 
                
                #creating threads
                for i in range (len(players)):
                    try:
                        players[i]['hand']=game.generate_hand(deck) #cards per player
                        Thread(target=client_thread, args=(players[i],)).start()
                    except:
                        print("Thread did not start.")
                        traceback.print_exc()                
        except KeyboardInterrupt:
            print("W: interrupt received, stopping…")
            break
        atexit.register(close_socket, soc)                    
    
    soc.close()

def client_thread(player, max_buffer_size=5120):
    global passed_already
    is_active = True
   
    while is_active:
        is_active = start_game(player, max_buffer_size, is_active)
        passed_already = False

    players.clear()

def close_socket(soc):
    soc.close()

# def endgame();


def start_game(player, max_buffer_size, is_active):
    global win_flag
    global passed
    global win
    
    while is_active:

        send_board(player) #1send
        #2rcv
        client_input = process_input(player, receive_input(player.get("conn"), max_buffer_size))

        if "QUIT" in client_input:
            print("Client is requesting to quit")
            player.get("conn").close()
            # del players[int(player.get("id"))-1]
            print("Connection " + str(player.get("address")[0]) + ":" + str(player.get("address")[1]) + " closed")
            is_active = False
        else:
            if 'P' in client_input:
                if win_flag == True:
                        data = "False|Someone already finished, enter 'T' to tap\n"
                        send_data(player, data)
                else:
                    turn_cards.update({ client_input[1] : client_input[2:] })
                    print(turn_cards)

                    player.get("hand").remove(client_input[2:])
                    print(player.get("hand"))

                    data = "True|" + game.get_board(players, int(player.get("id")) - 1)
                    send_data(player, data) #3send

                    while len(turn_cards) < max_players:
                            continue

                    data = ""
                    if len(turn_cards) == max_players:
                        data = "Cont|All players ready, 1-2-3 Pass!\n"
                        send_data(player, data)#4send

                        pass_cards()
                        passed += 1

                    # print("matutulog na ako")
                    print(passed)
                    if passed == max_players: #dahil lahat nagpapass cards, iccclear lang yung list pag lahat nakapagpasa na
                        turn_cards.clear()
                        passed = 0

            elif 'F' in client_input:
                if win_flag == True:
                    data = "False|Someone already finished, enter 'T' to tap\n"
                    send_data(player, data)
                else:
                    win_flag = game.check_win(player.get("hand"))

                    if win_flag == True:
                        data = "True|Congratulations, you win!\n"
                        send_data(player, data)

                        player["win"] = win
                        win += 1

                        while win < (max_players + 1):
                            continue

                        if win == (max_players + 1):
                            data = "Quit|" + game.get_board(players, int(player.get("id")) - 1)
                            send_data(player, data)
                    else:
                        data = "False|Hand incomplete, try again \nWinning conditions still not met\n"
                        send_data(player, data)

            elif 'T' in client_input:
                if win_flag == True:
                    data = "True|Tap successful\n"

                    if win == max_players:
                        data += "\nYou tapped last, you lose\n"
                        
                    send_data(player, data)
                        
                    player["win"] = win
                    win += 1

                    while win < (max_players + 1):
                        continue

                    if win == (max_players + 1):
                        data = "Quit|" + game.get_board(players, int(player.get("id")) - 1)
                        send_data(player, data)

                else:
                    data = "False|Tap invalid, there is no winner yet\n"
                    send_data(player, data)

        data = ""
        # print("cur ergo?")

    print("out of loop")
    return is_active

def send_data(player, data):
    player.get("conn").send(bytes(data, 'utf8'))

def send_board(player):
        data = game.get_board(players, int(player.get("id")) - 1)
        send_data(player, data)

def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line

    return decoded_input

def process_input(player, input_str):
    print("Processing the input received from client...")
    message = ''
    card_flag = False

    client_message = str(input_str).upper()
    print(client_message)

    if client_message == 'F' or client_message == 'T' or client_message == "QUIT":
        return client_message
    elif client_message != 'F' and client_message != 'T' and client_message != "QUIT":
        card_flag = game.check_card(player.get("hand"), client_message)

        if card_flag == True:
            message = "P" + str(player.get("id")) + client_message
        else:
            data = "False|The code does not match with any of your cards on hand"
            send_data(player, data)
    else:
        data = "False|Invalid input!"
        send_data(player, data)

    return message

def pass_cards():
    for player in players:
        print(turn_cards)
        p_id = int(player.get("id"))
        index = str((p_id % max_players) + 1) #id ng pagkukuhaan nung pinasang card sa kanya
        if turn_cards.get(index) in player.get("hand") or turn_cards.get(index) == None:
            continue
        else:
            player.get("hand").append(turn_cards.get(index))
            # print("awawa")
        print(player.get("hand"))

############################ END OF FUNCTION DEFINITIONS #############################

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
passed = 0
win = 1

max_players = int(input("Enter max no. of players: "))

if __name__ == "__main__":
    main()