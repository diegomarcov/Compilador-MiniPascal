# -*- coding: utf-8 -*-
from tipos import Attr,Booleano,Entero,Caracter,Procedimiento,Funcion
import traceback

class SymbolTableError(Exception):
	def __init__(self,existing,key):
		super(SymbolTableError,self).__init__()
		if existing:
			self.msg = "The key '" + key + "' has already been defined"
		else:
			self.msg = "Undeclared identifier '%s'" % key

class HashStack(list):
	def __init__(self):
		super(HashStack,self).__init__([])
		self.append(
						{
							"true": Attr(valor = 1, tipo = Booleano(), clase = "constant"),
							"false": Attr(valor = 0, tipo = Booleano(), clase = "constant"),
							"integer": Attr(tipo = Entero(), clase = "type"),
							"boolean": Attr (tipo = Booleano(), clase = "type"),
							"char": Attr(tipo = Caracter(), clase = "type"),
							"write": Attr (tipo = Procedimiento(), clase = "procedure"),
							"writeln": Attr (tipo = Procedimiento(), clase = "procedure"),
							"read": Attr (tipo = Procedimiento(), clase = "procedure"),
							"readln": Attr (tipo = Procedimiento(), clase = "procedure"),
							# procedimientos
						}
					)
		
	def top(self):
		return self[-1]
		
	def pop(self):
		return super(HashStack,self).pop()
		
	def push(self):
		self.append({})
		
	def addNewID(self,key,element):
		st = self.top()
		if not (key in st):
			st[key] = element
		else:
			raise SymbolTableError(True,key)
			
	def getGlobalValue(self,key):
		aux = None
		for x in self:
			if key in x:
				aux = x[key]
				break
		if aux == None:
			raise SymbolTableError(False,key)
		return aux
		
	def lastLexicalLevel(self): # cuidado con efectos colaterales... usar siempre debajo de getGlobalValue
		return len(self) + self.index
		
	def getCurrentLexLevel(self):
		return len(self)-1
			
	def __iter__(self):
		self.index = -1
		return self
			
	def next(self):
		try:
			aux = self[self.index]
			self.index -= 1
			return aux
		except IndexError as e:
			raise StopIteration			
		
if __name__ == '__main__':
	stack = HashStack()
	stack.push('asd')
	print(stack.top())
	# print(stack.pop())
	print(str(stack))
	stack.push()
	stack.addNewID("x","ENTERO")
	print(str(stack.top()))
	try:
		stack.addNewID("x","CARACTER")
	except:
		traceback.print_exc()
		
	for x in stack:
		print "elemento:",str(x)
		break
	for x in stack:
		print "elemento:",str(x)
		break
	for x in stack:
		print "elemento:",str(x)
		
	print("todo ok")