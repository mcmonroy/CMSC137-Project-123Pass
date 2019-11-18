import random

def create_player(player_num, hand):
	player = {
		"id" : "P" + str(player_num + 1),
		"hand" : hand,
		"win" : 0
	}

	return player

def generate_deck(player_num):
	rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
	suit = ['H', 'D', 'C', 'S']
	rank_list = []
	card_deck = []

	for i in range(player_num):
		card_rank = random.choice(rank)
		rank_list.append(card_rank)
		rank.remove(card_rank)

	for a in rank_list:
		for b in suit:
			card_deck.append(a + b)

	return card_deck

def generate_hand(deck_list):
	hand = []
	
	for j in range(4):
		rand_card = random.choice(deck_list)
		hand.append(rand_card)
		deck_list.remove(rand_card) 

	return hand

def display_board(players, num):
	print("***************************************")
	for i in range(len(players)):
		print(players[i].get("id") + "\t", end='')
	print("")
	for i in range(len(players)):
		print(str(players[i].get("win")) + "\t", end=''),
	print("")
	print("---------------------------------------")
	print("You are " + players[num].get("id"))
	print("---------------------------------------")
	for i in range(len(players[num].get("hand"))):
		print(players[num].get("hand")[i] + "\t", end=''),
	print("")
	print("***************************************")

def check_id(players_id, code_id):
	if players_id == code_id:
		return True
	else:
		print("The code does not match with your Player ID")
		return False

def check_card(players_card, code_card):
	if code_card in players_card:
		return True
	else:
		print("The code does not match with any of your cards on hand")
		return False

def check_win(player_hand):
	print(player_hand)
	for i in range(len(player_hand) - 1):
		if player_hand[i][0:1] != player_hand[i + 1][0:1]:
			print("Hand incomplete, try again")
			return False
	return True


############################ END OF FUNCTION DEFINITIONS #############################


players = []
win_flag = False
id_flag = False
card_flag = False
turn_tap = []

num_player = int(input("Enter number of players: "))
deck = generate_deck(num_player)

for i in range(num_player):
	card_hand = generate_hand(deck)
	players.append(create_player(i, card_hand))

while True:
	turn_cards = []

	for i in range(num_player):
		while True:
			display_board(players, i)
			code = str(input("Enter code: ")).upper()

			action = code[0:1]
			player_id = "P" + code[1:2]
			play_card = code[2:len(code)]

			# print(action, player_id, play_card)

			id_flag = check_id(players[i].get("id"), player_id)
			if id_flag == False:
				continue

			if action == 'P':
				card_flag = check_card(players[i].get("hand"), play_card)
				if card_flag == False:
					continue
				else:
					players[i].get("hand").remove(play_card)
					turn_cards.append(play_card)
					display_board(players, i)
					break

			elif action == 'F':
				win_flag = check_win(players[i].get("hand"))
				if win_flag == True:
					players[i]["win"] = 1
					break
				else:
					print("Winning conditions still not met")
			elif action == 'T':
				if win_flag == True:
					print("Tap successful")
					turn_tap.append(-i)
					break
				else:
					print("Tap invalid, there is no winner yet")
			else:
				print("Invalid action")

			if win_flag == True and len(turn_tap) == num_player - 1:
				for i in range(num_player):
					if players[i].get("win") == 1:
						continue

					players[i]["win"] = (turn_tap.index(-i) + 1) * -1
					display_board(players, i)
				break

		print(turn_cards)
		print(turn_tap)

	if win_flag == False:
		turn_cards.append(turn_cards.pop(0))
		print(turn_cards)

		for i in range(num_player):
			players[i].get("hand").append(turn_cards[i])
