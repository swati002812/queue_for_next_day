'''
	first call the ProcessFile function which will process the file text and create a list of member_day_data
'''

from queue_order.member_day_data import MemberDayData
from docx import *
import docx
import math

class QueueManipulator:
	CASE_TYPE_NORMAL = 'normal'
	CASE_TYPE_COMPLETE = 'complete'
	CASE_TYPE_CORNER = 'corner'

	WORD_BOLD = 'bold'
	WORD_NORMAL = 'normal'

	def __init__(self, baseline, filename):
		self.baseline = baseline
		self.filename = filename
		self.member_day_data_list = []
		print('Queue for next day: ')

	def print(self):
		for member_data in self.member_day_data_list:
			print("name:", member_data.name)
			print("is_on_leave_today:", member_data.is_on_leave_today)
			print("no_of_rounds:",member_data.no_of_rounds)
			print("is_BM:", member_data.is_BM)
			print("temp_variable:", member_data.temp_variable)
			print("\n")
		print('above_BL:', self.above_BL)
		print('equal_BL:', self.equal_BL)
		print('below_BL:', self.below_BL)
		print('Case Type:', self.case_type)
		print('Queue Type', self.queue_type)


########################################################## PROCESS WORDS AND CREATE MEMBER DAY DATA ######################################

	def getName(self, word):
		name = word.strip().split(" ")
		return name[0]
	
	'''
		getTempVariable functions
		1. no_of_rounds > baseline return 1
		2. no_of_rounds < baseline return -1
		3. else return 0
	'''
	def getTempVariable(self, no_of_rounds):
		if no_of_rounds > self.baseline:
			return 1
		elif no_of_rounds == self.baseline:
			return 0
		else:
			return (-1)
	
	def isNegativeNumber(self, text):
		num = text.split("-")
		if len(num) > 1 and num[1].isnumeric():
			return True
		return False
	
	'''
		getNoOfRounds function
			1. strip and slipt on space
			2. checks value of last index is numberic
			3. if yes return num and 1 for -1, and for non numeric text 
				return self baseline - 1 for normal and baseline for bold
	'''
	def getNoOfRounds(self, word, type):
		text = word.strip().split(" ", 10)
		if len(text) > 1:
			if text[len(text) - 1] != '':
				num = text[len(text) - 1].strip()
				if num.isnumeric() or self.isNegativeNumber(num):
					if self.isNegativeNumber(num):
						return str(0)
					return str(num)
		if type == self.WORD_BOLD:
			return str(self.baseline)
		return str(int(self.baseline) - 1)
	
	'''
		member was bm if, 
		1. word contains parantheses
		2. word in parantheses should be bm
	'''
	def checkBM(self, word):
		text = word.split("(")
		if (len(text) > 1):
			text = text[1].split(")")[0].strip()
			if text == 'bm':
				return 'Y'
		return None
	
	def isMinusOneMember(self, word):
		text = word.strip().split(" ", 10)
		if len(text) > 1:
			if text[len(text) - 1] != '':
				num = text[len(text) - 1].strip()
				if self.isNegativeNumber(num):
					return True
		return False
	
	'''
		member was on leave if words contains
		1. left and right paranthese
		2. and not bm
	'''
	def checkIsOnLeaveToday(self, word):
		text = word.split("(")
		if len(text) > 1:
			if not self.checkBM(word):
				return 'Y'
			else:
				return 'N'
		return 'N'

	'''
		processWords creates a member_data_data and append in member_day_data_list it fetches
		1. name
		2. bm (bin manager info)
		3. leave info
		4. no of rounds
	'''
	def processWords(self, words, type):
		for word in words:
			#check for empty word
			if word == ' ':
				continue

			# creating tempMember list
			temp_member = MemberDayData()
			temp_member.name = self.getName(word)
			temp_member.is_BM = self.checkBM(word)
			temp_member.is_on_leave_today = self.checkIsOnLeaveToday(word)
			temp_member.no_of_rounds = self.getNoOfRounds(word, type)

			if temp_member.is_on_leave_today == 'Y':
				temp_member.no_of_rounds = str(0)
			
			temp_member.temp_variable = self.getTempVariable(temp_member.no_of_rounds)
			
			if self.isMinusOneMember(word):
				temp_member.is_already_minus_one = True


			

			#appending member in global list
			self.member_day_data_list.append(temp_member)
	
	def isQueueCharacter(self, character):
		return character != '>'
		# return character.isalpha() or character.isnumeric() or character == ' ' or character == '(' or character == ')' or character == '-' or character == '_'

	'''
		get word split the words based on the right arrow (>) and checks the character should be
		alpha (a-z), number(1-10), space (' '), left and right parantheses , - and __
	'''
	def getWord(self, text):
		words = []
		temp = ''
		for i in range(len(text)):
			if not self.isQueueCharacter(text[i]):
				if temp != '':
					words.append(temp)
					temp = ''
					continue
			else:
				if (text[i].isnumeric() or text[i] == '(') and text[i-1] != '-':
					temp = temp + " " + text[i]
				else:
					temp = temp + text[i]
				
		if temp != '':
			words.append(temp)
		return words

	'''
		process file function process the docx file and retrieve all the details
	'''
	def processFile(self):
		document = Document(self.filename)
		self.member_day_data_list = []
		for paragraph in document.paragraphs:
			boldWords = ''
			for run in paragraph.runs:
				word = run.text.lower().replace(u'\xa0', u' ')
				tempWords = self.getWord(word)
				if len(tempWords) == 0:
					continue

				# checks if the word is bold and a number then the number belongs to previous word
				if run.bold and (tempWords[0].strip()).isnumeric():
					boldWords = boldWords + " " + " ".join(tempWords)
				# check for non bold word numeric word
				elif boldWords != '' and (tempWords[0].strip()).isnumeric():
					boldWords = boldWords + " " + " ".join(tempWords)
				# checks if the word is bold then appending with existing words
				elif run.bold:
					boldWords = boldWords + ">" + ">".join(tempWords)
				# this is for non bold , in this we process boldWords if not empty 
				else:
					if boldWords != '':
						words = self.getWord(boldWords)
						self.processWords(words, self.WORD_BOLD)
						boldWords = ''
					self.processWords(tempWords, self.WORD_NORMAL)
			if boldWords != '':
				words = self.getWord(boldWords)
				self.processWords(words, self.WORD_BOLD)
				boldWords = ''

