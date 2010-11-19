import sys
import string
import re
from myshlex import shlex
import utils
from utils import CompilerError

class LexError (CompilerError):

	def __init__(self,msg,leader):
		super(LexError,self).__init__(leader)
		self.msg = "Lexical error: " + msg

class LexAn():
	def __init__(self, file, filename):

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
									"(" : "<OPEN_PARENTHESIS>",
									")" : "<CLOSE_PARENTHESIS>",
									"[" : "<OPEN_BRACKET>",
									"]" : "<CLOSE_BRACKET>",
									"=" : "<EQUAL>",
									"<>": "<NOT_EQUAL_OP>", 
									"<=": "<LESS_EQUAL_OP>", 
									">=": "<GREATER_EQUAL_OP>", 
									"+" : "<ADD_OP>", 
									"-" : "<MINUS_OP>", 
									"*" : "<MULTIPLY_OP>", 
									"div" : "<DIV_OP>",
									"not" : "<NOT_LOGOP>",
									"or" : "<OR_LOGOP>",
									"and": "<AND_LOGOP>",
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
		
	def getLexeme(self):
		return self.originalLexeme
		
	def pushLexeme(self,file=None):
		if file:
			file.write('pushed: %s\n'%self.originalLexeme)
		self.lexer.push_token(self.getLexeme())
		
	def errorLeader(self):
		return self.lexer.error_leader()
	
	def getNextToken(self):
		try:
			self.originalLexeme = self.lexer.get_token()
		except EOFError:
			raise LexError('Lexical error: A comment in the source program was not closed!'% self.errorLeader())
		
		self.currentLexeme = self.originalLexeme.lower()
		if (self.currentLexeme in self.tokenDictionary):
			return self.tokenDictionary[self.currentLexeme]
		elif(self.currentLexeme == "."):
			try:
				self.forwardToken = self.lexer.get_token()
			except EOFError:
				raise LexError('A comment in the source program was not closed!', self.errorLeader())
			
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
				return "<GREATER_EQUAL_OP>"
			else:
				self.lexer.push_token(self.forwardToken)
				return "<GREATER_OP>"
		elif(self.currentLexeme == "<"):
			self.forwardToken = self.lexer.get_token()
			if(self.forwardToken == "="):
				self.originalLexeme = "<="
				return "<LESS_EQUAL_OP>"
			else:
				if self.forwardToken=='>':
					self.originalLexeme = "<>"
					return "<NOT_EQUAL_OP>"
				else:
					self.lexer.push_token(self.forwardToken)
					return "<LESS_OP>"
		elif(self.identifierRE.match(self.currentLexeme)):
			return "<IDENTIFIER>"
		elif(self.numberRE.match(self.currentLexeme)):
			return "<NUMBER>"
		elif(self.charRE.match(self.currentLexeme)):
			return "<CHAR>"
		else:
			raise LexError(msg = 'The lexeme "%s" could not be recognized' % self.originalLexeme, leader = self.errorLeader())
			
#######################################################################