import re,io

def spacereplace (matchobj):
	return matchobj.group(0).replace(' ','_')

with io.open('ebnf.txt', 'r') as file:
	with io.open('new.txt', 'w') as out:
		string = file.read()
		out.write(re.sub(r'(<[a-z\s ]+>)',spacereplace,string))