###################################################################################### PROCESS WORDS ##############################################



	
###################################################################################### CASE TYPE ##################################################

	def isMemberWorkingToday(self, member_data):
		if member_data.is_on_leave_today == 'Y' or member_data.is_BM == 'Y':
			return False
		return True

	def setQueueType(self):
		if (self.case_type == self.CASE_TYPE_COMPLETE):
			self.queue_type = 0
			return

		working_people = self.above_BL + self.below_BL + self.equal_BL
		working_people_half = math.floor(working_people/2)
		if working_people_half <= self.equal_BL:
			self.queue_type = -1
		else:
			self.queue_type = 1

	def setBMType(self):
		if self.case_type == self.CASE_TYPE_NORMAL:
			if self.above_BL > 0:
				self.bold_BM = 1
			else:
				self.bold_BM = 0
		elif self.case_type == self.CASE_TYPE_CORNER:
			if self.above_BL <= self.below_BL:
				self.bold_BM = 0
			else:
				self.bold_BM = 1
		else:
			self.bold_BM = 0

	def calculateAboveAndBelowBaselineValues(self):
		self.above_BL = 0
		self.below_BL = 0
		self.equal_BL = 0

		for member_data in self.member_day_data_list:
			if (not self.isMemberWorkingToday(member_data)):
				continue
			if member_data.no_of_rounds > self.baseline:
				self.above_BL = self.above_BL + 1
			elif member_data.no_of_rounds == self.baseline:
				self.equal_BL = self.equal_BL + 1
			else:
				self.below_BL = self.below_BL + 1

	def setCaseType(self):
		self.case_type = ''

		self.calculateAboveAndBelowBaselineValues()
		
		if self.above_BL == 0 and self.below_BL == 0:
			self.case_type = self.CASE_TYPE_COMPLETE
		elif self.above_BL != 0 and self.below_BL != 0:
			self.case_type = self.CASE_TYPE_CORNER
		else:
			self.case_type = self.CASE_TYPE_NORMAL

		self.setBMType()
		self.setQueueType()

###################################################################### CASE TYPE #########################################################

