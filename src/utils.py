#esto fue creado para tener un "archivo" que no escriba nada, para no tener que hacer siempre un if en los writes de debug
class VortexWriter(): # nombre sumamente cambiable
	def write(self,s):
		pass
		
class CompilerError(Exception):
	def __init__(self,leader):
		super(CompilerError,self).__init__()
		self.leader = leader
		
	def __str__(self):
		return "\n" + self.leader + self.msg + ".\n"
		
class SynError(CompilerError):
	def __init__(self,leader,expected="",found="",msg=""):
		super(SynError,self).__init__(leader)
		self.msg="Syntactical error found: "
		if msg=="":
			# self.leader = leader
			# self.expected = expected
			# if found == '':
				# self.found = 'EOF'
			# else:
				# self.found = found
			self.msg += 'Expecting %s, but "%s" was found' % (expected,found)
		else:
			self.msg += msg
		
class UnexpectedTokenError(CompilerError):
	def __init__(self,leader,found):
		super(UnexpectedTokenError,self).__init__(leader)
		
		if found == '':
			found = 'EOF'
		self.msg = 'Unexpected token: "%s" found.' % found
		
class SemanticError(CompilerError):
	def __init__(self,leader,msg):
		super(SemanticError,self).__init__(leader)
		self.msg = msg