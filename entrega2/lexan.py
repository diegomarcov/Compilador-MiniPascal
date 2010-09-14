import sys
import string
import re
from myshlex import shlex
from types import IntType, LongType

class LexError (Exception):

	def __init__(self,msg):
		super(LexError,self).__init__()
		self.message = msg
		
	def __str__(self):
		return self.message

class LexAn():
	def __init__(self, file,filename):

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
									"(" : "<OPEN_PARENTHESIS>",
									")" : "<CLOSE_PARENTHESIS>",
									"[" : "<OPEN_BRACKET>",
									"]" : "<CLOSE_BRACKET>",
									"=" : "<EQUAL>",
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
									
		self.lexer = shlex(file,filename)
		self.lexer.quotes = ''
		self.lexer.wordchars += "'"
		self.lexer.commenters = "//"
		#estas son expresiones regulares. Es importante leer la documentacion de la libreria re
		self.identifierRE = re.compile('^[a-zA-Z][a-zA-Z0-9]*$')
		self.numberRE = re.compile('^[0-9]+$')
		self.charRE = re.compile("^'[a-zA-Z0-9]'$")
	
	def getCurrentLine(self):
		return self.lexer.lineno
		
	def getCurrentLexeme(self,file=None):
		if file:
			file.write('%s\n'%self.originalLexeme)
		return self.originalLexeme
		
	def pushLexeme(self):
		self.lexer.push_token(self.getCurrentLexeme)
		
	def errorLeader(self):
		return self.lexer.error_leader()
	
	def getNextToken(self):
		try:
			self.originalLexeme = self.lexer.get_token()
		except EOFError:
			raise LexError('\n%sLexical error: A comment in the source program was not closed!'% self.errorLeader())
			
		self.currentLexeme = self.originalLexeme.lower()
		if (self.currentLexeme in self.tokenDictionary):
			return self.tokenDictionary[self.currentLexeme]
		elif(self.currentLexeme == "."):
			try:
				self.forwardToken = self.lexer.get_token()
			except EOFError:
				raise LexError('\n%sLexical error: A comment in the source program was not closed!' % self.errorLeader())
			
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
		elif(self.currentLexeme == ">"):
			self.forwardToken = self.lexer.get_token()
			if(self.forwardToken == "="):
				self.originalLexeme = ">="
			else:
				self.lexer.push_token(self.forwardToken)
			return "<RELOP>"
		elif(self.currentLexeme == "<"):
			self.forwardToken = self.lexer.get_token()
			if(self.forwardToken == "="):
				self.originalLexeme = "<="
			else:
				self.lexer.push_token(self.forwardToken)
			return "<RELOP>"
		elif(self.identifierRE.match(self.currentLexeme)):
			return "<IDENTIFIER>"
		elif(self.numberRE.match(self.currentLexeme)):
			return "<NUMBER>"
		elif(self.charRE.match(self.currentLexeme)):
			return "<CHAR>"
		else:
			raise LexError('\n%sLexical error: The lexeme "%s" couldn\'t be recognized' % (self.errorLeader(),self.originalLexeme))
			
#######################################################################