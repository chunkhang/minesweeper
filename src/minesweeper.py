# minesweeper.py - Minesweeper

from random import randint
from colorama import Fore, Back, Style, init, deinit
from re import compile, match

class Board(object):
	'''
	A minesweeper board loaded with mines and numbers.
	
	Properties:
		height: An integer for the board's height / number of rows
		width: An integer for the board's width / number of columns
		mines: An integer for the number of mines
		matrix: A 2D list to represent the board
		goal: An integer copy for the number of mines
		lastMove: A string for the last successful move made
		alphabets:  A dictionary for conversion between alphabets and numbers
	'''
	
	_alphabets = {	1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 
					11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 
					21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
						
	def __init__(self, height=1, width=2, mines=1):
		self.height = height
		self.width = width
		self.mines = mines
		# Generate matrix
		self._matrix = []
		for row in range(self._height):
			self._matrix.append([])
			for col in range(self._width):
				self._matrix[row].append(Tile())
		# Load with mines
		minesLeft = self._mines
		if minesLeft != 0:
			done = False
		while not done:
			for row in range(self._height):
				for col in range(self._width):
					if self._matrix[row][col].content == -1:
						continue
					if randint(1, 10) == 1:
						self._matrix[row][col].content = -1
						minesLeft -= 1
						if minesLeft == 0:
							done = True
							break
				if done:
					break
		self._goal = self._mines
		# Load with numbers
		for row in range(self._height):
			for col in range(self._width):
				if self._matrix[row][col].content == -1:
					continue
				self._matrix[row][col].content = self._calculateNumber(row, col)
		self._lastMove = 'Started game'
	
	@property
	def height(self):
		return self._height
		
	@height.setter
	def height(self, value):
		if value <= 0:
			value = 1
		self._height = value

	@property
	def width(self):
		return self._width
		
	@width.setter
	def width(self, value):
		# Board must have at least 2 squares
		if value <= 1:
			if self._height == 1:
				value = 2
			else:
				value = 1
		elif value > 50:
			value = 50
		self._width = value
			
	@property
	def mines(self):
		return self._mines
		
	@mines.setter
	def mines(self, value):
		if value < 0:
			value = 1
		elif value >= (self._height * self._width):
			value = (self._height * self._width) - 1
		self._mines = value
	
	def printBoard(self):
		'''Print the minesweeper board according to square status'''
		
		init(autoreset=True)
		
		rows = range(1, self._height + 1)
		columns = range(1, self._width + 1)
		
		print('    ', end='')
		for col in columns:
			print(Style.BRIGHT + Fore.GREEN + str(col).rjust(2), end=' ')
		print()
		for row in rows:
			print('   ' + '+--' * self._width, end='+\n')
			print(Style.BRIGHT + Fore.RED + Board._alphabets[row].rjust(2), end=' ')
			for col in columns:
				status = self._matrix[row - 1][col - 1].status
				content = self._matrix[row - 1][col - 1].content
				highlight = self._matrix[row - 1][col - 1].highlight
				print('|', end='')
				if status == 0:
					print(Back.CYAN + ' ' + ' ', end='')	# Closed tile
				elif status == -1:
					print(Style.BRIGHT + Back.CYAN + Fore.WHITE + ' ' + '#', end='')	# Flag 
				else:
					if content == -1:
						mineString = Style.BRIGHT + Fore.WHITE
						if highlight == 1:
							mineString += Back.GREEN
						elif highlight == -1:
							mineString += Back.RED
						print(mineString + ' ' + '*', end='')	# Mine
					else:	# Open tile / numbers
						numberString = Style.BRIGHT
						if content == 0:
							print(numberString + ' ' + ' ', end='')
							continue
						if content == 1:
							numberString += Fore.YELLOW
						elif content == 2:
							numberString += Fore.MAGENTA
						elif content == 3:
							numberString += Fore.GREEN
						elif content == 4:
							numberString += Fore.RED
						elif content == 5:
							numberString += Fore.CYAN
						elif content == 6:
							numberString = Style.NORMAL + Fore.YELLOW
						elif content == 7:
							numberString = Style.NORMAL + Fore.WHITE
						elif content == 8:
							numberString += Fore.BLACK
						print(numberString + ' ' + str(content), end='')
			print('|')
		print('   ' + '+--' * self._width, end='+\n')
			
		deinit()
			
	def checkMove(self, coordinate):
		'''Return True or False after validating the move'''
		
		alphabetRegex = compile(r'[a-zA-Z]')
		numberRegex = compile(r'[1-9]|[1-9]\d')
		
		n = 0
		if coordinate[0] == '/':
			n = 1
		
		if alphabetRegex.match(coordinate[n]) and numberRegex.match(coordinate[n + 1:]) and coordinate[n + 1:].isdigit():
			row, col = Board._convert(coordinate[n:])
			if row == -1 or row > (self._height - 1) or col > (self._width - 1):
				print('Move is out of range.')
				return False	# Out of range
			else:
				status = self._matrix[row][col].status
				if status == 1:
					print('Tile is already open.')
					return False	# Already open
				else:
					if n == 0:
						if status == -1:
							print('Flagged tile cannot be opened.')
							return False	# Already flagged
						else:
							return True
					else:
						if status == 0:
							if self._mines != 0:
								return True
							else:
								print('Out of flags.')
								return False	# Out of flags
						else:
							return True
		else:
			print('Invalid format.')
			return False	# Wrong format

	def executeMove(self, coordinate):
		'''Return True if move was good, and False if otherwise'''
		
		flag = True
		
		if coordinate[0] == '/':
			row, col = Board._convert(coordinate[1:])
		else:
			row, col = Board._convert(coordinate)
			flag = False
			
		if flag:
			if self._matrix[row][col].status == 0:	# Flag
				self._matrix[row][col].status = -1
				self._mines -= 1
				self._lastMove = 'Flagged ' + coordinate[1:].upper()
			else:
				self._matrix[row][col].status = 0	# Unflag
				self._mines += 1
				self._lastMove = 'Unflagged ' + coordinate[1:].upper()
			return True
		else:
			if self._matrix[row][col].content == -1:	# Open mine
				self._matrix[row][col].status = 1
				print('That was a mine.')
				return False
			else:	# Open adjacent tiles with recursion
				self._openTile(row, col)
				self._lastMove = 'Opened ' + coordinate.upper()
				return True
		
	def getLastMove(self):
		'''Return the last move'''
		
		return self._lastMove
		
	def checkWin(self):
		'''Return True if game has been won, otherwise False'''
		
		count = 0
		for row in range(self._height):
			for col in range(self._width):
				if self._matrix[row][col].status == 0 or self._matrix[row][col].status == -1:
					count += 1
				if count > self._goal:
					return False
		return True
	
	def revealBoard(self):
		'''Reveal location of all mines on the board, and highlight mistakes'''
		
		for i in range(self._height):
			for j in range(self._width):		
				if self._matrix[i][j].content == -1:
					if self._matrix[i][j].status == -1:	# Flagged mine
						self._matrix[i][j].highlight = 1
					else:	# Unflagged mine
						self._matrix[i][j].highlight = -1
					self._matrix[i][j].status = 1
		self.printBoard()

	def _convert(coordinate):
		'''Convert coordinate to row and column integers'''
		
		alphabet = coordinate[0].upper()
		row = -1		
		for key in Board._alphabets:
			if alphabet == Board._alphabets[key]:
				row = key - 1
				break
		col = int(coordinate[1:]) - 1
		return (row, col)
		
	def _openTile(self, row, col):
		'''Open one tile'''
		
		if self._matrix[row][col].status == 1 or self._matrix[row][col].status == -1:
			return	# Stop when tile is already open or flagged
		else:
			self._matrix[row][col].status = 1
			
		if self._matrix[row][col].content != 0:
			return	# Stop when tile has number 1 - 8
		
		if row != 0:	
			self._openTile(row - 1, col)	# Top
			if col != 0:	
				self._openTile(row - 1, col -1)	# Top left
			if col != (self._width - 1):	
				self._openTile(row - 1, col + 1) # Top right
		if row != (self._height - 1):
			self._openTile(row + 1, col)	# Bottom
			if col != 0:	
				self._openTile(row + 1, col -1)	# Bottom left
			if col != (self._width - 1):	
				self._openTile(row + 1, col + 1) # Bottom right			
		if col != 0:
			self._openTile(row, col - 1)	# Left
		if col != (self._width - 1):
			self._openTile(row, col + 1)	# Right
				
	def _calculateNumber(self, row, col):
		'''Return the number of mines adjacent to the coordinate'''
		
		number = 0
		if row != 0:
			if self._matrix[row - 1][col].content == -1:	# Top
				number += 1
			if col != 0:	# Top left
				if self._matrix[row - 1][col - 1].content == -1:
					number += 1
			if col != (self._width - 1):	# Top right
				if self._matrix[row - 1][col + 1].content == -1:
					number += 1
		if row != (self._height - 1):	
			if self._matrix[row + 1][col].content == -1:	# Bottom
				number += 1
			if col != 0:	# Bottom left
				if self._matrix[row + 1][col - 1].content == -1:
					number += 1
			if col != (self._width - 1):	# Bottom right
				if self._matrix[row + 1][col + 1].content == -1:
					number += 1
		if col != 0:		
			if self._matrix[row][col - 1].content == -1:	# Left
				number += 1
		if col != (self._width - 1):	
			if self._matrix[row][col + 1].content == -1:	# Right
				number += 1
		return number	
						
class Tile(object):
	'''
	A tile on a minesweeper board.
	
	Properties:
		content: An integer indicating the content the tile holds
		status: An integer indicating the status of the tile
		highlight: An integer indicating good or bad play
	'''
	
	def __init__(self, content=0, status=0):
		self.content = content
		self.status = status
		self.highlight = 0	# 0: Default, 1: Good, -1: Bad
				
	@property
	def content(self):
		'''-1: Mine, 0 - 8: Number of adjacent mines'''
		
		return self._content
		
	@content.setter
	def content(self, value):	
		if value < -1 or value > 8:
			value = 0
		self._content = value
	
	@ property
	def status(self):
		'''-1: Flagged, 0: Closed, 1: Open'''
		
		return self._status
		
	@status.setter
	def status(self, value):
		if value < -1 or value > 1:
			value = 0
		self._status = value
		

print('                    =======================                    ')	
print('                     M I N E S W E E P E R                     ')
print('                    =======================                    ')
print()
print('Instructions:                                                  ')
print()
print('* Type "A1" to open A1.                                        ')
print('* An open tile which has a number indicates the number of mines')
print('  adjacent to it.')
print('* Type "/A1" to flag A1 if it is unflagged, or unflag A1 if it ')
print('  is already flaged.')
print('* Flagging a tile merely marks it as a reminder that a mine may')
print('  be there.')
print('* The game is lost as soon as a tile with mine is opened.')
print('* The game is won when all the tiles have been opened except a ')
print('  number equivalent to the number of mines remains.')
print('* At the end of the game, the tiles with mines that have been  ')
print('  correctly flagged will be highlighted in green, while those  ')
print('  that incorrectly flagged or unflagged will be highlighted in ')
print('  red.')
print('* Type "restart" to restart the game.')
print('* Type "quit" to quit the game.')
print()

while True:
	quit = False
	restart = False
	
	print('       Mode            Height        Width      Number of Mines')
	print('   ------------       --------     --------     ---------------')
	print('0: Beginner               9            9               10      ')
	print('1: Intermediate          16           16               40      ')
	print('2: Expert                16           30               99      ')
	print('3: Custom             Min:  1      Min:  1      Min:    1      ')
	print('                      Max: 26      Max: 50      Max: H x W - 1 ')

	# Prompt mode
	while True:
		mode = input('\nSelect mode: ')
		if mode not in '0 1 2 3'.split():
			print('Invalid mode.')
		else:
			break
		
	if mode == '0':
		mode = 'Beginner'
		board = Board(9, 9, 10)
	elif mode == '1':
		mode = 'Intermediate'
		board = Board(16, 16, 40)
	elif mode == '2':
		mode = 'Expert'
		board = Board(16, 30, 99)
	else:
		mode = 'Custom'
		height = promptInteger('Enter height: ')
		width = promptInteger('Enter width: ')
		mines = promptInteger('Enter mines: ')
		if mines == 0:
			mines = 1
		board = Board(height, width, mines)

	lost = False
	while True:
		print('\n---' + '---' * board.width, end='----\n\n')
		print('Mode: %s     Mines Left: %d\n' % (mode, board.mines))
		
		# Print board
		board.printBoard()
		
		# Print last move
		print('\nLast Move: ' + board.getLastMove())
		
		# Prompt move
		move = ''
		while True:
			move = input('\n>> ')
			if move.lower() == 'quit':
				quit = True
				break
			if move.lower() == 'restart':
				restart = True
				break
			if board.checkMove(move):
				break
		
		if quit:
			break
		
		if restart:
			break
		
		# Execute move
		if not board.executeMove(move):
			lost = True
			break
		
		# Check winning condition
		if board.checkWin():
			break
	
	if quit:
		break
		
	if restart:
		print()
		continue
	
	# Reveal board
	print()
	board.revealBoard()
			
	if lost:
		print('\nYou lost. Better luck next time.')
	else:
		print('\nCongratulations. You won!')
		
	# Prompt again
	while True:
		again = input('\nPlay again? (Y/N) ').upper()
		if again not in 'Y N'.split():
			print('Invalid response.')
		else:
			break

	if again == 'N':
		break
	
	print()

print()		
print('            =======================================            ')	
print('             Thank you for playing. See you again!             ')
print('            =======================================            ')