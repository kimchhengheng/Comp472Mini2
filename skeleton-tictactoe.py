# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
# import numpy as np
Alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	def __init__(self,board,boardSize,winlineup, d1,d2,time,numBlocs, recommend = True):
		self.initBoard = board
		self.boardSize = boardSize
		self.xwin = ','.join([str(elem) for elem in ['X' for x in range(winlineup)]]) 
		self.owin = ','.join([str(elem) for elem in ['O' for x in range(winlineup)]]) 
		self.player1d1 = d1
		self.player2d2 = d2
		self.maxtime = time
		self.winLineUp = winlineup
		# self.count =0
		self.dict = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
		self.dictall = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
		self.depthdict= {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
		self.depthdictall = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
		# self.arddict = None
		self.initialize_game()
		self.recommend = recommend
		self.file_name ="./gameTrace-"+str(self.boardSize)+str(numBlocs)+str(winlineup)+str(time)+ ".txt" 
		self.move = []
		self.evaluation = []
	def writeToFile(self, mode, text):
		with open(self.file_name, mode) as textfile: 
			textfile.writelines(text)
	def initialize_game(self):
		self.current_state = self.initBoard
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		text ="\n"
		print()
		if len(self.move) > 0:
			print("  "+self.Alphabet[0:self.boardSize]+'\t\t(move'+str(len(self.move))+')')
			text +="  "+self.Alphabet[0:self.boardSize]+'\t\t(move'+str(len(self.move))+')'+'\n'
		else:
			print("  "+self.Alphabet[0:self.boardSize])
			text +="  "+self.Alphabet[0:self.boardSize]+'\n'
		print(" +"+str('-'* self.boardSize))
		text +=" +"+str('-'* self.boardSize)+'\n'
		for y in range(0, self.boardSize):
			for x in range(0, self.boardSize):
				if x== 0:
					print(F'{y}|{self.current_state[x][y]}', end="")
					text +=str(y)+"|"+str(self.current_state[x][y])
				else:
					print(F'{self.current_state[x][y]}', end="")
					text +=str(self.current_state[x][y])
			print()
			text +="\n"
		print()
		text +="\n"
		self.writeToFile('a', text)

	# input check the range
	def is_valid(self, px, py):
		# print('is valid')
		if px < 0 or px > self.boardSize-1 or py < 0 or py > self.boardSize-1:
			return False
		elif self.current_state[px][py] != '.':
			# != . include X O and * bloc
			return False
		else :
			return True

	def is_end(self):
		# print('is end')
		# Vertical win
		for col in range(0, self.boardSize): 
			column = ','.join([str(elem) for elem in [row[col] for row in self.current_state]])
			if self.player_turn == 'X' and self.xwin in column:
				return 'X'  
			elif self.player_turn == 'O' and self.owin in column:
				return 'O'

		# # Horizontal win
		for row in range(0, self.boardSize):
			row = ','.join([str(elem) for elem in self.current_state[row]])
			if self.player_turn == 'X' and self.xwin in row:
				return 'X'  
			elif self.player_turn == 'O' and self.owin in row:
				return 'O'

		# # Main diagonal win

		allDiagonal= [[self.current_state[d-i][i] for i in range(self.boardSize) if 0<=d-i<self.boardSize] for d in range(2*self.boardSize-1)]
		for dia in allDiagonal:
			if len(dia) >= self.winLineUp:
				dia = ','.join([str(elem) for elem in dia])
				if self.player_turn == 'X' and self.xwin in dia:
					return 'X'  
				elif self.player_turn == 'O' and self.owin in dia:
					return 'O'

		otherDiagonal= [[self.current_state[y-self.boardSize+x][x] for x in range(self.boardSize) if 0<=(y-self.boardSize+x)<self.boardSize] for y in range(2*self.boardSize-1)]
		for dial in otherDiagonal:
			if len(dial) >= self.winLineUp:
				dial = ','.join([str(elem) for elem in dial])
				if self.player_turn == 'X' and self.xwin in dial:
					return 'X'  
				elif self.player_turn == 'O' and self.owin in dial:
					return 'O'

		# # Is whole board full?
		for i in range(0, self.boardSize):
			for j in range(0, self.boardSize):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# # It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def evaluatedFunction(self):
		for col in range(0, self.boardSize): 
			column = [row[col] for row in self.current_state]
			if self.player_turn == 'X' and 'X' in column:
				ind = column.index('X')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = column[ind:self.boardSize]
					if 'O' not in subList and '*' not in subList:
						return -1
					else: 
						return 1
			elif self.player_turn == 'O' and 'O' in column:
				ind = column.index('O')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = column[ind:self.boardSize]
					if 'X' not in subList and '*' not in subList:
						return 1
					else: 
						return -1

		# # Horizontal win
		for row in range(0, self.boardSize):
			rowList  = self.current_state[row]
			if self.player_turn == 'X' and 'X' in rowList:
				ind = rowList.index('X')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = rowList[ind:self.boardSize]
					if 'O' not in subList and '*' not in subList:
						return -1
					else: 
						return 1
			elif self.player_turn == 'O' and 'O' in rowList:
				ind = rowList.index('O')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = rowList[ind:self.boardSize]
					if 'X' not in subList and '*' not in subList:
						return 1
					else: 
						return -1

		# # Main diagonal win

		allDiagonal= [[self.current_state[d-i][i] for i in range(self.boardSize) if 0<=d-i<self.boardSize] for d in range(2*self.boardSize-1)]
		allDiagonal = [ el for el in allDiagonal if len(el)>=self.boardSize]
		for dia in allDiagonal:
			if self.player_turn == 'X' and 'X' in dia:
				ind = dia.index('X')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = dia[ind:self.boardSize]
					if 'O' not in subList and '*' not in subList:
						return -1
					else: 
						return 1
			elif self.player_turn == 'O' and 'O' in dia:
				ind = dia.index('O')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = dia[ind:self.boardSize]
					if 'X' not in subList and '*' not in subList:
						return 1
					else: 
						return -1

		otherDiagonal= [[self.current_state[y-self.boardSize+x][x] for x in range(self.boardSize) if 0<=(y-self.boardSize+x)<self.boardSize] for y in range(2*self.boardSize-1)]
		otherDiagonal = [ el for el in otherDiagonal if len(el)>=self.boardSize]
		for dial in otherDiagonal:
			if self.player_turn == 'X' and 'X' in dial:
				ind = dial.index('X')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = dial[ind:self.boardSize]
					if 'O' not in subList and '*' not in subList:
						return -1
					else: 
						return 1
			elif self.player_turn == 'O' and 'O' in dial:
				ind = dial.index('O')
				if (ind + self.boardSize) <= (self.boardSize-1):
					subList = dial[ind:self.boardSize]
					if 'X' not in subList and '*' not in subList:
						return 1
					else: 
						return -1
		return 0

	def check_end(self):
		# print('check end')
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def minimax(self,start, depth, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		# print(depth)
		# print(count)
		self.count +=1
		self.dict[depth] = self.dict[depth]+1
		self.dictall[depth] = self.dictall[depth]+1
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		# is end return X O None or tie
		#  evaluated function , heuistic function 
		# if the time up or depth reach call heuristic function 
		now = time.time()
		# print(depth >= self.player1d1)
		if((now - start) >= self.maxtime):
			score =  self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			self.depthdictall[depth] = self.depthdictall[depth]+1
			return (score, x, y)
		elif self.player_turn == 'X' and depth >= self.player1d1:
			score =  self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			self.depthdictall[depth] = self.depthdictall[depth]+1
			return (score, x, y)
		elif self.player_turn == 'O' and depth >= self.player2d2:
			score = self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			self.depthdictall[depth] = self.depthdictall[depth]+1
			return (score, x, y)
		elif result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.boardSize):
			for j in range(0, self.boardSize):
				if self.current_state[i][j] == '.':
					if depth == 0:
						start = time.time()
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(start,depth+1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(start ,depth+1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self,start, depth,alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		self.count +=1
		self.dict[depth] = self.dict[depth]+1
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		now = time.time()
		if(now - start > self.maxtime):
			score =  self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			return (score, x, y)
		elif self.player_turn == 'X' and depth >= self.player1d1:
			score =  self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			return (score, x, y)
		elif self.player_turn == 'O' and depth >= self.player2d2:
			score = self.evaluatedFunction()
			self.depthdict[depth] = self.depthdict[depth]+1
			return (score, x, y)
		if result == 'X':
			return (-100, x, y)
		elif result == 'O':
			return (100, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.boardSize):
			for j in range(0, self.boardSize):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(start, depth,alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(start, depth,alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		i = 0 
		# while True:
		while True:
			i +=1
			# print('while loop play'+str(i))
			self.draw_board()
			re = self.check_end()
			if re:
				if re == '.':
					text = 'It is a ties!'+'\n'
				else:
					text = 'The winner is '+re+'\n'
				text += "\n"
				print(F'i Evaluation time: {round(sum(self.evaluation)/len(self.evaluation), 7)}s')
				text +='i Evaluation time: '+ str(round(sum(self.evaluation)/len(self.evaluation), 7))+ 's\n'
				print('ii Total Heuristic evaluation: '+str(sum(self.depthdictall.values())))
				text += 'ii Toatl Heuristic evaluation: '+str(sum(self.depthdictall.values()))+'\n'
				print('iii Evaluations by depth: '+str(self.dictall))
				text += 'iii Evaluations by depth: '+str(self.dictall)+'\n'
				self.writeToFile('a',text)
				return
			start = time.time()
			if algo == self.MINIMAX:
				self.count =0
				self.depthdict = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(start,0,max=False)
				else:
					(_, x, y) = self.minimax(start,0,max=True)
			else: # algo == self.ALPHABETA
				self.count =0
				self.dict = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
				self.dict = {0:0, 1:0, 2:0, 3:0 ,4: 0,5:0,6:0,7:0,8:0}
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(start,0,max=False)
				else:
					(m, x, y) = self.alphabeta(start,0,max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
				if self.recommend:
					print(F'Evaluation time: {round(end - start, 7)}s')
					print(F'Recommended move: x = {x}, y = {y}')
				(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
				text = "\n"
				print(F'Player {self.player_turn} under AI control plays: x = {Alp[x]}, y = {y}')
				text +='Player '+self.player_turn+'under AI control plays: x = '+str(Alp[x])+ ', y = '+str(y) +'\n'
				print(F'i Evaluation time: {round(end - start, 7)}s')
				self.evaluation.append(round(end - start, 7))
				text +='i Evaluation time: '+ str(round(end - start, 7))+ 's\n'
				print('ii Heuristic evaluation: '+str(sum(self.depthdict.values())))
				text += 'ii Heuristic evaluation: '+str(sum(self.depthdict.values()))+'\n'
				print('iii Evaluations by depth: '+str(self.dict))
				text += 'iii Evaluations by depth: '+str(self.dict)+'\n'
				self.writeToFile('a',text)
				
			self.current_state[x][y] = self.player_turn
			self.move.append({x:y})
			# if self.check_end():
			# 	return
			self.switch_player()

def main():
	
	boardSize=None
	numBlocs=None
	winLineUp= None
	maximumDep1=None
	maximumDep2=None
	maxtime=None
	algo=None
	player1=None
	player2=None
	board = None
	blocsx = []
	blocsy = []

	while True: 
		if(boardSize is None):
			temp = input('Please choose the size of the board -n- an integer in [3..10] ')
			if(not temp.isdigit() or int(temp)<3 or int(temp)>10):
				continue
			else:
				boardSize = int(temp)
				# create board of 
				board = [['.' for x in range(boardSize)] for y in range(boardSize)] 
		if(numBlocs is None):
			temp = input('the number of blocs - b - an integer in [0..2n('+str(2*boardSize)+")] ")
			if(not temp.isdigit() or int(temp)<0 or int(temp)>2*boardSize):
				continue
			else:
				numBlocs = int(temp)
				for n in range(numBlocs):
					print(F'The positions of the blocs - b - board coordinates for blocs number {n}')
					x = int(input('enter the x coordiate: '))
					y = int(input('enter the y coordiate: '))
					board[x][y]="*"
					blocsx.append(x)
					blocsy.append(y)
		if(winLineUp is None):
			temp = input('Please enter the winning line-up size - s - an integer in [3..n('+ str(boardSize)+")] ")
			if(not temp.isdigit() or int(temp)<3 or int(temp)>boardSize):
				continue
			else:
				winLineUp = int(temp)
		if(maximumDep1 is None):
			temp = input('Please enter the maximum depth of the adversarial search for player 1 ')
			if(not temp.isdigit()):
				continue
			else:
				maximumDep1 = int(temp)
		if(maximumDep2 is None):
			temp = input('Please enter the maximum depth of the adversarial search for player 2 ')
			if(not temp.isdigit()):
				continue
			else:
				maximumDep2 = int(temp)
		if(maxtime is None):
			temp = input('Please enter the maximum allowed time (in seconds) for your program to return a move - t ')
			if(not temp.isdigit()):
				continue
			else:
				maxtime = int(temp)
		if(algo is None):
			temp = input('Please choose algorithm either minimax (FALSE=0) or alphabeta (TRUE=1) - a ')
			print(algo)
			print(int(temp) != 0)
			if(not temp.isdigit() or int(temp)<0 or int(temp)>1):
				continue
			else:
				if( int(temp) == 0):
					algo = Game.MINIMAX
				else:
					algo = Game.ALPHABETA

		if(player1 is None or player2 is None):
			temp = input('Please choose the the play modes\n\t0 for H-H, 1 for H-AI, 2 AI-H and 3 AI-AI. ')
			if(not temp.isdigit() or int(temp)<0 or int(temp)>3):
				continue
			else:
				temp = int(temp)
				if(temp == 0):
					player1=Game.HUMAN
					player2=Game.HUMAN
				elif(temp ==1):
					player1=Game.HUMAN
					player2=Game.AI
				elif(temp ==2):
					player1=Game.AI
					player2=Game.HUMAN
				else:
					player1=Game.AI
					player2=Game.AI
		if(boardSize is not None and numBlocs is not None and winLineUp is not None and maximumDep1 is not None and maximumDep2 is not None and maxtime is not None and algo is not None and player1 is not None and player2 is not None and board is not None):
			break	
	# board = [['*','.','.','.'],['.','.','.','*'],['.','.','.','.'],['*','.','.','*']]
	# blocsx =[1,2,3,4]
	# blocsy =[1,2,3,4]
	# winLineUp=4
	# maximumDep1=6
	# maximumDep2=6
	# boardSize=4
	# maxtime=8
	# numBlocs=4
	# player1=Game.AI
	# player2=Game.AI
	# algo=0
	g = Game( board,boardSize,	winLineUp,maximumDep1,maximumDep2,maxtime,numBlocs, recommend=True)
	text = 'n='+str(boardSize)+ ' b=' +str(numBlocs)+ ' s=' +str(winLineUp)+ ' t='+str(maxtime)+'\n'
	g.writeToFile('a', text)
	blocs = zip(blocsx,blocsy)
	text = 'blocs=' +str(list(blocs)) +'\n'
	g.writeToFile('a', text)
	text = 'Player 1: ' + str(player1) + ' d= '+str(maximumDep1) +' a= ' +str(algo) +'\n'
	g.writeToFile('a', text)
	text = 'Player 1: ' + str(player2) + ' d= '+str(maximumDep2) +' a= ' +str(algo) +'\n'
	g.writeToFile('a', text)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	g.play(algo=Game.MINIMAX,player_x=player1,player_o=player2)

if __name__ == "__main__":
	main()

