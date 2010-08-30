import argparse
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
									"." : "<PROGRAM_END>",
									}
									
		self.lexer = shlex(file)
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
		else:
			if (self.currentLexeme == ''):
				return "<EOF>"
			else:
				if(self.currentLexeme == self.makeNumber(self.currentLexeme)):
					return "<NUMBER>"
				else:
					return "<IDENTIFIER>"
	
parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
parser.add_argument('inputFile', metavar='IN_FILE', type=file, help='The source .pas file')
parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

args = parser.parse_args()
inputFile = args.inputFile
#fileContent = inputFile.read()

'''
print 'ORIGINAL:', repr(fileContent)
print

print 'TOKENS:'
lexer = shlex(fileContent)
for token in lexer:
	print "%s @ %s" % (repr(token), lexer.lineno)
'''

lexicalAnalyzer = LexAn(inputFile)
print "LEXEME				TOKEN				LINE NUMBER"
token = lexicalAnalyzer.getNextToken()
while(token != "<EOF>"):
	#print token
	print "%s			%s				%s" % (lexicalAnalyzer.getCurrentLexeme(), token, lexicalAnalyzer.getCurrentLine())
	token = lexicalAnalyzer.getNextToken()