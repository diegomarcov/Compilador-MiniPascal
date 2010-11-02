#esto fue creado para tener un "archivo" que no escriba nada, para no tener que hacer siempre un if en los writes de debug
class VortexWriter(): # nombre sumamente cambiable
	def write(self,s):
		pass
		
class SynError(Exception):

	def __init__(self,leader,expected="",found="",msg=""):
		super(SynError,self).__init__()
		self.msg="\n%sSyntactical error found:" % leader
		if msg=="":
			# self.leader = leader
			# self.expected = expected
			# if found == '':
				# self.found = 'EOF'
			# else:
				# self.found = found
			self.msg += 'Expecting %s, but "%s" was found' % (self.leader,self.expected,self.found)
		else:
			self.msg += msg
		
	def __str__(self):
		# return '\n%sSyntactical error found: Expecting %s, but "%s" was found' % (self.leader,self.expected,self.found)
		return self.msg

		
class UnexpectedTokenError(Exception):

	def __init__(self,leader,found):
		super(UnexpectedTokenError,self).__init__()
		self.leader = leader
		if found == '':
			self.found = 'EOF'
		else:
			self.found = found
		
	def __str__(self):
		return '\n%sUnexpected token: "%s" found.\n' % (self.leader, self.found)