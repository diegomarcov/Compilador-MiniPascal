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
									".." : "<SUBRANGE>",
									":=" : "<ASSIGNMENT>",
									"," : "<COMMA>",
									";" : "<SEMI_COLON>",
									'' : "<EOF>"
									}
									
		self.lexer = shlex(file)
		self.lexer.quotes = ''
		self.lexer.wordchars += "'"
		self.lexer.commenters = "//"
		#estas son expresiones regulares. Es importante leer la documentacion de la libreria re
		self.identifierRE = re.compile('^[a-zA-Z][a-zA-Z0-9]*$')
		self.numberRE = re.compile('^[0-9]+$')
		self.charRE = re.compile("^'[a-zA-Z0-9!#$%&()*+,\"\\-./:;<=>?@[\\]_`{|}~]'$")
	
	def getCurrentLine(self):
		return self.lexer.lineno
		
	def getCurrentLexeme(self):
		return self.originalLexeme
	
	def getNextToken(self):
		try:
			self.originalLexeme = self.lexer.get_token()
		except:
			raise LexError('\nLexical error: A comment in the source program was not closed!')
		self.currentLexeme = self.originalLexeme.lower()
		if (self.currentLexeme in self.tokenDictionary):
			return self.tokenDictionary[self.currentLexeme]
		elif(self.currentLexeme == "."):
			self.forwardToken = self.lexer.get_token()
			if (self.forwardToken == "."):
				self.originalLexeme = ".."
				return "<SUBRANGE_SEPARATOR>"
			else:
				self.lexer.push_token(self.forwardToken)
				return "<END_PROGRAM>"
		elif(self.currentLexeme == ":"):
			self.forwardToken = self.lexer.get_token()
			if(self.forwardToken == "="):
				self.originalLexeme = ":="
				return "<ASSIGNMENT>"
			else:
				self.lexer.push_token(self.forwardToken)
				return "<TYPE_DECLARATION>"
		elif(self.identifierRE.match(self.currentLexeme)):
			return "<IDENTIFIER>"
		elif(self.numberRE.match(self.currentLexeme)):
			return "<NUMBER>"
		elif(self.charRE.match(self.currentLexeme)):
			return "<CHAR>"
		else:
			#cual es el proposito de self.lexer.error_leader(self.lexer.infile) en esta excepcion? hasta ahora, TODOS los casos me dieron 'None', o sea, solamente molesta...
			raise LexError(self.lexer.error_leader(self.lexer.infile)+'Lexical error: The lexeme "' + self.originalLexeme + '" couldn\'t be recognized')
			
#######################################################################
			

