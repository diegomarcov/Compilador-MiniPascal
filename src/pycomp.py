# -*- coding: utf-8 -*-

import sys
import argparse, io, traceback, re
# sys.path.append('../entrega2/')
from lexer.lexan import LexAn,LexError
from utils import VortexWriter,SynError,UnexpectedTokenError,CompilerError, SemanticError
from tipos import Elemento,Tipo,Simple,Caracter,Entero,Booleano,Subrango,SubCaracter,SubEntero,SubBooleano,Estructurado,Arreglo,Procedimiento,Funcion,Programa,Attr,Ref
from hashstack import HashStack,SymbolTableError
from copy import deepcopy


class SynAn():

	#stStack: pila de tablas de simbolos
	
	def __init__(self,lexer,debug,outputFile,mepa):
		self.lexer = lexer
		self.mepa = mepa
		self.labelIndex = 0
		
		self.relationals = {'<LESS_OP>':'CMME','<LESS_EQUAL_OP>':'CMNI','<GREATER_OP>':'CMMA','<GREATER_EQUAL_OP>':'CMYI','<EQUAL>':'CMIG','<NOT_EQUAL_OP>':'CMDG'}
		self.adding = {'<ADD_OP>':'SUMA','<MINUS_OP>':'SUST','<OR_LOGOP>':'DISJ'}
		self.multiplying = {'<MULTIPLY_OP>':'MULT','<DIV_OP>':'DIVC\nDIVI','<AND_LOGOP>':'CONJ'}
		if debug:
			self.out = outputFile
		else:
			self.out = VortexWriter()
	
	def imprimirST(self,st):
		for x in st:
			self.out.write("\t|%s|%s|\n" % (x.center(20), str(st[x]).center(80)))
		self.out.write("fin tabla\n\n")
			
	def checkTypes(self,tipo1,tipo2):
		return tipo1.instancia(type(tipo2))
			
	def escribir(self, s):
		self.mepa.write('\t\t' + s + '\n')
		
	def ponerLabel(self, label = None):
		if label == None:
			label = "L" + str(self.labelIndex)
		self.mepa.write('%s\t\tNADA\n' % label)
			
	def execute(self):
		try:
			return self.program()
		except SymbolTableError as e:
			raise SemanticError(self.lexer.errorLeader(),e.msg)

	def program(self):
		self.out.write('In program\n')
		
		###########
		self.stStack = HashStack()
		idPrograma = Ref()
		self.out.write("\tSymbol Table Stack: " + str(self.stStack) + "\n")
		self.escribir('INPP')		
		###########
		
		self.program_heading(idPrograma)
		self.block(idPrograma.ref)
		if self.lexer.getNextToken() == '<END_PROGRAM>':
			if self.lexer.getNextToken() == '<EOF>':
				self.out.write('Success\n')
				
				###########
				# finalizar el programa
				self.escribir('PARA')
				###########
				
				return 'The program is syntactically correct.'
			else: 
				raise SynError(self.lexer.errorLeader(),msg="There are characters after the last character ('.')")
		else:
			# self.thiserrorLeader = self.lexer.errorLeader()
			# self.thislexeme = self.lexer.getLexeme()
			self.synErr('"."')

	def program_heading(self,idPrograma):
		self.out.write('In program_heading\n')
		if self.lexer.getNextToken() == '<PROGRAM>':
			if self.lexer.getNextToken() == '<IDENTIFIER>':
			
				#############
				idPrograma.ref = self.lexer.getLexeme()
				self.out.write("\tprogram heading ID: " + idPrograma.ref + "\n")
				#############
				
				if self.lexer.getNextToken() == '<SEMI_COLON>':
					self.out.write('program_heading succeeded\n')
				else:
					self.synErr('";"')
			else:
				raise SynError(self.lexer.errorLeader(), msg="Expecting an identifier but %s was found" % self.lexer.getLexeme())
		else:
			self.synErr('"program"')

	def block(self,idPrograma=None):
		self.out.write('In block\n')
		currentToken = self.lexer.getNextToken()
		
		################		
		self.imprimirST(self.stStack.top())
		self.stStack.push() # agrega por default un diccionario, o sea una tabla de símbolos
		if idPrograma!=None:
			self.stStack.addNewID(idPrograma, Attr(valor=idPrograma,tipo=Programa(),clase="program"))			
			#procedimientos...
		################
		
		self.pushLexeme()
		tamanioVariables =Ref(0)
		if currentToken == "<CONST>":
			self.constant_definition_part()
			self.block_cons_rest(tamanioVariables)
		else:
			self.block_cons_rest(tamanioVariables)
			
		#########
		self.stStack.pop()
		
		#########

	def block_cons_rest(self,tamanioVariables):
		self.out.write('In block_cons_rest\n')
		currentToken = self.lexer.getNextToken()
		if currentToken == "<TYPE>":
			self.pushLexeme()
			self.type_definition_part()
			self.block_type_rest(tamanioVariables)
		else:
			self.pushLexeme()
			self.block_type_rest(tamanioVariables)
			
		###########		
		if tamanioVariables.ref: # si hay variables libero memoria
			self.escribir("LMEM %s" %tamanioVariables.ref)
		###########
	
	def block_type_rest(self,tamanioVariables):
		self.out.write('In block_type_rest\n')
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<VAR>":
			self.pushLexeme()
			self.variable_definition_part(tamanioVariables)
			self.block_var_rest()
		else:
			self.pushLexeme()
			self.block_var_rest()

	def block_var_rest(self):
		self.out.write('In block_var_rest\n')
		self.currentToken = self.lexer.getNextToken()
		# en este caso controlo si viene el <statement_part> porque es mas sencillo
		if self.currentToken == "<BEGIN>":
			self.pushLexeme()
			self.statement_part()
		else:
			self.pushLexeme()	
			
			########
			label = "L%s" % self.labelIndex
			self.labelIndex += 1
			self.escribir("DSVS %s" %label)
			########
			
			self.procedure_and_function_declaration_part()
			
			#######
			self.ponerLabel(label)
			#######
			
			self.statement_part()

	def constant_definition_part(self):
		self.out.write('In constant_definition_part\n')
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<CONST>":
			self.constant_definition()
			self.constant_definition_rest()
		else:
			self.synErr('"const"')


	def constant_definition_rest(self):
		self.out.write('In constant_definition_rest\n')	
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.constant_definition_rest_rest()
		else:
			self.synErr('";"')

	def constant_definition_rest_rest(self):
		self.out.write('In constant_definition_rest_rest\n')	
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.constant_definition()
			self.constant_definition_rest()
		else:
			self.pushLexeme()
			
	def constant_definition(self):
		self.out.write('In constant_definition\n')		
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
		
			#########
			id = self.lexer.getLexeme()
			#########
			
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<EQUAL>":
			
				#########
				attr = Ref()
				self.constant(attr)
				self.stStack.addNewID(id,attr.ref)
				self.out.write("\tConstant: "+id + ": " + str(attr.ref) +" at constant_definition\n")
				self.imprimirST(self.stStack.top())
				#########	
				
			else:
				self.synErr('"="')
		else:
			self.synErr('an identifier')
		
	def constant(self,attr=None): #cambiar!!!!! sacar el None
		self.out.write('In constant\n')	
		self.currentToken = self.lexer.getNextToken()
		
		#################
		if self.currentToken == "<NUMBER>":
			attr.ref = Attr(valor=int(self.lexer.getLexeme()),tipo=Entero(),clase="constant")
			self.out.write("\tInteger constant found: " + str(attr.ref) + "\n")			
		elif self.currentToken == "<IDENTIFIER>":
			attr.ref = self.stStack.getGlobalValue(self.lexer.getLexeme())
			if attr.ref.clase=="constant":
				attr.ref = deepcopy(attr.ref)
				self.out.write("\tConstant %s assigned to constant\n" % self.lexer.getLexeme())
			# elif attr.ref.clase=="variable":
				# attr.ref = Attr(valor = attr.ref.valor,) 
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid assignment: constant expected")
		elif self.currentToken == "<CHAR>":
			attr.ref = Attr(valor = self.lexer.getLexeme()[1],tipo = Caracter(),clase="constant")
			self.out.write("\tCharacter constant found: " + str(attr.ref) + "\n")	
		elif self.currentToken == "<ADD_OP>" or self.currentToken == "<MINUS_OP>":
			self.pushLexeme()
			signValue = Ref()
			self.sign(signValue)
			# attr = Ref()
			self.constant_rest(attr)
			attr.ref.valor = signValue.ref * attr.ref.valor
		################
		
		else:
			self.synErr('a number, identifier or char')
			
	def constant_rest(self,attr):
		self.out.write('In constant_rest\n')	
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>":
			attr.ref = Attr(valor = int (self.lexer.getLexeme()),tipo = Entero(), clase ="constant")
		elif self.currentToken == "<IDENTIFIER>":
			
			###########
			attr.ref = self.stStack.getGlobalValue(self.lexer.getLexeme())
			if attr.ref.clase=="constant":
				if attr.ref.tipo.instancia(Entero):
					attr.ref = deepcopy(attr.ref)
					self.out.write("\tConstant %s assigned to constant\n" % self.lexer.getLexeme())
				else:
					raise SemanticError(self.lexer.errorLeader(), "Can not apply sign operator to " + self.lexer.getLexeme())
			# elif attr.ref.clase=="variable":
				# attr.ref = Attr(valor = attr.ref.valor,) 
			else:
				raise SemanticError(self.lexer.errorLeader(),"Constant value can only be assigned with another constant")
			###########
			
			self.out.write("\nFound constant declaration succesfully!\n")
		else:
			self.synErr('a number or identifier')

	def sign(self,signValue):
		self.currentToken = self.lexer.getNextToken()
		
		###########
		if self.currentToken == "<ADD_OP>": 
			signValue.ref = 1
		elif self.currentToken == "<MINUS_OP>":
			signValue.ref = -1
		##########
		
		else:
			self.synErr('a sign')

	def type_definition_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<TYPE>":
			self.type_definition()
			self.type_definition_rest()
		else:
			self.synErr('"type"')

	def type_definition_rest(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.type_definition_rest_rest()
		else:
			self.synErr('";"')

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
			id = self.lexer.getLexeme()
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<EQUAL>":
			
				##########
				tipo = Ref()
				self.type(tipo)
				self.stStack.addNewID(id, tipo.ref)
				self.imprimirST(self.stStack.top())
				#########
				
			else:
				self.synErr('"="')
		else:
			self.synErr('identifier')

	def type(self,tipo):
		self.out.write('In type\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		#en este caso me resulta mas sencillo preguntar si es STRUCTURED TYPE
		if self.currentToken == "<ARRAY>":
			self.pushLexeme()
			self.structured_type(tipo)
		else:
		#asumo que si no vino un token ARRAY, se viene un tipo simple...
		#posiblemente este descartando casos de error!!!
			self.pushLexeme()
			self.simple_type(tipo)
		
	def simple_type(self,tipo):
		self.out.write('In simple_type\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<NUMBER>":
			number = int(self.lexer.getLexeme())
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
			
				######
				number2 = Ref()
				self.constant(number2)
				if number2.ref.tipo.instancia(Entero):
					if number <= number2.ref.valor:
						tipo.ref = Attr(tipo = SubEntero(Attr(valor = number,tipo = Entero(), clase = "constant"),number2.ref), clase = "type")
					else:
						raise SemanticError(self.lexer.errorLeader(),"Invalid subrange: lower bound must be smaller than upper bound.")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Non compatible subrange bounds (Integer expected, but " + str(number2.ref.tipo) + " found).")
				##########
				
			else:
				self.synErr('".."')
		elif self.currentToken == "<CHAR>":
			char = self.lexer.getLexeme()[1]
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":
				#############
				char2 = Ref()
				self.constant(char2)
				if char2.ref.tipo.instancia(Caracter):
					if char <= char2.ref.valor:
						tipo.ref = Attr(tipo = SubCaracter(Attr(valor = char,tipo = Caracter(), clase = "constant"),char2.ref), clase = "type")
					else:
						raise SemanticError(self.lexer.errorLeader(),"Invalid subrange: lower bound must be smaller than upper bound.")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Non compatible subrange bounds (Character expected, but " + str(char2.ref.tipo) + " found).")
				#############
				
			else:
				self.synErr('".."')
		elif self.currentToken == "<ADD_OP>" or self.currentToken == "<MINUS_OP>":
			self.pushLexeme()
			
			################
			valor = Ref()
			self.sign(valor)
			tipo2 = Ref()
			self.subrange_type_rest(tipo2)
			tipo2.ref.tipo.lowerBound.valor *= valor.ref
			if tipo2.ref.tipo.lowerBound.valor <= tipo2.ref.tipo.upperBound.valor:
				tipo.ref = Attr(tipo = tipo2.ref.tipo, clase = "constant")
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid subrange: lower bound must be smaller than upper bound")
			################
			
		elif self.currentToken == "<IDENTIFIER>":

			#########
			id = self.stStack.getGlobalValue(self.lexer.getLexeme())
			tipo2 = Ref()
			self.simple_type_rest(tipo2)
			if tipo2.ref==None:
				if id.clase == "type":
					tipo.ref = deepcopy(id)
				else:
					raise SemanticError(self.lexer.errorLeader(),"Type expected, but %s found" % id.clase)
			else:
				if tipo2.ref.tipo.instancia(type(id.tipo)):
					if id.valor <= tipo2.ref.tipo.upperBound.valor:
						tipo2.ref.tipo.lowerBound = deepcopy(id)
						tipo.ref = tipo2.ref
					else:
						raise SemanticError(self.lexer.errorLeader(),"Invalid subrange: lower bound must be smaller than upper bound")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Non compatible subrange bounds (%s expected, but %s found)" % (str(id.tipo),str(tipo2)))					
			#########
			
		else: 
			self.synErr('simple type')

	def simple_type_rest(self,attr):
		self.out.write('In simple_type_rest\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<SUBRANGE_SEPARATOR>":

			################
			tipo = Ref()
			self.constant(tipo)
			if tipo.ref.tipo.instancia(Entero):
				attr.ref = Attr(tipo = SubEntero(None,tipo.ref),clase = "type")
			elif tipo.ref.tipo.instancia(Caracter):
				attr.ref = Attr(tipo = SubCaracter(None,tipo.ref),clase = "type")
			else:
				attr.ref = Attr(tipo = SubBooleano(None,tipo.ref),clase = "type")
			################
			
		else:
		#lambda
			self.pushLexeme()

			############
			attr.ref = None
			############

	def subrange_type_rest(self, tipo):
		self.out.write('In subrange_type_rest\n')
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<NUMBER>":
			number = self.lexer.getLexeme()
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":

				##############
				number2 = Ref()
				self.constant(number2)
				if number2.ref.tipo.instancia(Entero):
					tipo.ref = Attr(tipo = SubEntero(lowerBound = Attr(valor = int(number),tipo = Entero(), clase = "constant"),upperBound = number2.ref), clase = "type")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Non compatible subrange bounds (Integer expected, but " + str(number2.ref.tipo) + " found).")
				##############
				
			else:
				self.synErr('".."')
		elif self.currentToken == "<IDENTIFIER>":
			id = self.lexer.getLexeme()
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SUBRANGE_SEPARATOR>":

				###############
				const = self.stStack.getGlobalValue(id)
				if const.clase=="constant":
					attr = Ref()
					self.constant(attr)
					if const.tipo.instancia(Entero):
						if not attr.ref.tipo.instancia(Entero):
							raise SemanticError(self.lexer.errorLeader(),"Non compatible subrange bounds (Integer expected, but " + str(attr.ref.tipo) + " found).")
					else:
						raise SemanticError(self.lexer.errorLeader(),"Integer subrange expected")
					tipo.ref = Attr(tipo = SubEntero(lowerBound = deepcopy(const),	upperBound = attr.ref), clase = "constant")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Constant value expected, but %s identifier found" % const.clase)
				###############
				
			else:
				self.synErr('".."')
		else:
			self.synErr('subrange declaration')
			

	def structured_type(self,tipo):
		self.out.write('In structured_type\n')
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<ARRAY>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<OPEN_BRACKET>":
				tipoIndice = Ref()
				self.simple_type(tipoIndice)
				self.currentToken = self.lexer.getNextToken()
				if self.currentToken == "<CLOSE_BRACKET>":
					self.currentToken = self.lexer.getNextToken()
					if self.currentToken == "<OF>":

						########
						tipoElem = Ref()
						self.simple_type(tipoElem)
						if tipoIndice.ref.tipo.instancia(Subrango) or tipoIndice.ref.tipo.instancia(Booleano):
							if tipoElem.ref.tipo.instancia(Simple):
								tipo.ref = Attr(tipo = Arreglo(tamanio = tipoIndice.ref.tipo.getRange(), indexType=tipoIndice.ref.tipo, elementType=tipoElem.ref.tipo),clase = "type")
							else:
								raise SemanticError(self.lexer.errorLeader(),"Element type of an array must be a simple type, but %s found" % str(tipoElem.ref.tipo))
						else:
							raise SemanticError(self.lexer.errorLeader(),"Index type  of an array must be a subrange or a boolean type, but %s found" % str(tipoIndice.ref.tipo))
						#########
						
					else:
						self.synErr('"of"')
				else:
					self.synErr('"]"')
			else:
				self.synErr('"["')
		else:
			self.synErr('"array"')

	def variable_definition_part(self,tamanioVariables):
		self.out.write('In variable_definition_part\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<VAR>":
			# self.globalVarIndex = 0
			tamanioVariables.ref = 0
			self.variable_declaration(tamanioVariables)
			self.variable_declaration_part_rest(tamanioVariables)
			
			#############
			# self.escribir("RMEM %s" % self.globalVarIndex)
			self.escribir("RMEM %s" % tamanioVariables.ref)
			#############
			
		else:
			self.synErr('"VAR"')

	def variable_declaration_part_rest(self,tamanioVariables):
		self.out.write('In variable_declaration_part_rest\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<SEMI_COLON>":
			self.variable_declaration_rest_rest(tamanioVariables)
		else:
			self.synErr('";"')

	def variable_declaration_rest_rest(self,tamanioVariables):
		self.out.write('In variable_declaration_rest_rest\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.variable_declaration(tamanioVariables)
			self.variable_declaration_part_rest(tamanioVariables)
		else:
		#lambda
			self.pushLexeme()

	def variable_declaration(self,tamanioVariables):
		self.out.write('In variable_declaration\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % self.currentToken)
		if self.currentToken == "<IDENTIFIER>":

			#########
			idList = Ref([self.lexer.getLexeme()])
			tipo = Ref()
			self.variable_declaration_rest(idList,tipo)
			for var in idList.ref:
				# self.stStack.addNewID(var, Attr(pos = self.globalVarIndex ,  clase = "variable", tipo = tipo.ref))
				# self.globalVarIndex += tipo.ref.tamanio
				self.stStack.addNewID(var, Attr(pos = tamanioVariables.ref,  clase = "variable", tipo = tipo.ref))
				tamanioVariables.ref += tipo.ref.tamanio
			self.imprimirST(self.stStack.top())
			# self.escribir("RMEM %s" %len(idList.ref))
			#########
			
		else:	
			self.synErr('an identifier')

	def variable_declaration_rest(self,idList,tipo):
		self.out.write('In variable_declaration_rest\n')
		self.currentToken = self.lexer.getNextToken()
		self.out.write('Current Token == %s\n' % self.currentToken)
		if self.currentToken == "<COMMA>":
			self.currentToken = self.lexer.getNextToken()
			self.out.write('Current token == %s\n' % self.currentToken)
			if self.currentToken == "<IDENTIFIER>":

				#########
				id = self.lexer.getLexeme()
				self.variable_declaration_rest(idList,tipo)
				idList.ref.append(id)
				#########
				
			else:
				self.synErr('an identifier')
		elif self.currentToken == "<TYPE_DECLARATION>":

			#########
			attr = Ref()
			self.type(attr)
			tipo.ref = attr.ref.tipo
			#########
			
		else:
			self.synErr('"," or ":"')

	def procedure_and_function_declaration_part(self):
		self.out.write("In procedure_and_function_declaration_part\n")
		self.currentToken = self.lexer.getNextToken()
		self.out.write("Current token @proc: %s" % self.currentToken)
		if self.currentToken == "<PROCEDURE>" or self.currentToken == "<FUNCTION>":
			self.pushLexeme()
			self.procedure_or_function_declaration_part()
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SEMI_COLON>":
				self.procedure_and_function_declaration_part()
			else:
				self.synErr('";"')
		else:
			#lambda
			self.pushLexeme()

	def procedure_or_function_declaration_part(self):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<PROCEDURE>":
			self.pushLexeme()
			self.procedure_declaration()
		elif self.currentToken == "<FUNCTION>":
			self.pushLexeme()
			self.function_declaration()
		else:
			self.synErr('a function or procedure')		
		
	def procedure_declaration(self):
	
		##########
		self.ponerLabel()
		label = "L%s" % self.labelIndex
		self.labelIndex += 1
		##########
		tamanioParams = Ref()
		self.procedure_heading(label,tamanioParams)
		
		#########
		nivel = self.stStack.getCurrentLexLevel() 
		self.escribir("ENPR %s" % nivel)
		#########
		
		self.block()
		
		#########		
		self.escribir("RTPR %s, %s" % (nivel, tamanioParams.ref))
		#########

	def procedure_heading(self,label,tamanioParams):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<PROCEDURE>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				
				######
				id = self.lexer.getLexeme()
				parameterList = Ref([])
				self.procedure_heading_rest(parameterList)
				attr = Attr(clase ="procedure", tipo = Procedimiento(label,parameterList.ref))
				self.stStack.addNewID(id, attr)
				tamanioParams.ref = attr.tipo.tamanioParams()
				######
				
			else:
				self.synErr('identifier')
		else:
			self.synErr('procedure')

	def procedure_heading_rest(self,parameterList):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
			self.out.write('\nSuccesfully recognised procedure heading!\n')
		elif self.currentToken == "<OPEN_PARENTHESIS>":
		
			#########pa
			parameterList1 = Ref([])
			self.formal_parameter_section(parameterList1)
			parameterList2 = Ref([])
			self.formal_parameter_rest(parameterList2)
			parameterList.ref = parameterList1.ref + parameterList2.ref
			#########
			
		else:
			self.synErr('; or (')

	def formal_parameter_rest(self,parameterList):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<SEMI_COLON>":
		
			########
			parameterList1  =Ref([])
			self.formal_parameter_section(parameterList1)
			parameterList2  =Ref([])
			self.formal_parameter_rest(parameterList2)
			parameterList.ref = parameterList1.ref + parameterList2.ref
			##############
			
		elif self.currentToken == "<CLOSE_PARENTHESIS>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<SEMI_COLON>":
				self.out.write('\nSuccesfully recognised procedure heading!\n')
			else:
				self.synErr('";"')
		else:
			self.synErr(' \";\" or \")\"')
				
	def formal_parameter_section(self,parameterList):
		self.currentToken = self.lexer.getNextToken()
		tipo = Ref()
		parameterList1 = Ref([])
		if self.currentToken == "<VAR>":
			
			self.parameter_group(parameterList1,tipo)

			##########
			for x in parameterList1.ref:
				parameterList.ref.append((x,tipo.ref, True))
			##########
			
		elif self.currentToken == "<IDENTIFIER>":
			self.pushLexeme()
			self.parameter_group(parameterList1,tipo)
			
			##########
			for x in parameterList1.ref:
				parameterList.ref.append((x,tipo.ref, False))
			##########
			
		else:
			self.synErr('a parameter group')

	def parameter_group(self,parameterList,tipo):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<IDENTIFIER>":
			id = self.lexer.getLexeme()
			self.parameter_group_rest(parameterList,tipo)
			
			##########
			parameterList.ref = [id] + parameterList.ref
			##########
			
		else:
			self.synErr('parameter group')

	def parameter_group_rest(self,parameterList,tipo):
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<COMMA>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
			
				############
				id = self.lexer.getLexeme()
				self.parameter_group_rest(parameterList,tipo)
				parameterList.ref = [id] + parameterList.ref
				############
				
			else:
				raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.getLexeme())
		elif self.currentToken == "<TYPE_DECLARATION>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
			
				###########
				identifier = self.stStack.getGlobalValue(self.lexer.getLexeme())
				if identifier.clase == "type":
					tipo.ref = identifier.tipo
				else:
					raise SemanticError(self.lexer.errorLeader(),"Invalid procedure or function heading: Expecting a type identifier")
				###########
				
				self.out.write('\nSuccesfully recognised parameter group')
			else:
				# si bien el token es IDENTIFIER, lo que se espera en este caso es un DATA TYPE
				self.synErr('a type identifier')
		else:
			self.synErr('\",\" or \":\"')
		
	def function_declaration(self):
		self.out.write('In function_declaration\n')
		self.function_heading()
		self.block()

	def function_heading(self):
		self.out.write('In function_heading\n')
		self.currentToken = self.lexer.getNextToken()
		if self.currentToken == "<FUNCTION>":
			self.currentToken = self.lexer.getNextToken()
			if self.currentToken == "<IDENTIFIER>":
				self.function_heading_rest()
			else:
				self.synErr('an identifier')
		else:
			self.synErr('a function')

	def function_heading_rest(self):
		self.out.write('In function_heading_rest\n')
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
				self.synErr('a type identifier')
		elif self.currentToken == "<OPEN_PARENTHESIS>":
			self.formal_parameter_section()
			self.formal_parameter_function_rest()
		else:
			self.synErr('\":\" or \")\"')

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
						self.synErr('";"')
				else:
					#este error se podria cambiar por "VALID DATA TYPE"
					self.synErr('identifier')
			else:
				self.synErr('":"')
		else:
			self.synErr('";" or ")"')
			
	def statement_part(self):
		self.compound_statement()

	def compound_statement(self):
		self.out.write('In statement_part\n')
		if self.lexer.getNextToken() == '<BEGIN>':
			self.statement()
			self.compound_statement_rest()
			if self.lexer.getNextToken() != '<END>':
				self.synErr('"end" or a valid statement')
		else:
			self.synErr('"begin"')

	def compound_statement_rest(self):
		self.out.write('In compound_statement_rest\n')
		token=self.lexer.getNextToken()
		if token=='<SEMI_COLON>':
			self.statement()
			self.compound_statement_rest()
		else:
			self.pushLexeme()
		
	def statement(self):
		self.out.write('In statement\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token=="<BEGIN>" or token=="<IF>" or token =="<WHILE>":
			self.structured_statement()
		else:
			self.simple_statement()

	def simple_statement(self):
		self.out.write('In simple_statement\n')
		token=self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % token)
		if token=='<IDENTIFIER>' :
			self.simple_statement_rest(self.lexer.getLexeme())
		else:
			self.pushLexeme()

	def simple_statement_rest(self, id):
		self.out.write('In simple_statement_rest\n')
		token=self.lexer.getNextToken()
		
		if token=='<ASSIGNMENT>' :
		
			############
			identifier = self.stStack.getGlobalValue(id)
			lexLevel = self.stStack.lastLexicalLevel()
			attr = Ref()
			self.expression(attr)
			if identifier.clase == "variable":
				if self.checkTypes(attr.ref.tipo,identifier.tipo):
					self.escribir("ALVL %s, %s" % (lexLevel, identifier.pos))
				else:
					raise SemanticError(self.lexer.errorLeader(), "Non compatible types in assignment. %s expected, but %s found" % (identifier.tipo, attr.ref.tipo))
			else:
				raise SemanticError(self.lexer.errorLeader(), "Left side of assignment must be a variable")
			############
			
		elif token=='<OPEN_BRACKET>' :
		
			#############
			attr1 = Ref()
			self.expression(attr1)
			array = self.stStack.getGlobalValue(id)
			lexLevel = self.stStack.lastLexicalLevel()
			self.escribir("CONT %s,%s" % (array.tipo.indexType.getLower(),array.tipo.indexType.getUpper()))
			self.escribir("APCT %s" % array.tipo.indexType.getLower())
			self.escribir("SUST")
			#############
			
			if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
				if self.lexer.getNextToken()=='<ASSIGNMENT>':
					
					############
					attr2 = Ref()
					self.expression(attr2)					
					if self.checkTypes(array.tipo.indexType,attr1.ref.tipo):
						if self.checkTypes(array.tipo.elementType, attr2.ref.tipo):
							self.escribir("ALAR %s,%s" % (lexLevel, array.pos))
						else:
							raise SemanticError(self.lexer.errorLeader(),"Non compatible types in assignment. %s expected, but %s found" % (array.tipo.elementType, attr2.ref.tipo))
					else:
						raise SemanticError(self.lexer.errorLeader(), "Non compatible types in assignment. %s expected as index, but %s found" % (array.tipo.indexType, attr1.ref.tipo))
					############
					
				else:
					self.synErr('":="')
			else:
				self.synErr('"]"')
				
		elif token=='<OPEN_PARENTHESIS>':
			
			###############
			proc = self.stStack.getGlobalValue(id)
			nivel = self.stStack.lastLexicalLevel()
			listParams = proc.tipo.params
			if proc.clase == "procedure":
				if nivel==-1:
					self.actual_parameter(id = id)
					self.actual_parameter_rest(id = id)
				else:
					self.actual_parameter(esperado = listParams[0])
					self.actual_parameter_rest(listParams = listParams[1:])
					self.escribir("LLPR %s" %proc.tipo.label)
			else:
				raise SemanticError(self.lexer.errorLeader(), "Invalid statement: %s is not a procedure" % id)
			###############
			
		else:
			#lambda
			self.out.write('push lexeme\n')
			self.pushLexeme()
			
			#######
			proc = self.stStack.getGlobalValue(id)
			nivel = self.stStack.lastLexicalLevel()
			if proc.clase == "procedure":
				if proc.tipo.params==[]:
					self.escribir("LLPR %s" %proc.tipo.label)
				else:
					raise SemanticError(self.lexer.errorLeader(),"Invalid procedure call: %s has %s parameters" % (id,len(proc.tipo.params)))
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid statement: %s is not a procedure" % id)
			#######

	def component_variable(self):
		self.out.write('In component_variable\n')
		token=self.lexer.getNextToken()
		if token=='<IDENTIFIER>': 
			if self.lexer.getNextToken()=='<OPEN_BRACKET>':
				self.expression()
				if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
					self.out.write('component_variable is finished\n')
				else:
					self.synErr('"]"')
			else:
				self.synErr('"["')
		else:
			self.synErr('an identifier')

	def expression(self, attr = None, porRef = None):
		self.out.write('In expression\n')
		
		########
		# attr.ref = Attr(clase="subexpresion", tipo= Entero())
		attr1 = Ref() 
		# sintetizo attr1
		self.simple_expression(attr1,porRef)		
		self.expression_rest(attr1,porRef)
		attr.ref = attr1.ref
		#########

	def expression_rest(self,attr, porRef = None):
		self.out.write('In expression_rest\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		
		if token in self.relationals:
		
			###########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			op = Ref()
			self.relational_operator(op)
			attr1 = Ref()
			self.simple_expression(attr1)
			if attr.ref.tipo.instancia(Simple): #esto nunca va a dar false... ya se chequea en factor_rest
				if self.checkTypes(attr.ref.tipo,attr1.ref.tipo):
					self.escribir(op.ref)
					attr.ref = Attr(clase="subexpression", tipo = Booleano())
				else:
					raise SemanticError(self.lexer.errorLeader(), "Non compatible types in expression: %s and %s" % (attr.ref.tipo, attr1.ref.tipo))
			else:
				raise SemanticError(self.lexer.errorLeader(), "Invalid expression: Simple type expected, but %s found" % attr.ref.tipo)
			##########
			
		else:
			pass #lambda

	def simple_expression(self,attr=None, porRef = None):
		self.out.write('In simple_expression\n')

		#########
		attr1 = Ref()
		self.term(attr1,porRef)
		self.simple_expression_other(attr1,porRef)
		attr.ref = attr1.ref
		#########

	def simple_expression_other(self,attr, porRef = None):
		self.out.write('In simple_expression_other\n')
		token=self.lexer.getNextToken()
		operator = self.lexer.getLexeme()
		self.pushLexeme()
		if token in self.adding:
		
			###########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			op = Ref()
			tipo = Ref()
			self.adding_operator(op,tipo)
			attr1 = Ref()
			self.term(attr1)
			if attr.ref.tipo.instancia(tipo.ref):
				if self.checkTypes(attr.ref.tipo,attr1.ref.tipo):
					self.escribir(op.ref)
				else:
					raise SemanticError(self.lexer.errorLeader(), "Non compatible types in expression: %s and %s" % (attr.ref.tipo, attr1.ref.tipo))
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid expression: Can not apply '%s' operator to %s" % (operator, attr.ref.tipo))
			self.simple_expression_other(attr1)
			attr.ref = attr1.ref
			############
			
		else:
			pass #lambda

	def term(self,attr, porRef = None):
		self.out.write('In term\n')
		
		#########
		attr1 = Ref()		
		self.factor(attr1,porRef)
		self.term_other(attr1,porRef)
		attr.ref = attr1.ref
		#########
		
	def term_other(self,attr, porRef = None):
		self.out.write('In term_other\n')
		token=self.lexer.getNextToken()
		operator = self.lexer.getLexeme()
		self.pushLexeme()
		if token in self.multiplying:
		
			#########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			op = Ref()
			tipo = Ref()
			self.multiplying_operator(op,tipo)
			attr1 = Ref()
			self.factor(attr1)
			if attr.ref.tipo.instancia(tipo.ref):
				if self.checkTypes(attr.ref.tipo,attr1.ref.tipo):
					self.escribir(op.ref)
				else:
					raise SemanticError(self.lexer.errorLeader(), "Non compatible types in expression: %s and %s" % (attr.ref.tipo, attr1.ref.tipo))
			else:
				raise SemanticError(self.lexer.errorLeader(), "Invalid expression: Can not apply '%s' operator to %s" % (operator, attr.ref.tipo))
			self.term_other(attr1)
			attr.ref = attr1.ref
			#########
			
		else:			
			pass #lambda

	def factor(self,attr,porRef = None):
		self.out.write('In factor\n')
		
		token=self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % token)
		if token=='<IDENTIFIER>':

			########			
			self.factor_rest(self.lexer.getLexeme(),attr,porRef)
			########
			
		elif token=='<NUMBER>':
		
			########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			self.escribir("APCT %s" % self.lexer.getLexeme())
			attr.ref = Attr(clase = "subexpression", tipo = Entero(), valor = int(self.lexer.getLexeme()))
			########
			
		elif token=='<OPEN_PARENTHESIS>':
		
			###########
			self.expression(attr,porRef)
			###########
			
			if self.lexer.getNextToken()=='<CLOSE_PARENTHESIS>':
				pass
			else:
				self.synErr('")"')
		elif token=='<NOT_LOGOP>':
		
			###########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			attr1 = Ref()
			self.factor(attr1)
			if attr1.ref.tipo.instancia(Booleano):
				self.escribir("NEGA")
				attr.ref = attr1.ref
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid expression: Cannot apply 'not' operator to %s" % str(attr1.ref.tipo))
			###########
			
		elif token=='<CHAR>':
						
			########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			self.escribir("APCT %s" % ord(self.lexer.getLexeme()[1]))
			attr.ref = Attr(clase = "subexpression", tipo = Caracter(),valor = self.lexer.getLexeme()[1])
			########
			
		elif token == '<ADD_OP>' or token == '<MINUS_OP>':
		
			##########
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			self.pushLexeme()
			valor = Ref()
			self.sign(valor)			
			attr1 = Ref()
			self.factor(attr1)
			if attr1.ref.tipo.instancia(Entero):
				self.escribir("APCT %s" %valor.ref)
				self.escribir("MULT")
				attr.ref = attr1.ref
			else:
				raise SemanticError("Invalid expression: Integer expected, but %s found" % attr1.ref.tipo)
			###########
			
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.getLexeme())
		self.out.write('factor is finished\n')

	def factor_rest(self,id,attr,porRef = None):
		self.out.write('In factor_rest\n')
		token=self.lexer.getNextToken()
		if token=='<OPEN_BRACKET>':
			#TODOOOOOOOOOOOOOOOOOOOOOOO
			###############
			attr1 = Ref()
			###############
			
			self.expression(attr1)
			if self.lexer.getNextToken()=='<CLOSE_BRACKET>':
			
				###############
				array = self.stStack.getGlobalValue(id)
				nivel = self.stStack.lastLexicalLevel()
				if array.clase=="variable" and array.tipo.instancia(Arreglo):
					if self.checkTypes(attr1.ref.tipo,array.tipo.indexType):
						self.escribir("CONT %s,%s" % (array.tipo.indexType.getLower(),array.tipo.indexType.getUpper()))
						self.escribir("APCT %s" % array.tipo.indexType.getLower())
						self.escribir("SUST")
						self.escribir("APAR %s,%s" % (nivel, array.pos))
						attr.ref = Attr(clase = "subexpression", tipo = array.tipo.elementType)
					else:
						raise SemanticError(self.lexer.errorLeader(), "%s expected as index, but %s found" % (array.tipo.indexType, attr1.ref.tipo))
				else:
					raise SemanticError(self.lexer.errorLeader(), "Invalid expression: '%s' is not an array" % id)			
				###############
				
				self.out.write('factor_rest is finished\n')
		elif token=='<OPEN_PARENTHESIS>': # TODOOOOOOOOOOOOOOOOOOOOOOO
			if porRef:
				raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			self.actual_parameter()
			self.actual_parameter_rest()
		else:
			self.pushLexeme() #lambda
			
			########
			identifier = self.stStack.getGlobalValue(id)
			nivel = self.stStack.lastLexicalLevel()
			if identifier.clase == 'function':
				if porRef:
					raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
			elif identifier.clase == 'variable':
				if porRef:
					self.escribir("APDR %s, %s" % nivel, identifier.pos)
				else:
					if identifier.tipo.instancia(Simple):
						self.escribir("APVL %s,%s" % (nivel,identifier.pos))
						attr.ref = deepcopy(identifier)
					else:
						raise SemanticError(self.lexer.errorLeader(), "Invalid expression: Simple type expected, but %s found" % identifier.tipo)
			elif identifier.clase == 'constant':
				if porRef:
					raise SemanticError(self.lexer.errorLeader(),"Invalid function or procedure call: reference parameter expected")
				self.escribir("APCT %s" % identifier.valor)
				attr.ref = deepcopy(identifier)
				attr.ref.clase = "subexpression"
			else:
				raise SemanticError(self.lexer.errorLeader(), "Function, variable or constant expected, but "+ str(identifier.clase)+" identifier found")			
			########

	def actual_parameter(self, esperado = None,id=None):
		self.out.write('In actual_parameter\n')
		
		###########
		attrE = Ref()
		self.expression(attrE)
		
		if id: #si no es None es nuestro
			if id=="write":
				if attrE.ref.tipo.instancia(Entero):
					self.escribir("IMPR")
				elif attrE.ref.tipo.instancia(Caracter):
					self.escribir("IMCH")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Invalid statement: Cannot write %s parameter. Integer or Character expected" % attrE.ref.tipo)
			elif id=="writeln":
				if attrE.ref.tipo.instancia(Entero):
					self.escribir("IMLN")
				elif attrE.ref.tipo.instancia(Caracter):
					self.escribir("IMCN")
				else:
					raise SemanticError(self.lexer.errorLeader(),"Invalid statement: Cannot write %s parameter. Integer or Character expected" % attrE.ref.tipo)
			# elif id=="read": # Falta mucho aca... poner el valor en la variable 
				# if attrE.ref.tipo.instancia(Entero):
					# self.escribir("LEER")
				# elif attrE.ref.tipo.instancia(Caracter):
					# self.escribir("LECH")
				# else:
					# raise SemanticError(self.lexer.errorLeader(),"Invalid statement: Cannot read %s parameter" % attrE.ref.tipo)
			# elif id=="readln":
				# if attrE.ref.tipo.instancia(Entero):
					# self.escribir("LELN")
				# elif attrE.ref.tipo.instancia(Caracter):
					# self.escribir("LECN")
				# else:
					# raise SemanticError(self.lexer.errorLeader(),"Invalid statement: Cannot read %s parameter" % attrE.ref.tipo)
			else:
				Exception("This should not happen")
		else:# si es None es definido por el usuario	
			if not self.checkTypes(esperado[1],attrE.ref.tipo):
				raise SemanticError(self.lexer.errorLeader(),"Invalid procedure or function call: %s parameter expected, but %s found" % (esperado[1],attrE.ref.tipo))
				
		###########

	def actual_parameter_rest(self, listParams=None,id=None):
		self.out.write('In actual_parameter_rest\n')
		token=self.lexer.getNextToken()
		if token=='<COMMA>':
		
			##########
			if id: #es predefinido... necesita una solo parámetro
				raise SemanticError(self.lexer.errorLeader(),"Invalid procedure call: %s has only 1 parameter(s)" % id)
			if len(listParams)>0:
				self.actual_parameter(listParams[0])
				self.actual_parameter_rest(listParams[1:])			
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid procedure or function call: More parameters than expected")
			##########
			
		elif token=='<CLOSE_PARENTHESIS>':
			self.out.write('actual_parameter_restis finished\n')
			
			############
			if id: #es predefinido
				pass
			else:
				if len(listParams)!=0:
					raise SemanticError(self.lexer.errorLeader(),"Invalid procedure or function call: Less parameters than expected")
			############
			
		else:
			self.synErr('"," or ")"')

	def multiplying_operator(self,op,tipo):
		self.out.write('In multiplying_operator\n')
		token=self.lexer.getNextToken()
		if token in self.multiplying:
			self.out.write('multiplying_operator is finished\n')
			
			########
			if token=='<AND_LOGOP>':
				tipo.ref = Booleano
			else:
				tipo.ref = Entero
			op.ref = self.multiplying[token]
			########
			
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.getLexeme())

	def adding_operator(self,op,tipo):
		self.out.write('In adding_operator\n')
		token=self.lexer.getNextToken()
		if token in self.adding:
			
			#############
			if token == "<OR_LOGOP>":
				tipo.ref = Booleano
			else:
				tipo.ref = Entero
			op.ref = self.adding[token]
			#############
			
			self.out.write('adding_operator is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.getLexeme())

	def relational_operator(self,op):
		self.out.write('In relational_operator\n')
		token=self.lexer.getNextToken()
		if token in self.relationals:
		
			#########
			op.ref = self.relationals[token]
			#########
			
			self.out.write('relational_operator is finished\n')
		else:
			raise UnexpectedTokenError(self.lexer.errorLeader(),self.lexer.getLexeme())

	def structured_statement(self):
		self.out.write('In structured_statement\n')
		token=self.lexer.getNextToken()
		self.pushLexeme()
		if token == '<BEGIN>':
			self.compound_statement()
		elif token == '<IF>':
			self.conditional_statement()
		else:
			self.repetitive_statement()

	def conditional_statement(self):
		self.out.write('In conditional_statement\n')
		token=self.lexer.getNextToken()
		self.out.write('Current token == %s\n' % token)
		if token =='<IF>':
		
			################
			attr = Ref()
			self.expression(attr)
			if attr.ref.tipo.instancia(Booleano):
				labelActual = "L" + str(self.labelIndex)
				self.labelIndex += 1
				self.escribir("DSVF %s"% labelActual)
				
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid conditional statement. Boolean expected, but %s found" % attr.ref.tipo)
			################
			
			if self.lexer.getNextToken() =='<THEN>':

				self.statement()
				self.conditional_statement_other(labelActual)
			else:
				self.synErr('"then"')
		else:
			self.synErr('"if"')

	def conditional_statement_other(self,label):
		self.out.write('In conditional_statement_other\n')
		token=self.lexer.getNextToken()
		if token =='<ELSE>':
			
			#############
			labelDpsIf = "L%s" % self.labelIndex
			self.labelIndex+=1
			self.escribir("DSVS %s" %labelDpsIf)
			self.ponerLabel(label)
			#############
			
			self.statement()
			
			###########
			self.ponerLabel(labelDpsIf)
			###########
			
		else:
			self.ponerLabel(label)
			
			self.pushLexeme()


	def repetitive_statement(self):
		self.out.write('In repetitive_statement\n')
		token=self.lexer.getNextToken()

		if token =='<WHILE>':
			
			###########
			self.ponerLabel()
			labelExp = "L%s" % self.labelIndex
			self.labelIndex += 1
			attr = Ref()
			self.expression(attr)
			if attr.ref.tipo.instancia(Booleano):		
				labelDpsWhile = "L%s" % self.labelIndex
				self.labelIndex += 1
				self.escribir("DSVF %s" %labelDpsWhile)				
			else:
				raise SemanticError(self.lexer.errorLeader(),"Invalid repetitive statement condition: Boolean expected but %s found" % attr.ref.tipo)
			###########
			
			if self.lexer.getNextToken() == '<DO>':
				self.statement()
				
				###########
				self.escribir("DSVS %s" % labelExp)
				self.ponerLabel(labelDpsWhile)
				###########
				
			else:
				self.synErr('"do"')
		else:
			self.synErr('"while"')

	def synErr(self,s):
		raise SynError(self.lexer.errorLeader(),s,self.lexer.getLexeme())
		
	def pushLexeme(self):
		self.lexer.pushLexeme(self.out)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file for the compiler messages.')
	parser.add_argument('-d', help='Debug mode',action='store_const', const=True, dest='debug')
	parser.add_argument('-o', dest = 'mepaFile', help='The output file for the generated program (.mepa file).', metavar='OUT_FILE', nargs='?')

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
			
	if args.mepaFile == None:
		mepaFile = args.inputFile[0:args.inputFile.rfind('.')] + ".mepa" #rfind busca la aparición más lejana del parámetro pasado
	else:	
		mepaFile = args.mepaFile
	try:
		mepa = open(mepaFile,'w')
	except:
		print "Error: The file %s could not be opened for writing" % args.mepaFile
			
	lexicalAnalyzer = LexAn(inputFile,args.inputFile)
	syntacticalAnalyzer = SynAn(lexicalAnalyzer,args.debug,output,mepa)
	try:
		msg = syntacticalAnalyzer.execute()
		if output != sys.stdout:
			output.write(msg)
			
		print msg
	except CompilerError as e:
		# output.write(str(e))
		traceback.print_exc()
	finally:
		output.close()
		mepa.close()