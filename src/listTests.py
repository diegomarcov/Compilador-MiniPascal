import os
list = os.listdir("./bateria")
casoErroneo = []
casoCorrecto = []
for x in list:
	if x.endswith(".pas"):
		print "\n\n\tpython pycomp.py bateria/%s\n\n" % x
		code = os.system("python pycomp.py bateria/%s" % x)
		if code:
			casoErroneo.append(x)
		else:
			casoCorrecto.append(x)
print "Casos correctos:"		
for x in casoCorrecto:
	while True:
		a = raw_input("comando para %s, o next para sig.-->" % x)
		if a=="next":
			break

		print os.system(a.replace("$$","bateria/"+x)) 
print "Casos erroneos:"		
for x in casoErroneo:
	while True:
		a = raw_input("comando para %s, o next para sig.-->" % x)
		if a=="next":
			break
			
		print os.system(a.replace("$$","bateria/"+x))