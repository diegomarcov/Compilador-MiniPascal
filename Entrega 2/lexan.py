import sys
import string
import re
from shlex import shlex
from types import IntType, LongType

class LexError (Exception):

	def ___init___(self,msg):
		self.message = msg
		
	def __str__(self):
		return self.message

class LexAn():
	def __init__(self, file):

		self.tokenDictionary = {"program" : "<PROGRAM>",
									"type" : "<TYPE>",
									"const" : "<CONST>",
									"var" : "<VAR>",
									"array" : "<ARRAY>",
									"of" : "<OF>",
									"function" : "<FUNCTION>",
									"procedure" : "<PROCEDURE>",
									"begin" : "<BEGIN>",
									"end" : "<END>",
									"while" : "<WHILE>",
									"do" : "<DO>",
									"if" : "<IF>",
									"then" : "<THEN>",
									"else" : "<ELSE>",
									"div" : "<DIV>",
									"not" : "<NOT>",
									"or" : "<OR>",
									"and" : "<AND>",
									"true" : "<TRUE>",
									"false" : "<FALSE>",
									"(" : "<PARENTHESIS>",
									")" : "<PARENTHESIS>",
									"[" : "<BRACKET>",
									"]" : "<BRACKET>",
									"=" : "<EQUAL>",
									"<" : "<RELOP>",
									">" : "<RELOP>", 
									"<>": "<RELOP>", 
									"<=": "<RELOP>", 
									">=": "<RELOP>", 
									"+" : "<ARITHOP>", 
									"-" : "<ARITHOP>", 
									"*" : "<ARITHOP>", 
									"div" : "<ARITHOP>",
									"not" : "<UN_LOGOP>",
									"or" : "<BIN_LOGOP>",
									"and": "<BIN_LOGOP>",
									":" : "<TYPE_DECLARATION>",
									".." : "<SUBRANGE>",
									":=" : "<ASSIGNMENT>",
									"," : "<COMMA>",
									";" : "<SEMI_COLON>",
									'' : "<EOF>"
									}
									
		self.lexer = shlex(file)
		self.lexer.quotes = '"'
		self.lexer.commenters = "//"
		#estas son expresiones regulares. Es importante leer la documentacion de la libreria re
		self.identificatorRE = re.compile('^[a-zA-Z][a-zA-Z0-9]*$')
		self.numberRE = re.compile('^[0-9]+$')
		#self.currentLexemeIndex = -1
	
	def isKeyword(self, lexeme=None):
		if lexeme==None:
			lexeme = self.currentLexeme
		return lexeme in self.tokenDictionary
	
	def getCurrentLine(self):
		return self.lexer.lineno
		
	def getCurrentLexeme(self):
		return self.currentLexeme
	
	# def makeNumber(self, source):
		# try:
			# number = str(int(source))
		# except:
			# number = None
		# return number
	
	def getNextToken(self):
		#self.currentLexemeIndex +=1
		#print self.lexer
		#if self.currentLexemeIndex > len(self.lexer):
		#	return "<EOF>"
		#else:
		self.currentLexeme = self.lexer.get_token().lower()
		#print "Current lexeme: 		%s" % repr(self.currentLexeme)
		if (self.currentLexeme in self.tokenDictionary):
			return self.tokenDictionary[self.currentLexeme]
		elif(self.currentLexeme == "."):
			self.forwardToken = self.lexer.get_token()
			if (self.forwardToken == "."):
				self.currentLexeme = ".."
				return "<SUBRANGE_SEPARATOR>"
			else:
				self.lexer.push_token(self.forwardToken)
				return "<END_PROGRAM>"
		# elif(self.currentLexeme == ":"):
			# print "AAAAAAAAAAAAAAAAAAAAASSSSSSSDDDDDDDDDDDDDDDDDDDDDDDD"
			# if(self.lexer.read_token() == "="):
				# self.lexer.get_token()
				# self.currentLexeme = ":="
				# return "<ASSIGNMENT>"
		elif(self.identificatorRE.match(self.currentLexeme)):
			return "<IDENTIFIER>"
		elif(self.numberRE.match(self.currentLexeme)):
			return "<NUMBER>"
		else:
			raise LexError(self.lexer.error_leader(self.lexer.infile)+'Lexical error: The lexeme "' + self.currentLexeme + '" couldn\'t be recognized')
			
#######################################################################
			

