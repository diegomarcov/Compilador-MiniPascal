import sys
import argparse, io
sys.path.append('../entrega2/')
from lexan import LexAn,LexError

#esto fue creado para tener un "archivo" que no escriba nada, para no tener que hacer siempre un if en los writes de debug
class VortexWriter(): # nombre sumamente cambiable
	def write(self,s):
		pass
		
class SynError (Exception):

	def __init__(self,leader,expected,found):
		super(SynError,self).__init__()
		self.leader = leader
		self.expected = expected
		self.found = found
		
	def __str__(self):
		return '\n%sSyntactical Error: Expecting %s, but a %s was found' % (self.leader,self.expected,self.found)

		
class UnexpectedTokenError(Exception):

	def __init__(self,leader,found):
		super(UnexpectedTokenError,self).__init__()
		self.leader = leader
		self.found = found
		
	def __str__(self):
		return '\n%sUnexpected token "%s" found.\n' % (self.leader, self.found)
		
class SynAn():
	def __init__(self,lexer,debug,outputFile):
		self.lexer = lexer
		
		self.debug = bool(debug)
		
		if self.debug:
			self.out = outputFile
		else:
			self.out = VortexWriter()
		
	def execute(self):
		return self.program()

	def program(self):
		self.out.write('In program\n')
		self.program_heading()
		self.block()
		if self.lexer.getNextToken() == '<END_PROGRAM>':
			self.out.write('Success\n')
			return 'The program is syntactically correct.'
		else:
			self.thiserrorLeader = self.lexer.errorLeader()
			self.thislexeme = self.lexer.getCurrentLexeme()
			print self.thiserrorLeader
			print self.thislexeme
			self.synErr('.')
			
			raise self.currentError

	def program_heading(self):
		self.out.write('In program_heading\n')
		if self.lexer.getNextToken() == '<PROGRAM>':
			if self.lexer.getNextToken() == '<IDENTIFIER>':
				if self.lexer.getNextToken() == '<SEMI_COLON>':
					self.out.write('program_heading succeeded\n')
				else:
					self.synErr(';')
			else:
				pass

	def block(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<CONST>":
			self.pushLexeme()
			self.constant_definition_part()
			self.block_cons_rest()
		else:
			self.pushLexeme()
			self.block_cons_rest()
			
		# or self.currentToken == "<VAR>" or self.currentToken == "<PROCEDURE>" or self.currentToken == "<FUNCTION>":

	def block_cons_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<TYPE>":
			self.pushLexeme()
			self.type_definition_part()
			self.block_type_rest()
		else:
			self.pushLexeme()
			self.block_type_rest()
	
	def block_type_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<VAR>":
			self.pushLexeme()
			self.variable_definition_part()
			self.block_var_rest()
		else:
			self.pushLexeme()
			self.block_var_rest()

	def block_var_rest(self):
		self.currentToken = self.lexer.getNextToken()
		# en este caso controlo si viene el <statement_part> porque es mas sencillo
		if self.currentToken == "<BEGIN>":
			self.pushLexeme()
			self.statement_part()
		else:
			self.pushLexeme()
			self.procedure_and_function_declaration_part()
			self.statement_part()

	def constant_definition_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<CONST>":
			self.constant_definition()
			self.constant_definition_rest()
		else:
			self.synErr('const')


	def constant_definition_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.constant_definition_rest_rest()
		else:
			self.synErr(';')

	def constant_definition_rest_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.constant_definition()
			self.constant_definition_rest()
		else:
			self.pushLexeme()
			
	def constant_definition(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<EQUAL>":
				self.constant()
			else:
				self.synErr('=')
		else:
			self.synErr('identifier')
		
	def constant(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>" or self.currentToken == "<IDENTIFIER>" or self.currentToken == "<CHAR>":
			self.out.write("\nFound constant declaration succesfully!\n")
		elif self.currentToken == "<ADD_OP>" or self.currentToken == "<MINUS_OP>":
			self.pushLexeme()
			self.sign()
			self.constant_rest()
		else:
			self.synErr('number, identifier or char')
			
	def constant_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>" or self.currentToken == "<IDENTIFIER>":
			self.out.write("\nFound constant declaration succesfully!\n")
		else:
			self.synErr('number or identifier')

	def sign(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<ADD_OP>" or self.currentToken == "<MINUS_OP>":
			pass
		else:
			self.synErr('sign')

	def type_definition_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<TYPE>":
			self.type_definition()
			self.type_definition_rest()
		else:
			self.synErr('type')

	def type_definition_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.type_definition_rest_rest()
		else:
			self.synErr(';')

	def type_definition_rest_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.type_definition()
			self.type_definition_rest()
		else:
			# si no es un IDENTIFIER es <LAMBDA>, asi que no hacemos nada, simplemente devolvemos el lexema
			self.pushLexeme()

	def type_definition(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.currentToken == self.lexer.getNextToken()
			if self.currentToken == "<EQUAL>":
				self.type()
			else:
				self.synErr('=')
		else:
			self.synErr('identifier')

	def type(self):
		self.currentToken = self.lexer.getNextToken()
		#en este caso me resulta mas sencillo preguntar si es STRUCTURED TYPE
		if self.currentToken == "<ARRAY>":
			self.pushLexeme()
			self.structured_type()
		else:
		#asumo que si no vino un token ARRAY, se viene un tipo simple...
		#posiblemente este descartando casos de error!!!
			self.pushLexeme()
			self.simple_type()
		
	def simple_type(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
				self.constant()
			else:
				self.synErr('..')
		elif self.currentToken == "<CHAR>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
				self.constant()
			else:
				self.synErr('..')
		elif self.currentToken == "<ADD_OP>" or self.currentToken == "<MINUS_OP>":
			self.pushLexeme()
			self.sign()
			self.subrange_type_rest()
		elif self.currentToken == "<IDENTIFIER>":
			self.simple_type_rest()
		else: self.synErr('simple type')

	def simple_type_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SUBRANGE_SEPARATOR>":
			self.constant()
		else:
		#lambda
			self.pushLexeme()

	def subrange_type_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
				self.constant()
			else:
				self.synErr('..')
		elif self.currentToken == "<IDENTIFIER>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
				self.constant()
			else:
				self.synErr('..')
		else: self.synErr('subrange declaration')
			

	def structured_type(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<ARRAY>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<OPEN_BRACKET>":
				self.simple_type()
				self.currentToken = self.lexer.getNextToken()
				if self.currentToken == "<CLOSE_BRACKET>":
					self.currentToken = self.lexer.getNextToken()
					if self.currentToken == "<OF>":
						self.simple_type()
					else:
						self.synErr('of')
				else:
					self.synErr(']')
			else:
				self.synErr('[')
		else:
			self.synErr('array')

	def variable_definition_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<VAR>":
			self.variable_declaration()
			self.variable_declaration_part_rest()
		else:
			self.synErr('VAR')

	def variable_declaration_part_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.variable_declaration_rest_rest()
		else:
			self.synErr(';')

	def variable_declaration_rest_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.variable_declaration()
			self.variable_declaration_rest()
		else:
		#lambda
			self.pushLexeme()

	def variable_declaration(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.variable_declaration_rest()
		else:
			self.synErr('identifier')

	def variable_declaration_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<COMMA>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.variable_declaration_rest()
			else:
				self.synErr('identifier')
		elif self.currentToken == "<TYPE_DECLARATION>":
			self.type()
		else:
			self.synErr(', or :')

	def procedure_and_function_declaration_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<PROCEDURE>" or self.currentToken == "<FUNCTION>":
			self.pushLexeme()
			self.procedure_or_function_declaration_part()
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SEMI_COLON>":
				self.procedure_and_function_declaration_part()
			else:
				self.synErr(';')
		else:
			pass#lambda

	def procedure_or_function_declaration_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<PROCEDURE>":
			self.pushLexeme()
			self.procedure_declaration()
		elif self.currentToken == "<FUNCTION>":
			self.pushLexeme()
			self.function_declaration()
		else:
			self.synErr('function or procedure')		
		
	def procedure_declaration(self):
		self.procedure_heading()
		self.block()

	def procedure_heading(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<PROCEDURE>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.procedure_heading_rest()
			else:
				self.synErr('identifier')
		else:
			self.synErr('procedure')

	def procedure_heading_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.out.write('\nSuccesfully recognised procedure heading!\n')
		elif self.currentToken == "<OPEN_PARENTHESIS>":
			self.formal_parameter_section()
			self.formal_parameter_rest()
		else:
			self.synErr('; or (')

	def formal_parameter_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.formal_parameter_section()
			self.formal_parameter_rest()
		elif self.currentToken == "<CLOSE_PARENTHESIS>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SEMI_COLON>":
				self.out.write('\nSuccesfully recognised procedure heading!\n')
			else:
				self.synErr(';')
		else:
			self.synErr('; or )')
				
	def formal_parameter_section(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<VAR>":
			self.parameter_group()
		else:
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.pushLexeme()
				self.parameter_group()
			else:
				self.synErr('parameter group')

	def parameter_group(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.parameter_group_rest()
		else:
			self.synErr('parameter group')

	def parameter_group_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<COMMA>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.parameter_group_rest()
			else:
				# quizas este error se podria mejorar con algo como "current lexeme no es un parametro valido"
				self.synErr('identifier')
		elif self.currentToken == "<TYPE_DECLARATION>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.out.write('\nSuccesfully recognised parameter group')
			else:
				# si bien el token es IDENTIFIER, lo que se espera en este caso es un DATA TYPE
				self.synErr('valid data type')
		else:
			self.synErr(', or :')
		
	def function_declaration(self):
		self.function_heading()
		self.block()

	def function_heading(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<FUNCTION>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.function_heading_rest()
			else:
				self.synErr('identifier')
		else:
			self.synErr('function')

	def function_heading_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<TYPE_DECLARATION>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.currentToken = self.lexer.getNextToken()
				if self.currentToken == "<SEMI_COLON>":
					self.out.write('\nSuccesfully recognised function heading!\n')
				else:
					self.synErr(';')
			else:
				#este error se podria cambiar por "VALID DATA TYPE"
				self.synErr('identifier')
		elif self.currentToken == "<OPEN_PARENTHESIS>":
			self.formal_parameter_section()
			self.formal_parameter_function_rest()
		else:
			self.synErr(': or )')

	def formal_parameter_function_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.formal_parameter_section()
			self.formal_parameter_function_rest()
		elif self.currentToken == "<CLOSE_PARENTHESIS>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<TYPE_DECLARATION>":
				self.currentToken = self.lexer.getNextToken()
				if self.currentToken == "<IDENTIFIER>":
					self.currentToken = self.lexer.getNextToken()
					if self.currentToken == "<SEMI_COLON>":
						self.out.write('\nSuccesfully recognised parameter group!\n')
					else:
						self.synErr(';')
				else:
					#este error se podria cambiar por "VALID DATA TYPE"
					self.synErr('identifier')
			else:
				self.synErr(':')
		else:
			self.synErr('; or )')

	def statement_part(self):
		self.out.write('In statement_part\n')
		if self.lexer.getNextToken() == '<BEGIN>':
			self.statement_part_rest()
		else:
			raise SysAn(self.lexer.errorLeader(),"begin",self.lexer.currentLexeme())

	def statement_part_rest(self):
		self.out.write('In statement_part\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token=='<SEMI_COLON>' or token=='<END>':
			self.statement_rest()
		else:
			statement()
			statement_rest()

	def statement_rest(self):
		self.out.write('In statement_rest\n')
		token=self.lexer.getNextToken()
		if token=='<SEMI_COLON>':
			self.statement_rest_rest()
		elif token=='<END>':
			self.out.write('statement_rest is finished')
		else:
			raise self.synErr(';" or "end')

	def statement_rest_rest(self):
		self.out.write('In statement_rest_rest\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token=='<SEMI_COLON>' or token=='<END>':
			self.statement_rest_rest()
		else:
			self.statement()
			self.statement_rest()

	def statement(self):
		self.out.write('In statement\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token=='<IDENTIFIER>':
			self.simple_statement_rest()
		else:
			self.synErr('identifier')

	def simple_statement(self):
		self.out.write('In simple_statement\n')
		token=self.lexer.getNextToken()
		
		if token=='<IDENTIFIER>' :
			self.simple_statement()
		else:
			self.structured_statement()

	def simple_statement_rest(self):
		self.out.write('In simple_statement_rest\n')
		token=self.lexer.getNextToken()
		
		if token=='<ASSIGNMENT>' :
			self.expression()
		elif token=='<OPEN_BRACKET>' :
			self.expression()
			if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
				if self.lexer.getNextToken()=='<ASSIGNMENT>':
					self.expression()
				else:
					raise synErr(':=')
			else:
				raise synErr(']')
		elif token=='<OPEN_PARENTHESIS>' :
			self.expression()
		else:
			self.out.write('push lexeme\n')
			self.pushLexeme()

	def component_variable(self):
		self.out.write('In component_variable\n')
		token=self.lexer.getNextToken()
		if token=='<IDENTIFIER>': 
			if self.lexer.getNextToken()=='<OPEN_BRACKET>':
				self.expression()
				if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
					self.out.write('component_variable is finished\n')
				else:
					raise synErr(']')
			else:
				raise synErr('[')
		else:
			raise synErr('identifier')

	def expression(self):
		self.out.write('In expression\n')
		self.simple_expression()
		self.expression_rest()

	def expression_rest(self):
		self.out.write('In expression_rest\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token in ('<LESS_OP>','<LESS_EQUAL_OP>','<GREATER_OP>','<GREATER_EQUAL_OP>','<EQUAL>'):
			self.relational_operator()
			self.simple_expression
		else:
			pass #lambda

	def simple_expression(self):
		self.out.write('In simple_expression\n')
		token=self.lexer.getNextToken()
		self.out.write('In simple_expression\n')
		self.pushLexeme()
		if token in ('<ADD_OP>','<MINUS_OP>'):
			self.sign()
			self.term()
			self.simple_expression_other()
		else:
			self.term()
			self.simple_expression_other()

	def simple_expression_other(self):
		self.out.write('In simple_expression_other\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token in ('<ADD_OP>','<MINUS_OP>','<OR_LOGOP>'):
			self.adding_operator()
			self.term()
			self.simple_expression_other()
		else:
			pass #lambda

	def term(self):
		self.out.write('In term\n')
		self.factor()
		self.term_other()
		
	def term_other(self):
		self.out.write('In term_other\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token in ('<MULTIPLY_OP>','<DIV_OP>','<AND_LOGOP>'):
			self.multiplying_operator()
			self.factor()
			self.term_other()
		else:
			pass #lambda

	def factor(self):
		self.out.write('In factor\n')
		token=self.lexer.getNextToken()
		if token=='<IDENTIFIER>':
			self.factor_rest()
		elif token=='<NUMBER>':
			self.out.write('factor is finished\n')
		elif token=='<OPEN_PARENTHESIS>':
			self.expression()
			if self.lexer.getNextToken()=='<CLOSE_PARENTHESIS>':
				self.out.write('factor is finished\n')
			else:
				raise synErr(')')
		elif token=='<NOT_LOGOP>':
			self.factor()
		elif token=='<CHAR>':
			self.out.write('factor is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.currentLexeme())

	def factor_rest(self):
		self.out.write('In factor_rest\n')
		token=self.lexer.getNextToken()
		if token=='<OPEN_BRACKET>':
			self.expression()
			if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
				self.out.write('factor_rest is finished\n')
		elif token=='<OPEN_PARENTHESIS>':
			self.actual_parameter()
		else:
			self.pushLexeme() #lambda

	def actual_parameter(self):
		self.out.write('In actual_parameter\n')
		self.expression()

	def actual_parameter_rest(self):
		self.out.write('In actual_parameter_rest\n')
		token=self.lexer.getNextToken()
		if token=='<COMMA>':
			self.actual_parameter()
			self.actual_parameter_rest()
			
		elif token=='<CLOSE_PARENTHESIS>':
			self.out.write('actual_parameter_restis finished\n')
		else:
			raise synErr(')')

	def multiplying_operator(self):
		self.out.write('In multiplying_operator\n')
		token=self.lexer.getNextToken()
		if token in ('<MULTIPLY_OP>','<DIV_OP>','<AND_LOGOP>'):
			self.out.write('multiplying_operator is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.currentLexeme())

	def adding_operator(self):
		self.out.write('In adding_operator\n')
		token=self.lexer.getNextToken()
		if token in ('<ADD_OP>','<MINUS_OP>','<OR_LOGOP>'):
			self.out.write('adding_operator is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.currentLexeme())

	def relational_operator(self):
		self.out.write('In relational_operator\n')
		token=self.lexer.getNextToken()
		if token in ('<LESS_OP>','<LESS_EQUAL_OP>','<GREATER_OP>','<GREATER_EQUAL_OP>','<EQUAL>'):
			self.out.write('relational_operator is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.currentLexeme())

	def procedure_statement(self):
		self.out.write('In procedure_statement\n')
		token=self.lexer.getNextToken()
		if token == '<IDENTIFIER>':
			self.procedure_statement_rest()
		else:
			raise synErr('identifier')

	def procedure_statement_rest(self):
		self.out.write('In procedure_statement_rest\n')
		token=self.lexer.getNextToken()
		if token == '<OPEN_PARENTHESIS>':
			self.actual_parameter()
			self.actual_parameter_restactual_parameter()
		else:
			self.pushLexeme()

	def structured_statement(self):
		self.out.write('In structured_statement\n')
		token=self.lexer.getNextToken()
		if token == '<BEGIN>':
			self.structured_statement_other()
			self.conditional_statement()
		else:
			self.pushLexeme()
			self.repetitive_statement()

	def structured_statement_other(self):
		self.out.write('In structured_statement_other\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token in ('<SEMI_COLON>','<END>'):
			self.statement_rest()
		else:
			self.statement()
			self.statement_rest()

	def conditional_statement(self):
		self.out.write('In conditional_statement\n')
		token=self.lexer.getNextToken()

		if token =='<IF>':
			self.expression()
			if self.lexer.getNextToken() =='<THEN>':
				self.statement()
				self.conditional_statement_rest()
			else:
				raise synErr('then')
		else:
			raise synErr('if')

	def conditional_statement_other(self):
		self.out.write('In conditional_statement_other\n')
		token=self.lexer.getNextToken()
		if token =='<ELSE>':
			self.statement()
		else:
			self.pushLexeme()


	def repetitive_statement(self):
		self.out.write('In repetitive_statement\n')
		token=self.lexer.getNextToken()

		if token =='<WHILE>':
			self.expression()
			if self.lexer.getNextToken() =='<DO>':
				self.repetitive_statement_rest()
				
			else:
				raise synErr('do')
		else:
			raise synErr('while')

	def repetitive_statement_rest(self):
		self.out.write('In repetitive_statement_rest\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token in('<BEGIN>','<WHILE>','<IF>','<IDENTIFIER>'):
			self.statement()
		else:
			pass #lambda
		
	def synErr(self,s):
		return SynError(self.lexer.errorLeader(),s,self.lexer.currentLexeme())
		
	def pushLexeme(self):
		self.lexer.pushLexeme(self.out)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')
	parser.add_argument('-d', help='Debug mode',action='store_const', const=True, dest='debug')

	args = parser.parse_args()
	inputFile = io.BufferedReader(io.FileIO(args.inputFile))
	outputFile = args.outputFile
	
	if outputFile == None:
		output = sys.stdout
		print "\n\nStarting file lexical and syntactical analysis...\n\n"
	else:
		try:
			output = open(outputFile, 'w')
			print "\n\nStarting file lexical and syntactical analysis... results will be shown right here, and be written to %s\n\n" % outputFile
		except:
			print "Error: The file %s could not be opened for writing" % outputFile
			
	lexicalAnalyzer = LexAn(inputFile,args.inputFile)
	syntacticalAnalyzer = SynAn(lexicalAnalyzer,args.debug,output)
	try:
		msg = syntacticalAnalyzer.execute()
		if output is not None:
			output.write(msg)
		print msg
	except SynError as e:
		output.write(str(e))
	except UnexpectedTokenError as e:
		output.write(str(e))
	except LexError as e:
		output.write(str(e))
