from utils import CompilerError
import traceback

class SymbolTableError(Exception):
	def __init__(self,existing,key):
		super(SymbolTableError,self).__init__()
		if existing:
			self.msg = "The key " + key + " has already been defined"
		else:
			pass

class HashStack(list):
	def __init__(self):
		list.__init__([])
		
	def top(self):
		return self[-1]
		
	def pop(self):
		return list.pop(self)
		
	def push(self,x={}):
		list.append(self,x)
		
	def addNewID(self,key,element):
		st = self.top()
		if not (key in st):
			st[key] = element
		else:
			raise SymbolTableError(True,key)
			
if __name__ == '__main__':
	stack = HashStack()
	stack.push('asd')
	print(stack.top())
	print(stack.pop())
	print(str(stack))
	stack.push()
	stack.addNewID("x","ENTERO")
	print(str(stack.top()))
	try:
		stack.addNewID("x","CARACTER")
	except:
		traceback.print_exc()
	print("todo ok")