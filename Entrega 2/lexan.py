import sys
import string
from shlex import shlex
from types import IntType, LongType

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
		#self.currentLexemeIndex = -1
	
	def isKeyword(self, lexeme=None):
		if lexeme==None:
			lexeme = self.currentLexeme
		return lexeme in self.tokenDictionary
	
	def getCurrentLine(self):
		return self.lexer.lineno
		
	def getCurrentLexeme(self):
		return self.currentLexeme
	
	def makeNumber(self, source):
		try:
			number = str(int(source))
		except:
			number = None
		return number
	
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
			if (self.lexer.read_token() == "."):
				self.lexer.get_token()
				self.currentLexeme = ".."
				return "<SUBRANGE_SEPARATOR>"
			else:
				return "<END_PROGRAM>"
		elif(self.currentLexeme == self.makeNumber(self.currentLexeme)):
			return "<NUMBER>"
		else:
			return "<IDENTIFIER>"
