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
	
class Subrango(Simple):
	#upperBound y lowerBound
	def __init__(self):
		Simple.__init__(self)
		
	def checkValue(self,value): #obviamente esta de onda este metodo
		return (value < self.upperBound) and (value > self.lowerBound)
		
class SubCaracter(Subrango,Caracter):
	def __init__(self):
		Simple.__init__(self)
		
	def __str__(self):
		return "Character subrange"
		
class SubEntero(Subrango,Entero):
	def __init__(self):
		Simple.__init__(self)
		
	def __str__(self):
		return "Integer subrange"
		
class SubBooleano(Subrango,Booleano):
	def __init__(self):
		Simple.__init__(self)
		
	def __str__(self):
		return "Boolean subrange"
		
class Estructurado(Tipo):
	pass
	
class Arreglo(Estructurado):
	#index: tipo del indice
	#element: tipo de los elementos
	def __init__(self,tamanio,index,element):
		self.tamanio=tamanio
		self.index = index
		self.element = element
		
	def __str__(self):
		return "Array"
		
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
		return ret
	
class Program(Elemento):#no puse que hereda de tipo porque no es un tipo
	def __str__(self):
		return "Program identifier"
		
class Attr:
	
	def __init__(self,valor,tipo,clase):
		self.valor=valor
		#valor: puede ser el valor de la constante... o el lugar fisico donde se encontrara
		self.tipo=tipos
		#tipo: objeto de clase tipo con el tipo del valor
		self.clase=clase
		#clase:tributo que define si el identificador es un "type", una "variable", "function", "procedure" o "constant". Agregué tambien subexpresion, para cuando solo se trata de un valor que viene en una expresion
		
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
