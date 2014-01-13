from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from time import time, sleep
from random import seed, random
from sys import argv
import logging

RUZZLE_OPTIONS = {
	DIFFICULTY = 1
	BASE_PATH = ""
	DICT_PATH = "" + "English Dictionary Words\\"

	LOG_LEVEL = logging.INFO # logging.DEBUG
	BOARD_SIZE = 4
	INPUT_SIZE = BOARD_SIZE * BOARD_SIZE
	MAX_WORD_LENGTH = INPUT_SIZE # 16
	MIN_WORD_LENGTH = 2

	# pixels from top edge of screen to first row
	BOARD_PADDING_TOP = 213
	# pixels from left edge of screen to first column 
	BOARD_PADDING_LEFT = 16
	# pixels of padding between each column
	COLUMN_PADDING = 16
	# pixels of padding between each row
	ROW_PADDING = 17
	# size of letter blocks in pixels
	BLOCK_HEIGHT = 100
	BLOCK_WIDTH = 100

	# time taken to draw one letter-to-letter segment of a word path
	DRAW_SPEED = .001 #seconds
	NO_DEVICE = True
}

class RuzzleSolver:
	def __init__(self, options):
		self.__dict__.update(options or {})

		self.DRAG_COORDINATES = {k:(
		    k[0]*self.COLUMN_PADDING+self.BOARD_PADDING_LEFT+k[0]*self.BLOCK_WIDTH +self.BLOCK_WIDTH /2,
		    k[1]*self.ROW_PADDING +self.BOARD_PADDING_TOP +k[1]*self.BLOCK_HEIGHT+self.BLOCK_HEIGHT/2
		    ) for k in [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]}
		logging.basicConfig(
			filename="ruzzlesolver.log",
		    filemode='a',
		    format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
		    datefmt='%H:%M:%S',
	        level=self.LOG_LEVEL
	        )	
		self.dictionary = set()
		self.word_parts = set()
		logging.info("initializing the dictionary")
		word_parts_file = open(DICT_PATH+"Word Parts.txt",'w')
		for L in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			with dict_page as open(DICT_PATH+L+" Words.txt",'r'):
			    for line in dict_page:
			        self.dictionary.add(line[:-1])
			        word_part = ""
			        for letter in line[:-1]:
			            word_part += letter
			            if (not word_part in word_parts):
			                word_parts_file.write(word_part+"\n")
			                self.word_parts.add(word_part)
		with dict_page as open(DICT_PATH+"extra.txt","r"): 
			for line in dict_page:
			    self.dictionary.add(line[:-1])
			    word_part = ""
			    for letter in line[:-1]:
			        word_part += letter
			        if (not word_part in word_parts):
			            word_parts_file.write(word_part+"\n")
			            self.word_parts.add(word_part)
        word_parts_file.close()

	class IncorrectInput(Exception):
	    def __init__(self, value):
	        self.value = value
	    def __str__(self):
	        return repr(self.value) + " is not the correct number of characters in length"

	# given a letter returns the integer point value ruzzle has for that letter
    def letterEvaluator(self, char):
        if (char in ['x']):
            return 8
        if (char in ['k']):
            return 5
        if (char in ['b','c','f','h','p','w','y']):
            return 4
        if (char in ['m','g','v']):
            return 3
        if (char in ['d','u']):
            return 2
        return 1

	# This function solves the ruzzle and lists words in the order of
	# --board modifier symbols--
	# double word : 'D'
	# triple word : 'T'
	# double letter : 'd'
	# triple letter : 't'
	# no modifier : ' '
	def ruzzleSolve(self, board_str, board_modifiers):
		seed(time())
	    if (len(board_str) != self.INPUT_SIZE):
	        raise IncorrectInput(board_str)
	    if (len(board_modifiers) != self.INPUT_SIZE):
	        raise IncorrectInput(board_modifiers)

	    board = [[],[],[],[]]
	    startTime = time()

	    # the list of found legal real words
	    words = []

	    for i, L in enumerate(board_str):
	        board[i/4].append((L,board_modifiers[i],self.letterEvaluator(L),(i%4,i/4)))

	    # recursive solver. 
	    def solve(wurd,currentword, x, y):
	        if (x > 3 or x < 0 or y > 3 or y < 0 or board[y][x] in currentword or len(currentword) > self.MAX_WORD_LENGTH):
	            return
	        V = currentword+[board[y][x],]
	        W = wurd + board[y][x][0]
	        if (len(V) >= self.MIN_WORD_LENGTH):
	            if (W in self.RUZZLE_DICTIONARY):
	                words.append(V)
	                loging.debug(",".join(map(lambda x: str(x[3]),V))+" - "+W+" - found"+'\n')
	        if (W in word_parts):
	            loging.debug(",".join(map(lambda x: str(x[3]),V))+" - "+W+" - parts"+'\n')
	            solve(W,V,x+1,y+1)
	            solve(W,V,x+1,y)
	            solve(W,V,x+1,y-1)
	            solve(W,V,x,y+1)
	            solve(W,V,x,y-1)
	            solve(W,V,x-1,y+1)
	            solve(W,V,x-1,y)
	            solve(W,V,x-1,y-1)
	        else:
	            loging.debug(",".join(map(lambda x: str(x[3]),V))+" - "+W+" - failed"+'\n')

	    # initialize the solve functions on each starting location
	    for x in range(self.BOARD_SIZE):
	        for y in range(self.BOARD_SIZE):
	            solve("",[],x,y)

	    loging.info("scoring");
	    wordlist = map( 
	    	lambda word: (
	    		"".join(map(lambda v: v[0], word)),
	    		self.score(word),
	    		word ),
	    	words).sort(key=lambda word: word[1],reverse=True)

	    checklist = set()
	    for i, word in enumerate(wordlist):
	        if word[0] in checklist:
	            del(wordlist[i])
	        else:
	            checklist.add(word[0])
    	self.drawWords(wordlist)

    def drawWords (self, words ):
    	if (self.NO_DEVICE)
	    loging.info("connecting to the device")
	    AndroidDevice = MonkeyRunner.waitForConnection()

    	def drawPath (wordArray):
	        AndroidDevice.touch(
	        	x = self.DRAG_COORDINATES[wordArray[0]][0],
	        	y = self.DRAG_COORDINATES[wordArray[0]][1],
	        	type = MonkeyDevice.DOWN)
	        sleep( self.DRAW_SPEED )
	        for coordinate in wordArray[1:]:
	            AndroidDevice.touch(
	            	x = self.DRAG_COORDINATES[coordinate][0],
	            	y = self.DRAG_COORDINATES[coordinate][1],
	            	type = MonkeyDevice.MOVE)
	            sleep( self.DRAW_SPEED )
	        AndroidDevice.touch(
	        	x = self.DRAG_COORDINATES[wordArray[-1]][0],
	        	y = self.DRAG_COORDINATES[wordArray[-1]][1],
	        	type = MonkeyDevice.UP)
	        sleep( self.DRAW_SPEED )

	    loging.info("drawing")
	    for word in words:
	        loging.debug( "%3d :: %s" % (word[1],word[0]))
	        if (random() < DIFFICULTY):
	            drawPath(map(lambda x: x[3],word[2]))
	    loging.info("Solved in",time()-startTime,"seconds")

    def score(self, word):
        letterModifiers = {
            't': 3,
            'd': 2
	        }
        wordModifiers = {
            'T': 3,
            'D': 2
	        }
        wordMultiplier = 1
        letterScore = 0
        for letter in word:
            letterScore += letter[2] * (letterModifiers[letter[1]] or 1)
            wordMultiplier *= (wordModifiers[letter[1]] or 1)
        return letterScore * wordMultiplier + max(len(word)-4,0) * 5

	def addWord (self, word):
	    if (word in self.RUZZLE_DICTIONARY):
	        print "Already included"
	        return
	    if (not word[0] in "abcdefghijklmnopqrstuvwxyz"):
	        print "invalid word"
	        return
	    else:
	        self.RUZZLE_DICTIONARY.add(word)
	        newwords = open(DICT_PATH + "extra.txt",'a')
	        newwords.write(word+'\n')

if __name__ == "__main__":
	RUZZLE = new RuzzleSolver( RUZZLE_OPTIONS )
	if (len(argv) > 3):
		RUZZLE.DIFFICULTY = float(argv[3])
	if not len(argv) > 2: 
		print argv[0] + " must be called with two arguments of : "
	else:
		RUZZLE.ruzzleSolve( argv[1], argv[2] )
