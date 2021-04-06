# Hackbright Academy Prep Course - Final Project
# Assignment: create a terminal-based game.

# Game title: Spaceship Obstacle Course
# Goal: navigate the obstacle course to hit the target! 


# --- MVP PSEUDOCODE --- #
#
# 1. Create obstacle course
#    - store in a 2D list of lists 
#      - this data structure allows easy mapping of locations and is easy to change the value at each location to store path information
#      - name main list 'space_map'
#      - each sublist will represent one line on the terminal
#    - print space_map to screen
#    - print directions to screen 
#      - 'direct your spaceship (>) to the target (X)'
#      - 'use the 'wasd' keys to choose your path'
#
# 2. Place blinking 'spaceship' @ start & target @ end
#    - add these entries into the space_map by defining space_map[y][x]
#    - blink a few times by alternating space_map w/ blank_space_map 
#    - adjust frequency of blinks using time package
#
# 3. Get user input
#    - use either 'wasd' or arrow keys
#    - log user keystrokes for path
#    - user hits enter to start the spaceship moving
#
# 4. Translate keystrokes into directions
#    - create path... split up string of user input into individual keystrokes
#    - for each keystroke:
#      - read keystroke, move accordingly
#        - change the indices (y,x) of the lists to get to a new position in space_map
#      - check path validity:
#        - if path hits obstacle OR edge
#            -> 'crash! try again?' ... user input to restart or not
#        - if it makes it through but misses target
#            -> 'lost in space! try again?' ... "  "
#        - if it hits the target
#            -> 'you made it!'
#        - otherwise, continue...
#      - enter ship location in space_map
#    - print path onscreen (all at once)


# --- NTH... Improvements After MVP --- #
#    - randomize starting location & target location (vertically) - DONE
#    - animate path dot by dot - DONE
#    - crash animation
#    - winning animation
#    - multiple levels
#    - auto-generation of levels? 
#    	- add random planets in new_map that do not overlap with the path in empty_map
# 		- have several standard planets & place by line
#		- OR randomly generated space junk - DONE
#	- color! - DONE
# 	- emoji ship and target - DONE



# mini space_map to conceptualize data structure:
#
# [	[0-0, 0-1, 0-2],
# 	[1-0, 1-1, 1-2],
# 	[2-0, 2-1, 2-2],
# 	[3-0, 3-1, 3-2]  ]
#
# coordinates: space_map[y][x]






# --- ACTUAL CODE --- #

# import packages:
import copy
import emoji	# for ship and target
import os
import random
import time
from colorama import init, Fore, Back, Style	# color options for terminal text
init(autoreset=True)


# set up space_map: 
# 	dimensions:
#     	0 < y < 11 (indices 0 & 11 are borders)
#     	0 < x < 51 (indices 0 & 51 are borders)
# 	coordinates: space_map[y][x]

