import sys
import argparse, io
sys.path.append('../Entrega 2/')
from lexan import LexAn,LexError

class SynAn():
	def __init__(self,lexer):
		self.lexer = lexer
		
	def execute(self):
		self.program()

	def program(self):
		pass

	def program_heading(self):
		pass

	def block(self):
		pass

	def constant_definition_part(self):
		pass

	def block_cons_rest(self):
		pass

	def type_definition_part(self):
		pass

	def block_type_rest(self):
		pass

	def variable_definition_part(self):
		pass

	def block_var_rest(self):
		pass

	def procedure_and_function_declaration_part(self):
		pass

	def statement_part(self):
		pass

	def constant_definition(self):
		pass

	def constant_definition_rest(self):
		pass

	def constant_definition_rest_rest(self):
		pass

	def constant(self):
		pass

	def sign(self):
		pass

	def constant_rest(self):
		pass

	def type_definition(self):
		pass

	def type_definition_rest(self):
		pass

	def type_definition_rest_rest(self):
		pass

	def type(self):
		pass

	def simple_type(self):
		pass

	def structured_type(self):
		pass

	def subrange_type(self):
		pass

	def subrange_type_rest(self):
		pass

	def variable_declaration(self):
		pass

	def variable_declaration_part_rest(self):
		pass

	def variable_declaration_rest_rest(self):
		pass

	def variable_declaration_rest(self):
		pass

	def procedure_or_function_declaration_part(self):
		pass

	def procedure_declaration(self):
		pass

	def function_declaration(self):
		pass

	def procedure_heading(self):
		pass

	def procedure_heading_rest(self):
		pass

	def formal_parameter_section(self):
		pass

	def formal_parameter_rest(self):
		pass

	def parameter_group(self):
		pass

	def parameter_group_rest(self):
		pass

	def function_heading(self):
		pass

	def function_heading_rest(self):
		pass

	def formal_parameter_function_rest(self):
		pass

	def statement_part_rest(self):
		pass

	def statement(self):
		pass

	def statement_rest(self):
		pass

	def statemente_rest_rest(self):
		pass

	def simple_statement(self):
		pass

	def structured_statement(self):
		pass

	def simple_statement_rest(self):
		pass

	def expression(self):
		pass

	def actual_parameter(self):
		pass

	def actual_parameter_rest(self):
		pass

	def component_variable(self):
		pass

	def simple_expression(self):
		pass

	def expression_rest(self):
		pass

	def relational_operator(self):
		pass

	def term(self):
		pass

	def simple_expression_other(self):
		pass

	def adding_operator(self):
		pass

	def factor(self):
		pass

	def term_other(self):
		pass

	def multiplying_operator(self):
		pass

	def factor_rest(self):
		pass

	def procedure_statement(self):
		pass

	def procedure_statement_rest(self):
		pass

	def structured_statement_other(self):
		pass

	def conditional_statement(self):
		pass

	def repetitive_statement(self):
		pass

	def conditional_statement_rest(self):
		pass

	def conditional_statement_other(self):
		pass

	def repetitive_statement_rest(self):
		pass



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lexical analysis for the provided .pas file.')
	parser.add_argument('inputFile', metavar='IN_FILE', help='The source .pas file')
	parser.add_argument('outputFile', metavar='OUT_FILE', nargs='?', help='The optional output file.')

	args = parser.parse_args()
	inputFile = io.BufferedReader(io.FileIO(args.inputFile))
	outputFile = args.outputFile
	
	if outputFile == None:
		output = None
		print "\n\nStarting file lexical and syntactical analysis...\n\n"
	else:
		try:
			output = open(outputFile, 'w')
			print "\n\nStarting file lexical and syntactical analysis... results will be shown right here, and be written to %s\n\n" % outputFile
		except:
			print "Error: The file %s could not be opened for writing" % outputFile
			
	lexicalAnalyzer = LexAn(inputFile)
	syntacticalAnalyzer = SynAn(lexicalAnalyzer)
	try:
		msg = syntacticalAnalyzer.execute()
		if output is not None:
			output.write(msg)
		print msg
	except Exception as e:
		if output is not None:
			output.write(msg)
		print e