import re, string
import argparse, io, sys

def corchetes(matchobj):
	return '[' + matchobj.group(0) + matchobj.group(0).upper() + ']'

def regex(matchobj):
	return matchobj.group(1) + re.sub('(.)',corchetes,matchobj.group(2)) + matchobj.group(3)
	


parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
parser.add_argument('inputFile', metavar='IN_FILE', type=file)
parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')
args = parser.parse_args()
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

s = args.inputFile.read()
output.write(re.sub(r'(\{\\ttfamily )(\w+)(\})',regex,s))