# -*- coding: utf-8 -*-
import re,io,argparse
from shlex import shlex

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE',type=file, help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = args.inputFile
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
	noTerm = list(noTerm)
	inputFile.seek(0)
	s = inputFile.read()
	print s
	for x in noTerm:
		# for y in noTerm[:noTerm.index(x)-1]:
			print 'no terminal', x 
			producciones = re.search(r'^'+ x + ' ::= (.*)',s,re.MULTILINE).group(1)
			listaProd = []
			
			while producciones!='':
				matchobj = re.search(r'([<>\w ]*)\|?(.*)', producciones)
				print 'grupos', matchobj.groups()
				
				listaProd += [matchobj.group(1)]
				print 'una produccion', matchobj.group(1)
				producciones = matchobj.group(2)
				print 'producciones', producciones, len(producciones)
			print 'lista' , listaProd
