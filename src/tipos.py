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
	
class Entero(Simple):
	def __init__(self):
		Simple.__init__(self)
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubEntero
		
class Booleano(Simple):
	def __init__(self):
		Simple.__init__(self)
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or tipo == SubBooleano
	
class Subrango(Simple):
	#upperBound y lowerBound
	def __init__(self):
		Simple.__init__(self)
		
	def checkValue(self,value): #obviamente esta de onda este metodo
		return (value < self.upperBound) and (value > self.lowerBound)
		
class SubCaracter(Subrango,Caracter):
	def __init__(self):
		Simple.__init__(self)
		
class SubEntero(Subrango,Entero):
	def __init__(self):
		Simple.__init__(self)
		
class SubBooleano(Subrango,Booleano):
	def __init__(self):
		Simple.__init__(self)
		
class Estructurado(Tipo):
	pass
	
class Arreglo(Estructurado):
	def __init__(self,tamanio):
		self.tamanio=tamanio
		
class Procedimiento(Elemento): #no puse que hereda de tipo porque no es un tipo
	#params:lista de parametros (son tipos)
	def __init__(self,params):
		self.params = params
		
class Funcion(Procedimiento):
	#ret:tipo que devuelve
	def __init__(self,params,ret):
		Procedimiento.__init__(self,params)
		self.ret = ret
		
	def instancia(self,tipo):
		return isinstance(self,tipo) or self.ret==tipo
	
class Program(Elemento):#no puse que hereda de tipo porque no es un tipo
	pass
	
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
	arreglo = Arreglo(3)
	print "arreglo es de tipo estructurado", arreglo.instancia(Estructurado)
	print "tamaño arreglo", arreglo.tamanio
	proc = Procedimiento([])
	print "procedimiento es simple",proc.instancia(Simple)
	funcion = Funcion([],Entero)
	print "funcion es tipo", funcion.instancia(Tipo)
	print "funcion devuelve", str(funcion.ret)
	print "funcion compatible con entero", funcion.instancia(Entero)
