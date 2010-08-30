import argparse
import sys
import string
from shlex import shlex

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
									"false" : "<FALSE>"
									# "<" : 
									}
									
		self.lexer = shlex(file)
		#self.currentLexemeIndex = -1
	
	def isKeyword(self, lexeme=None):
		if lexeme==None:
			lexeme = self.currentLexeme
		return lexeme in self.tokenDictionary
	
	def getNextToken(self):
		#self.currentLexemeIndex +=1
		#print self.lexer
		#if self.currentLexemeIndex > len(self.lexer):
		#	return "<EOF>"
		#else:
		self.currentLexeme = self.lexer.get_token()
		if (self.currentLexeme == shlex.eof):
			return "<EOF>"
		else:
		print repr(self.currentLexeme)
		if(self.isKeyword(self.currentLexeme)):
			print self.tokenDictionary[self.currentLexeme]
			return self.tokenDictionary[self.currentLexeme]
		else:
			pass
	
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
