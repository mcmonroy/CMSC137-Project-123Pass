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

    max_players = int(input("Enter max no. of players: "))

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(max_players)    # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        print("len:", len(players))
        players.append(game.create_p(len(players) ,[], connection, address))
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        if (len(players)==max_players):
            deck = game.generate_deck(max_players)
            print(deck)
            for i in range (len(players)):
                try:
                    players[i]['hand']=game.generate_hand(deck)
                    print(players[i])
                    Thread(target=client_thread, args=(players[i],)).start()
                except:
                    print("Thread did not start.")
                    traceback.print_exc()                

    soc.close()


def client_thread(player, max_buffer_size=5120):
    is_active = True
   
    while is_active:
        is_active = start_game(player, max_buffer_size, is_active)

# '''
# def client_thread(connection, ip, port, players, max_buffer_size = 5120):
#     is_active = True

#     while is_active:
#         if (len(players)==2):
#             is_active = start_game(connection, players, ip, port, max_buffer_size, is_active)

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

'''
def start_game(player, max_buffer_size, is_active):
    generate board for this player 
    data = board
    player.get("connection").send(bytes(data, 'utf8'))
'''
# def start_game(connection, players, ip, port, max_buffer_size, is_active):

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

#     return is_active

def start_game(player, max_buffer_size, is_active):
    
    # passing of board to players
    data = game.get_board(player)
    player.get("conn").send(bytes(data, 'utf8'))

    client_input = receive_input(player.get("conn"), max_buffer_size)


    if "--QUIT--" in client_input:
        print("Client is requesting to quit")
        player.get("conn").close()
        print("Connection " + str(player.get("address")[0]) + ":" + str(player.get("address")[1]) + " closed")
        is_active = False
    else:
        print("{}".format(client_input))
        player.get("conn").sendall("-".encode("utf8"))

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