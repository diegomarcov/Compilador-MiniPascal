import argparse
from lexan import LexAn

if __name__ == '__main__':
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
	token = ""
	while(token != "<EOF>"):
		token = lexicalAnalyzer.getNextToken()
		print "%s			%s				%s" % (lexicalAnalyzer.getCurrentLexeme(), token, lexicalAnalyzer.getCurrentLine())