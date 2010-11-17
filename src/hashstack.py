class HashStack(list):
	def __init__(self):
		list.__init__([])
		
	def top(self):
		return self[-1]
		
	def pop(self):
		return list.pop(self)
		
	def push(self,x):
		list.append(self,x)
		
	def addNewID(self,key,element):
		st = self.top()
		if not (key in st):
			st[key] = element
		else:
			pass #errorrrrrrrrrrr
		
if __name__ == '__main__':
	stack = HashStack()
	stack.push('asd')
	print(stack.top())
	print(stack.pop())
	print(str(stack))