space_map_planets = [
	['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+'],
	['|','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+',' ',' ',' ',' ','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+',' ',' ',' ',' ','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+','+','+',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','+','+','+','+','+',' ',' ',' ','|'],
	['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+']
	]

empty_map = [
	['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
	['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+']
	]

INSTRUCTIONS = f'SPACESHIP OBSTACLE COURSE \n\n  - Direct your spaceship to the target. \n  - Use the \'wasd\' keys to plan your path, then hit enter. \n  - Don\'t hit the space junk! \n'


def play_game(space_map, y_0, y_X, mode, cheat_code):
	""" play the game! """

	# get game going and prompt user for input:
	initialize_game(space_map, y_0, y_X)

	# take in the user input and check that it is valid
	user_keystrokes = user_defined_path(space_map, y_0, mode, cheat_code)

	# translate the user input into the ship's path
	#	at each step: check that the ship is not crashing or off the screen
	translate_path(space_map, user_keystrokes, y_0)


def loading(num_seconds):
	""" create a loading animation """
	print('loading', end = '')
	for i in range(int(num_seconds*2)):
		print('.', end = '')
		time.sleep(0.2)
	print()


def initialize_game(space_map, y_0=7, y_X=5):
	""" set up game on screen """ 

	space_map_blank = copy.deepcopy(space_map)
	space_map_blank[y_0][1] = ' '

	# highlight ship location by blinking maps 
	for i in range(3):  
		time.sleep(.4)
		os.system('clear')
		print_map(space_map_blank)
		time.sleep(.4)
		os.system('clear')
		print_map(space_map)


def print_map(space_map):
	""" print space map to the terminal with instructions """

	print(Fore.CYAN + Style.BRIGHT + INSTRUCTIONS)
	for space_map_line in space_map:
		print(''.join(space_map_line))


def user_defined_path(space_map, y, mode, cheat_code):
	""" get user input & check its validity """

	while True:
		# get user input 
		print(Fore.CYAN + Style.BRIGHT + 'Choose your path!')
		user_keystrokes = input('> ')

		error = None
		if user_keystrokes == 'cheat': # check if user entered cheat code
			if mode == 'a':
				return 'd'*2 + 's'*(11-y) + 'd'*3 + 'w'*7 + 'd'*13 + 's'*2 + 'd'*4 + 's'*5 + 'd'*10 + 'w'*4 + 'a'*5 + 's'*2 + 'd'*10 + 'w'* 5 + 'd'*5 + 'w'*3 + 'd'*7 + 's'*11
			else:
				return cheat_code

		else:
			for letter in user_keystrokes: # check that user's input is valid
				if letter not in 'wasd':
					error = 'Error: you entered invalid keystrokes. Use only the wasd keys.'
			if error:
				print(Fore.RED + error)
			else:	
				return user_keystrokes


def check_direction(x_step = 0, y_step = 0):
	""" take in a change in index and translate to wasd direction """

	if x_step == 1:
		direction = 'd'
	elif x_step == -1:
		direction = 'a'
	elif y_step == 1:
		direction = 's'
	elif y_step == -1:
		direction = 'w'
	else:
		direction = ''
	return direction


def translate_path(space_map, user_keystrokes, y):
	""" translate user keystrokes into path; check validity of path """

	x = 1
	win = False
	adrift = True
	space_map_with_path = copy.deepcopy(space_map)

	# figure out next step based on keystroke
	for letter in user_keystrokes:
		if letter == 'w': # up
			y -= 1
		elif letter == 'a': # left
			x -= 1
		elif letter == 's': # down
			y += 1
		elif letter == 'd': # right
			x += 1

		# check validity of next step
		if space_map[y][x] == '-' or space_map[y][x] == '|': # off edge
			adrift = False
			print(Fore.RED + Style.BRIGHT + '\nYou are lost in space... \n')
			break
		elif space_map[y][x] == '+': # crash
			adrift = False
			print(Fore.RED + Style.BRIGHT + '\nOh no! You crashed! \n')
			break
		elif space_map[y][x] == bullseye: # hit target!
			win = True
			reload = False
			adrift = False
			print(Fore.GREEN + '\nNice job - you win! \n')
			break
		else: # place path marker and print to screen
			space_map_with_path[y][x] = '.'
			time.sleep(.05)
			os.system('clear')
			print_map(space_map_with_path)
			print(Fore.CYAN + Style.BRIGHT + f'You chose the path {user_keystrokes}.')

	if adrift == True: # didn't hit anything & didn't make it
		print(Fore.RED + Style.BRIGHT + '\nYou are adrift in space... \n')
		

def create_map(emptiest_map, ship, bullseye):
	''' create a randomized new obstacle map using a random walk free path '''
	
	empty_map = copy.deepcopy(emptiest_map)

	y_X = random.randint(1,11) # y position of target
	empty_map[y_X][50] = bullseye # place target in map
	empty_map[y_X][51] = ''

	x = 1 # initial x position of ship
	y = random.randint(1,11) # initial y position of ship
	empty_map[y][x] = ship # place ship in map
	y_0 = y
	
	new_map = copy.deepcopy(empty_map)
	
	# choose a random walk path from ship to target
	#	this ensures there is definitely a way through!
	#	store this path in empty_map since that will not be returned
	cheat_code = ''
	hit_target = False
	
	while hit_target == False:
		# choose a random next step (restricted to up, down, or right)
		x_step = 0
		y_step = 0

		if x != 50:
			x_step = random.choice([0, 1])
		if x_step == 0: 
			y_step = random.choice([1, -1])
		
		if new_map[y + y_step][x + x_step] == bullseye:
			# target reached!
			direction = check_direction(x_step, y_step) 
			cheat_code += direction # save path keystrokes to cheat code
			hit_target = True

		elif empty_map[y + y_step][x + x_step] == ' ': 
			# take next step
			x += x_step
			y += y_step
			empty_map[y][x] = '.' # place temporary path markers in empty_map
			direction = check_direction(x_step, y_step)	
			cheat_code += direction # save keystroke to cheat code

		elif x == 50 and new_map[y + y_step][x] == '-': # (note x_step = 0)
			# skip down or up to the target and call it good!
			# print(Fore.RED + Style.BRIGHT + 'stuck in corner') ###
			y_step = -y_step
			while True:
				y += y_step
				if new_map[y + y_step][x] == bullseye:
					direction = check_direction(0, y_step)
					cheat_code += direction + direction # add keystroke to cheat code
					target = True
					break
				else: 
					empty_map[y + y_step][x] = '.' # place temp path markers in empty_map
					direction = check_direction(0, y_step)
					cheat_code += direction # add keystroke to cheat code

	# place randomized obstacles
	for y, line in enumerate(new_map):
		for x, spot in enumerate(line):
			if empty_map[y][x] == ' ' and x < 50:
				new_map[y][x] = random.choice([' ',' ',' ',' ',' ',' ',' ',' ',' ','+'])

	return new_map, y_0, y_X, cheat_code



## --- play the game, with two mode options! --- ##

ship = emoji.emojize(':rocket:')
bullseye = emoji.emojize(':bullseye:')
reload = True
print(Fore.CYAN + Style.BRIGHT + 'Welcome to SPACESHIP OBSTACLE COURSE! \n')

while reload == True:
	print(Fore.CYAN + Style.BRIGHT + 'Choose your play mode: \n    (a) Planet Mode (single level map of planets) \n    (b) Random Mode (auto-generated maps)')
	mode = input('> ')

	if mode == 'a': # play in planet mode
		loading(2)
		space_map = copy.deepcopy(space_map_planets)
		y_0 = random.randint(4,11) # initial y position of ship
		space_map[y_0][1] = ship
		y_X = random.randint(4,11) # y position of target
		space_map[y_X][50] = bullseye
		space_map[y_X][51] = ''
		cheat_code = ''
		play_game(space_map, y_0, y_X, mode, cheat_code)

	elif mode == 'b': # play in random mode
		loading(2)
		space_map, y_0, y_X, cheat_code = create_map(empty_map, ship, bullseye)

		while True:
			play_game(space_map, y_0, y_X, mode, cheat_code)
			# give user the chance to play the same map again:
			print(Fore.CYAN + Style.BRIGHT + 'Would you like to try this map again? (y/n)')
			try_again = input('> ')
			if try_again == 'n':
				print(Fore.CYAN + Style.BRIGHT + 'Okay, this map will disappear forever now', end = '')
				for i in range(3):
					print(Fore.CYAN + Style.BRIGHT + '.', end = '')
					time.sleep(0.3)
				print()
				break
			elif try_again == 'y':
				pass
			else: 
				print(Fore.RED + Style.BRIGHT + 'Error: invalid entry.\n')

	else: 
		print(Fore.RED + Style.BRIGHT + 'Error: invalid entry.\n')
	
	# ask if user wants to restart the game from main menu
	while True:
		print(Fore.CYAN + Style.BRIGHT + '\nWould you like to restart SPACESHIP OBSTACLE COURSE? (y/n)')
		restart = input('> ')
		if restart == 'y':
			reload = True
			os.system('clear')
			break
		elif restart == 'n':
			reload = False
			print(Fore.CYAN + Style.BRIGHT + '\nOkay, goodbye.')
			break
		else:
			print(Fore.RED + Style.BRIGHT + 'Error: invalid entry.\n')

