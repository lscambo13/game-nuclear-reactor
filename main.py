import os
import random
import logging
from enum import Enum
 
# LOGGING
logging.basicConfig(filename="log.log",
					format='[%(levelname)s] %(asctime)s - %(message)s',
					filemode='+a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.info("booting the console...")


# CONFIG
SECRET_CODE = random.randint(1,100)
CONSOLE_WIDTH = 80
GAME_TITLE = "N U C L E A R  R E A C T O R  C O N S O L E"
MSG_EXIT = "E X I T I N G"
MSG_SUCCESS = "Success!"
MSG_FAIL = "Incorrect!"
MSG_LOCKDOWN = "Intruder suspected!\nSystem entering lockdown mode!"
MSG_CHOOSE_LEVEL = "Which tower do you wish to access? (Select between 1-10)"
selected_level:int = -1


class Color(Enum):
	BLACK = "0"
	BLUE = "1"
	GREEN = "2"
	AQUA = "3"
	RED = "4"
	PURPLE = "5"
	YELLOW = "6"
	WHITE = "7"
	GRAY = "8"
	LIGHT_BLUE = "9"
	LIGHT_GREEN = "A"
	LIGHT_AQUA = "B"
	LIGHT_RED = "C"
	LIGHT_PURPLE = "D"
	LIGHT_YELLOW = "E"
	BRIGHT_WHITE = "F"

class DifficultyLevel(Enum):
	Easiest = 10
	Easier = 9
	Easy = 8
	Normal = 7
	Medium = 6
	Hard = 5
	Harder = 4
	Hardest = 3
	Lucky = 2
	Impossible = 1
	Unknown = -1

# UTILS
def clear_console():
	os.system("cls")

def read_high_score():
	file_permission = "r"
	if not os.path.isfile("high_score"):
		logger.debug(f"High score file missing")
		file_permission = "+a"
	with open("high_score", file_permission) as file:
		if not os.path.isfile("high_score"):
			print("Not enough read or write permissions!")
			exit()
		high_score = file.readline()
		logger.debug(f"Past high score: {high_score}")
		if not high_score: return 0
		return int(high_score)
	
score = read_high_score()
# logger.debug(f"Past high score: {score}")
score = "0000" if not score else score
if score:
	zeroes = (4 - len(str(score))) * "0"
	score = f"{zeroes}{str(score)}"
logger.debug(f"Past high score: {score}")

def calculate_new_score(lives:int):
	max_score = 1000 // selected_level
	score = (max_score // selected_level) * lives
	return score


def color_console(bg:Color=Color.BLACK, fg:Color=Color.BRIGHT_WHITE):
	# color = f"color {bg.value}{fg.value}"
	# logger.debug(f"color {bg.value}{fg.value}")
	os.system(f"color {bg.value}{fg.value}")

def center_text(text:str, separator:str=" "):
	space_around = (CONSOLE_WIDTH - len(text)) // 2
	if space_around <= 0: 
		return text
	padding_text = (space_around//len(separator)) * separator
	return f"{padding_text} {text} {padding_text}"

def choose_difficulty():
	try:
		input_level = int(input(center_text(MSG_CHOOSE_LEVEL)))
		if input_level>10 or input_level<1:
			raise NotImplementedError
		return input_level
	except Exception as err:
		logger.error(f"Level select: {err}")
		return -1

# CORE
def main_menu():
	# score = HIGH_SCORE
	# score = "0000" if not score else score
	# if score:
	# 	zeroes = (4 - len(str(score))) * "0"
	# 	score = f"{zeroes}{str(score)}"
	print("\n")
	print(center_text(f"Security Level: {DifficultyLevel(selected_level).name} {' ' * 32} High Score: {score}"))
	logger.debug(SECRET_CODE)
	# print(SECRET_CODE)
	print("\n")
	print(center_text(GAME_TITLE, " - "))
	print("\n")
	return

def exit_game(fail:bool=False):
	logger.debug('Exiting')
	if fail is True:
		color_console(Color.LIGHT_RED, Color.BLACK)
		print(MSG_LOCKDOWN)
	print("\n")
	print(center_text(MSG_EXIT, "-  "))
	print("\n")
	input("...")
	color_console()

def prompt_nuclear_code_input():
	try:
		input_code = int(input(f"{' ' * 4}Password: "))
		return input_code
	except Exception as err:
		logger.error(f"User input: {err}")
		return None


def log_in(lives:int=7):
	is_successful = False
	logger.debug(f"Difficulty: {selected_level}")
	hint = "1-100"
	while lives > 0:
		clear_console()
		main_menu()
		color_console(Color.BLACK, Color.LIGHT_RED)
		lives = lives - 1
		print(f"{' ' * 4}Attempts remaining: {lives}\t\t\t\t\tDebug: {hint}\n")
		input_code = prompt_nuclear_code_input()
		if input_code is None:
			exit_game(True)
			break
		elif input_code == SECRET_CODE:
			is_successful = True
			new_score = calculate_new_score(lives+1)
			print(center_text(MSG_SUCCESS))
			print("\n")
			print(f"\n{center_text(f'You scored {new_score} points!')}\n")
			if new_score > int(score):
				print(center_text(f"Congratulations! You have set a new high score."))
				with open("high_score", "w") as file:
					file.write(f"{new_score}")
			color_console(Color.BLACK, Color.LIGHT_GREEN)
			exit_game()
			break
		elif input_code > SECRET_CODE:
			hint = "Too High"
		elif input_code < SECRET_CODE:
			hint = "Too Low"
	if not lives:
		if is_successful is False:
			exit_game(True)

# ENTRY POINT
while selected_level < 0:
	clear_console()
	main_menu()
	selected_level = choose_difficulty()
log_in(selected_level)
