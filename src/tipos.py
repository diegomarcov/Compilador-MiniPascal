# -*- coding: utf-8 -*-
# toda la herencia de tipos

class Elemento: #todos los elementos que pueden aparecer como tipo de un attr en la tabla de simbolos
	def instancia(self,tipo):
		return isinstance(self,tipo)

class Tipo(Elemento):
	#nombre: el nombre del tipo
	#tamanio: cantidad de locaciones de memoria que ocupa	
	pass
	
class Simple(Tipo):
	def __init__(self):
		self.tamanio = 1
		
class Caracter(Simple):
	def __init__(self):
		Simple.__init__(self)
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubCaracter
		
	def __str__(self):
		return "Character"
	
class Entero(Simple):
	def __init__(self):
		Simple.__init__(self)
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubEntero
		
	def __str__(self):
		return "Integer"
		
class Booleano(Simple):
	def __init__(self):
		Simple.__init__(self)
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubBooleano
		
	def __str__(self):
		return "Boolean"

	def getRange(self):
		return 2
	
class Subrango(Simple):
	#upperBound y lowerBound
	def __init__(self, lowerBound, upperBound):
		Simple.__init__(self)
		self.lowerBound = lowerBound
		self.upperBound = upperBound
		
	def checkValue(self,value): #obviamente esta de onda este metodo
		return (value < self.upperBound) and (value > self.lowerBound)

	def getRange(self):
		return int(self.upperBound.valor) - int(self.lowerBound.valor) + 1
		
class SubCaracter(Subrango,Caracter): #herencia múltiple troska
	def __init__(self, lowerBound, upperBound):
		Subrango.__init__(self, lowerBound, upperBound)
		
	def __str__(self):
		return "Character subrange from %s to %s" %(self.lowerBound.valor,self.upperBound.valor)
		
class SubEntero(Subrango,Entero):
	def __init__(self,lowerBound, upperBound):
		Subrango.__init__(self, lowerBound, upperBound)
		
	def __str__(self):
		return "Integer subrange from %s to %s" % (self.lowerBound.valor,self.upperBound.valor)
		
class SubBooleano(Subrango,Booleano):
	def __init__(self, lowerBound, upperBound):
		Subrango.__init__(self,lowerBound, upperBound)
		
	def __str__(self):
		return "Boolean subrange from %s to %s" % (self.lowerBound.valor,self.upperBound.valor)
		
class Estructurado(Tipo):
	pass
	
class Arreglo(Estructurado):
	#indexType: tipo del indice
	#elementType: tipo de los elementos
	def __init__(self,tamanio,indexType,elementType):
		self.tamanio=tamanio
		self.indexType = indexType
		self.elementType = elementType
		
	def __str__(self):
		return "Array (index: %s, elements: %s)" % (str(self.indexType),str(self.elementType))
		
class Procedimiento(Elemento): #no puse que hereda de tipo porque no es un tipo
	#params:lista de parametros (son tipos)
	def __init__(self,params):
		self.params = params
		
	def __str__(self):
		return "Procedure"
		
class Funcion(Procedimiento):
	#ret:tipo que devuelve
	def __init__(self,params,ret):
		Procedimiento.__init__(self,params)
		self.ret = ret
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or self.ret==tipo
		
	def __str__(self):
		return ret + " Function"
	
class Programa(Elemento):#no puse que hereda de tipo porque no es un tipo
	def __str__(self):
		return "Program identifier"
		
class Attr:
	
	def __init__(self,tipo,clase, valor=None):
		self.valor=valor
		#valor: puede ser el valor de la constante... o el lugar fisico donde se encontrara
		self.tipo=tipo
		#tipo: objeto de clase tipo con el tipo del valor
		self.clase=clase
		#clase:tributo que define si el identificador es un "type", una "variable", "function", "procedure" o "constant". Agregué tambien subexpresion, para cuando solo se trata de un valor que viene en una expresion
		
	def __str__(self):
		return "value: " + str(self.valor) + ", type: " + str(self.tipo) + ",class:" + self.clase
		
class Ref:
	#clase utilizada para pasar variables por referencia (o sea, serán utilizadas para pasar atributos sintetizados)
	def __init__(self,ref=None):
		self.ref = ref

if __name__ == '__main__':
	#testeo de la herencia
	print "hola"
	caracter = Caracter()
	print "tamaño caracter", caracter.tamanio
	subCaracter = SubCaracter()
	print "tamaño subcaracter", subCaracter.tamanio
	print "caracter instancia de subcaracter", caracter.instancia(SubCaracter)
	print "subcaracter instancia de caracter", subCaracter.instancia(Caracter)

	print "caracter es tipo simple", caracter.instancia(Simple)
	print "subcaracter es tipo estructurado", subCaracter.instancia(Estructurado)
	arreglo = Arreglo(3,caracter,subCaracter)
	print "arreglo es de tipo estructurado", arreglo.instancia(Estructurado)
	print "tamaño arreglo", arreglo.tamanio
	proc = Procedimiento([])
	print "procedimiento es simple",proc.instancia(Simple)
	funcion = Funcion([],Entero)
	print "funcion es tipo", funcion.instancia(Tipo)
	print "funcion devuelve", str(funcion.ret)
	print "funcion compatible con entero", funcion.instancia(Entero)
