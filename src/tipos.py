# -*- coding: utf-8 -*-
# toda la herencia de tipos

class Elemento(object): #todos los elementos que pueden aparecer como tipo de un attr en la tabla de simbolos
	def __init__(self):
		super(Elemento,self).__init__()
	
	def instancia(self,tipo):
		return isinstance(self,tipo)
		
	def strExtendido(self):
		return str(self)

class Tipo(Elemento):
	#nombre: el nombre del tipo
	#tamanio: cantidad de locaciones de memoria que ocupa	
	def __init__(self):
		super(Tipo,self).__init__()
		self.imprimible = False
	
class Simple(Tipo):
	def __init__(self):
		super(Simple,self).__init__()
		self.tamanio = 1	

	def getRange(self):
		return self.getUpper() - self.getLower() + 1
		
class Caracter(Simple):
	def __init__(self):
		super(Caracter,self).__init__()
		self.imprimible = True
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubCaracter
		
	def __str__(self):
		return "Character"
		
	def getLower(self):
		return 0
		
	def getUpper(self):
		return 255
	
class Entero(Simple):
	def __init__(self):
		super(Entero,self).__init__()
		self.imprimible = True
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubEntero
		
	def __str__(self):
		return "Integer"
		
	def getLower(self):
		return -32768
		# return -2147483648
		
	def getUpper(self):
		return 32767
		# return 2147483647
	
		
class Booleano(Simple):
	def __init__(self):
		super(Booleano,self).__init__()
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubBooleano
		
	def __str__(self):
		return "Boolean"
		
	def getLower(self):
		return 0
		
	def getUpper(self):
		return 1
	
	
class Subrango(Simple):
	#upperBound y lowerBound
	def __init__(self, lowerBound, upperBound):
		super(Subrango,self).__init__()
		self.lowerBound = lowerBound
		self.upperBound = upperBound
		
	def checkValue(self,value): #obviamente esta de onda este metodo
		return (value < self.upperBound) and (value > self.lowerBound)
		
	def getLower(self):
		return self.lowerBound.valor
		
	def getUpper(self):
		return self.upperBound.valor
		
class SubCaracter(Subrango,Caracter): #herencia múltiple troska
	def __init__(self, lowerBound, upperBound):
		Subrango.__init__(self, lowerBound, upperBound)
		self.imprimible = True
		
	def __str__(self):
		return "Character subrange from '%s' to '%s'" %(self.lowerBound.valor,self.upperBound.valor)
		
	def getLower(self):
		return ord(self.lowerBound.valor)
		
	def getUpper(self):
		return ord(self.upperBound.valor)
		
class SubEntero(Subrango,Entero):
	def __init__(self,lowerBound, upperBound):
		Subrango.__init__(self, lowerBound, upperBound)
		self.imprimible = True
		
	def __str__(self):
		return "Integer subrange from %s to %s" % (self.lowerBound.valor,self.upperBound.valor)
		
class SubBooleano(Subrango,Booleano):
	def __init__(self, lowerBound, upperBound):
		Subrango.__init__(self,lowerBound, upperBound)
		
	def __str__(self):
		return "Boolean subrange from %s to %s" % (self.lowerBound.valor,self.upperBound.valor)
		
class Estructurado(Tipo):
	def __init__(self):
		Tipo.__init__(self)
	
class Arreglo(Estructurado):
	#indexType: tipo del indice
	#elementType: tipo de los elementos
	def __init__(self,tamanio,indexType,elementType):
		Estructurado.__init__(self)
		self.tamanio=tamanio
		self.indexType = indexType
		self.elementType = elementType
		
	def __str__(self):
		return "%s Array" % str(self.elementType)
		
	def strExtendido(self):
		return "Array [%s] of %s" %(self.indexType,self.elementType)
		
class Procedimiento(Elemento): #no puse que hereda de tipo porque no es un tipo
	#params:lista de parametros (son tipos)
	def __init__(self,label=None,params=None):
		Elemento.__init__(self)
		if not params:
			params = []
		self.label = label
		self.params = params
		
	def __str__(self):
		return "Procedure"
		
	def strExtendido(self):
		aux = "Procedure("
		for x in self.params:
			aux+= str(x[1]) + ","
		return aux + ")"
	
	def tamanioParams(self):
		aux = 0
		for x in self.params:
			if x[2]: #por Referencia
				aux += 1
			else:
				aux += x[1].tamanio
		return aux
			
		
class Funcion(Procedimiento):
	#ret:tipo que devuelve
	def __init__(self,label,params,ret):
		Procedimiento.__init__(self,label,params)
		self.ret = ret
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or self.ret==tipo
		
	def __str__(self):
		return ret + " Function"
		
	def strExtendido(self):
		aux = "Funcion("
		for x in self.params:
			aux+= str(x[1]) + ","

		return aux + "): %s" %self.ret
	
class Programa(Elemento):#no puse que hereda de tipo porque no es un tipo
	def __str__(self):
		return "Program identifier"
		
class Attr:
	def __init__(self,tipo,clase, valor=None, pos=None, used = None):
		self.valor=valor
		#valor: puede ser el valor de la constante... o el lugar fisico donde se encontrara
		self.tipo=tipo
		#tipo: objeto de clase tipo con el tipo del valor
		self.clase=clase
		#clase: atributo que define si el identificador es un "type", una "variable", "function", "procedure" o "constant". Agregué tambien subexpresion, para cuando solo se trata de un valor que viene en una expresion
		self.pos = pos
		#pos: el numero de identificador de una variable en el programa o procedimiento actual
		self.used = used
		#used: si fue asignado alguna vez
		
	def __str__(self):
		aux = "value: " + str(self.valor) + ", type: " + self.tipo.strExtendido() + ",class:" + self.clase + ", pos: " + str(self.pos) 
		if self.tipo.instancia(Procedimiento):
			aux+= ", tamanioParams: "+ str(self.tipo.tamanioParams())
		return aux
		
class Ref:
	#clase utilizada para pasar variables por referencia (o sea, serán utilizadas para pasar atributos sintetizados)
	def __init__(self,ref=None):
		self.ref = ref

if __name__ == '__main__':
	#testeo de la herencia
	# print "hola"
	# caracter = Caracter()
	# print "tamaño caracter", caracter.tamanio
	# subCaracter = SubCaracter()
	# print "tamaño subcaracter", subCaracter.tamanio
	# print "caracter instancia de subcaracter", caracter.instancia(SubCaracter)
	# print "subcaracter instancia de caracter", subCaracter.instancia(Caracter)

	# print "caracter es tipo simple", caracter.instancia(Simple)
	# print "subcaracter es tipo estructurado", subCaracter.instancia(Estructurado)
	# arreglo = Arreglo(3,caracter,subCaracter)
	# print "arreglo es de tipo estructurado", arreglo.instancia(Estructurado)
	# print "tamaño arreglo", arreglo.tamanio
	# proc = Procedimiento([])
	# print "procedimiento es simple",proc.instancia(Simple)
	# funcion = Funcion([],Entero)
	# print "funcion es tipo", funcion.instancia(Tipo)
	# print "funcion devuelve", str(funcion.ret)
	# print "funcion compatible con entero", funcion.instancia(Entero)
	int = Entero()
	print type(Entero()) == Entero
