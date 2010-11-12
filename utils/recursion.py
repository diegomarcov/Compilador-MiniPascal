# -*- coding: utf-8 -*-
import re,io,argparse,string,sys
from shlex import shlex

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE',type=file, help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = args.inputFile
	outputFile = args.outputFile

	if outputFile == None:
		output = sys.stdout
		#print "\n\nStarting file lexical analysis...\n\n"
	else:
		try:
			output = open(outputFile, 'w')
			#prinqq"\n\nStarting file lexical analysis... results will be written to %s\n\n" % outputFile
		except:
			print "Error"
		
	lex =shlex(inputFile)
	lex.wordchars += "<>"
	lex.commenters = "#"
	noTerm = set([])
	term = set([])
	s='$'
	termre = re.compile('^<[A-Z_]*>')
	notermre = re.compile('^<[a-z_]*>')
	# s = lex.get_token()
	while s!='':
		line = lex.lineno
		s = lex.get_token()
		# print s
		if termre.match(s):
			term.add(s)
			
		elif notermre.match(s):
			print line, lex.lineno, s
			if line != lex.lineno and (lex.lineno%2) ==1:
				output.write("\tdef %s(self):\n\t\tpass\n\n" % s.replace('<','').replace('>',''))
			noTerm.add(s)
		line = lex.lineno
			
	noTerm = list(noTerm)
	# inputFile.seek(0)
	# s = inputFile.read()
	# print s
	# for x in noTerm:
		# producciones = re.search(r'^'+ x + ' ::= (.*)',s,re.MULTILINE).group(1)
		# for y in noTerm[:noTerm.index(x)-1]:
			# print 'no terminal', x 
			
			# listaProd = []
			
			# while producciones!='':
				# matchobj = re.search(r'([<>\w ]*)\|?(.*)', producciones)
				# print 'grupos', matchobj.groups()
				
				# listaProd += [matchobj.group(1)]
				# print 'una produccion', matchobj.group(1)
				# producciones = matchobj.group(2)
				# print 'producciones', producciones, len(producciones)
			# print 'lista' , listaProd
			# for produccion in listaProd:
				# matchobj = re.match(r' ?(<[a-z_]*>)',produccion)
				# if matchobj:
					# if matchobj.group(1) == y:
						# produccionesY = re.search(r'^'+ y + ' ::= (.*)',s,re.MULTILINE).group(1)
						# listaProdY = []
						# while produccionesY!='':
							# matchobj = re.search(r'([<>\w ]*)\|?(.*)', producciones)
							# listaProdY += [matchobj.group(1)]
							# print 'una produccion', matchobj.group(1)
							# produccionesY = matchobj.group(2)

