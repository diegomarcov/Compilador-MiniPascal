# -*- coding: utf-8 -*-
import re,io,argparse
from shlex import shlex

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = io.BufferedReader(io.FileIO(args.inputFile))
	outputFile = args.outputFile

	#if outputFile == None:
		#output = sys.stdout
		##print "\n\nStarting file lexical analysis...\n\n"
	#else:
		#try:
			#output = open(outputFile, 'w')
			##prinqq"\n\nStarting file lexical analysis... results will be written to %s\n\n" % outputFile
		#except:
			#print "Error"
		
	lex =shlex(inputFile)
	lex.wordchars += "<>"
	lex.commenters = "#"
	noTerm = set([])
	term = set([])
	s='$'
	termre = re.compile('^<[A-Z_]*>')
	notermre = re.compile('^<[a-z_]*>')
	while s!='':
		s = lex.get_token()
		print s
		if termre.match(s):
			term.add(s)
		elif notermre.match(s):
			noTerm.add(s)
	#print noTerm
	