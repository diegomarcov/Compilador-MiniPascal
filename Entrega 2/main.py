import sys
import argparse, io
from lexan import LexAn,LexError

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = io.BufferedReader(io.FileIO(args.inputFile))
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
	print "\nStarting file lexical analysis...\n\n"
	print "----------------------------------------------------------------------------------------------"
	print "|%s|%s|%s|" % ("LEXEME".center(35), "TOKEN".center(35), "LINE NUMBER".center(20))
	print "----------------------------------------------------------------------------------------------"
	token = ""
	try:
		while(token != "<EOF>"):
			token = lexicalAnalyzer.getNextToken()
			print "|%s|%s|%s|" % (str(lexicalAnalyzer.getCurrentLexeme()).center(35), str(token).center(35), str(lexicalAnalyzer.getCurrentLine()).center(20))
	except LexError as e:
		print e
	print "----------------------------------------------------------------------------------------------"	
	