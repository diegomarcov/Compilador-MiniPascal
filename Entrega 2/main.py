import sys
import argparse, io
from lexan import LexAn,LexError

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = io.BufferedReader(io.FileIO(args.inputFile))
	outputFile = args.outputFile

	if outputFile == None:
		output = sys.stdout
		print "\n\nStarting file lexical analysis...\n\n"
	else:
		try:
			output = open(outputFile, 'w')
			print "\n\nStarting file lexical analysis... results will be written to %s\n\n" % outputFile
		except:
			print "Error"
		
	lexicalAnalyzer = LexAn(inputFile)
	
	output.write("----------------------------------------------------------------------------------------------\n")
	output.write("|%s|%s|%s|\n" % ("LEXEME".center(35), "TOKEN".center(35), "LINE NUMBER".center(20)))
	output.write("----------------------------------------------------------------------------------------------\n")
	token = ""
	try:
		while(token != "<EOF>"):
			token = lexicalAnalyzer.getNextToken()
			output.write("|%s|%s|%s|\n" % (str(lexicalAnalyzer.getCurrentLexeme()).center(35), str(token).center(35), str(lexicalAnalyzer.getCurrentLine()).center(20)))
	except LexError as e:
		print e
	else:
		output.write("----------------------------------------------------------------------------------------------\n")
		print "\nFinished lexical analysis succesfully!\n\n"
	