####################################################### People On Leave #############################################

	def isMemberOnLeaveToday(self, member_data):
		if (member_data.is_on_leave_today == 'Y'):
			return True
		return False

	def isMemberNotOnleaveTodayAndNotBM(self, member_data):
		if (member_data.is_on_leave_today == 'N' and member_data.is_BM == None):
			return True
		return False
	
	def findPersonIsNotOnLeaveTodayRight(self, start, end):
		if (start > end or start < 0):
			return None

		for i in range(start, end + 1):
			if i >= len(self.member_day_data_list):
				break
			member_data = self.member_day_data_list[i]
		
			if self.isMemberNotOnleaveTodayAndNotBM(member_data):
				return member_data

		return None
	
	def findPersonIsNotOnLeaveTodayLeft(self, start, end):
		if (end < start or end < 0):
			return None

		for i in range(end, start - 1, -1):
			if i < 0:
				break
			member_data = self.member_day_data_list[i]

			if self.isMemberNotOnleaveTodayAndNotBM(member_data):
				return member_data

		return None


	def setTempVariableForPersonOnLeave(self):
			for i in range(0, len(self.member_day_data_list)):
				if (not self.isMemberOnLeaveToday(self.member_day_data_list[i])):
					continue

				member_data_right = self.findPersonIsNotOnLeaveTodayRight(i+1, len(self.member_day_data_list))
				member_data_left = self.findPersonIsNotOnLeaveTodayLeft(0, i-1)
				if member_data_left != None and member_data_right != None:
					self.member_day_data_list[i].temp_variable = min(member_data_left.temp_variable, member_data_right.temp_variable)
				elif member_data_left != None:
					self.member_day_data_list[i].temp_variable = member_data_left.temp_variable
				else:
					self.member_day_data_list[i].temp_variable = member_data_right.temp_variable

######################################################  People On Leave #######################################################################################


###############################################################  Bin Manager Temp Variable ################################


	def setBinManagerTempVariable(self):
		for i in range(0, len(self.member_day_data_list)):
			member_data = self.member_day_data_list[i]
			if member_data.is_BM == 'Y':
				self.member_day_data_list[i].temp_variable = self.bold_BM
				break

################################################################## Bin Manager Temp Variable #####################

	def printQueue(self):
		queue_for_tom = ' '
		i = 0 
		for member_day_data in self.member_day_data_list:
			queue_for_tom = queue_for_tom + member_day_data.name
			if member_day_data.is_bold == True:
				queue_for_tom = queue_for_tom + ' b '
			if member_day_data.is_minus_one == True or member_day_data.is_already_minus_one == True:
				queue_for_tom = queue_for_tom + ' -1 '
			if member_day_data.diff != None:
				queue_for_tom = queue_for_tom + member_day_data.diff
			
			if i < len(self.member_day_data_list) - 1:
				queue_for_tom = queue_for_tom + ' > '
			i = i + 1
		print(queue_for_tom)

	def markBoldAndMinusOneMemberData(self, member_data):
		diff = int(member_data.no_of_rounds) - int(self.baseline)
		if diff >= 2: # picked more than baseline 
			member_data.diff = str(diff)
		
		if self.queue_type == 1:
			if diff >= 1:
				diff = diff + 1
				member_data.diff = str(diff)
		member_data.is_bold = True
		return member_data

	def markBoldOrMinusOne(self):
		queue_for_tom = ' '
		for i in range(0, len(self.member_day_data_list)):
			self.member_day_data_list[i].name = self.member_day_data_list[i].name.capitalize()
			if self.queue_type == -1:
				if self.member_day_data_list[i].temp_variable == 1: #bold
					self.member_day_data_list[i] = self.markBoldAndMinusOneMemberData(self.member_day_data_list[i])
				elif self.member_day_data_list[i].temp_variable == 0: # neither bold nor -1
					self.member_day_data_list[i].is_minus_one = False
					self.member_day_data_list[i].is_bold = False
				else:
					self.member_day_data_list[i].is_minus_one = True
			elif self.queue_type == 1: # bold queue
				if self.member_day_data_list[i].temp_variable == 1:
					self.member_day_data_list[i] = self.markBoldAndMinusOneMemberData(self.member_day_data_list[i])
				elif self.member_day_data_list[i].temp_variable == 0:
					self.member_day_data_list[i].is_bold = True
				else:
					self.member_day_data_list[i].is_minus_one = False
			else: # complete case
				if self.member_day_data_list[i].temp_variable == 1:
					self.member_day_data_list[i] = self.markBoldAndMinusOneMemberData(self.member_day_data_list[i])
				else:
					self.member_day_data_list[i].is_minus_one = False
					self.member_day_data_list[i].is_bold = False
