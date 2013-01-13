from time import time
MAXLENGTH = 10
MINLENGTH = 2
DICTPATH = "C:\\Users\\Cyrus\\Desktop\\English Dictionary Words\\"
# initialize the dictionary
LISTOFWORDS = []
for L in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	for line in open(DICTPATH+L+" Words.txt"):
		LISTOFWORDS.append(line[:-1])
dictionary = set(LISTOFWORDS)

# This function solves the ruzzle and lists words in the order of
# point value rather than simply by length
# board_modifiers symbol meanings
# double word : 'D'
# triple word : 'T'
# double letter : 'd'
# triple letter : 't'
# default : ' '
def ruzzlesolve(board_str,board_modifiers):

	# the reference array
	board = [[],[],[],[]]
	starttime = time()

	# the list of found legal real words
	words = []

	# given a letter returns the integer point value ruzzle has for that letter
	def letterevaluator(char):
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

	# attach the letter tuples to the board with the correct modifiers coordinates
	# and the values of each respective letter
	for i, L in enumerate(board_str):
		board[i/4].append((L,board_modifiers[i],letterevaluator(L),(i%4,i/4)))

	# recursive solver. 
	# started on all 16 die it goes through all possible letter paths and adds words that 
	# corresponds to the loaded dictionary to the words array
	def solve(wurd,currentword, x, y):
		if (x > 3 or x < 0 or y > 3 or y < 0 or board[y][x] in currentword or len(currentword) > MAXLENGTH):
			return
		V = currentword+(board[y][x],)
		W = wurd + board[y][x][0]
		if (len(currentword) >= MINLENGTH):
			if (W in dictionary):
				words.append(V)
		solve(W,V,x+1,y+1)
		solve(W,V,x+1,y)
		solve(W,V,x+1,y-1)
		solve(W,V,x,y+1)
		solve(W,V,x,y-1)
		solve(W,V,x-1,y+1)
		solve(W,V,x-1,y)
		solve(W,V,x-1,y-1)

	# Calculates the score of a word
	# Used after all vetted words have been found
	def score(word):
		# returns the letter modifier
		def interpretS(val):
			if (val == 't'):
				return 3
			if (val == 'd'):
				return 2
			return 1

		# returns the multiplication modifier
		def interpretM(val):
			if (val == 'T'):
				return 3
			if (val == 'D'):
				return 2
			return 1
		
		mult = 1
		su = 0
		# sum all the individual tiles with letter modifiers
		# and combine the word modifiers into one multiplicative modifier
		for i in word:
			su += i[2] * interpretS(i[1])
			mult *= interpretM(i[1])
		# return the word score + length score 
		return su * mult + max(len(word)-4,0) * 5

	# initialize the solve functions on each starting location
	# and notify when each row has been checked
	for x in range(4):
		for y in range(4):
			print "X",
			solve("",tuple(),x,y)
		print ""
	print "done"

	# create a secondary list of tuples of the form:
	# (the word , the point value of the word)
	wordlist = map(lambda word: ("".join(map(lambda v: v[0], word)),score(word)),words)
	# sort the list by score
	wordlist.sort(key=lambda word: word[1],reverse=True)
	# iterate through the words, if a word is currently unique, add it to checklist
	# if it is not unique, then the word currently being checked has a lower score
	# than the previous word (since we reversed the order), thus remove the lower
	# scoring duplicate
	checklist = []
	for i, word in enumerate(wordlist):
		if word[0] in checklist:
			del(wordlist[i])
		else:
			checklist.append(word[0])

	# to make it easy on the user we reverse it so that the 
	# higher value words are printed last
	wordlist.reverse()
	for word in wordlist:
		print "%3d :: %s" % (word[1],word[0])
	print "Solved in",time()-starttime,"seconds"

# our dictionary is not completely the same as ruzzle's
# I added this function to make it easy to add words to the dictionary
def addWord (word):
	if (word in dictionary):
		print "Already included"
		return
	if (not word[0] in "abcdefghijklmnopqrstuvwxyz"):
		print "invalid word"
		return
	else:
		dictionary.add(word)
		newwords = open(DICTPATH + "extra.txt",'a')
		newwords.write(word+'\n')