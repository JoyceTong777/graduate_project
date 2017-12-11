import math
import re
from basic_domain import basic_domain
class int_domain(basic_domain):
	def __init__(self):
		self._domain_type = 'INT'

	def get_cardinality(self, value_component_len):
		if value_component_len <= 0:
			return 0
		if value_component_len == 1:
			return 10
		return math.pow(11, value_component_len)

	def get_match_result(self, value):
		reg = r'^([-+]?[0-9]+).*$'
		compile_reg = re.compile(reg)
		match_result = compile_reg.match(value)
		return match_result

	def match_domain_success(self, value):
		match_result = self.get_match_result(value)
		if match_result is None:
			return False
		else:
			return True

	def get_value_component(self, value):
		match_result = self.get_match_result(value)
		if match_result is not None:
			match_string = match_result.group(1)
		else:
			match_string = ''
		return match_string
		
	def get_remain_string(self, value):
		match_string = self.get_value_component(value)
		match_string_len = len(match_string)
		if match_string_len  == len(value):
			remain_string = ''
		elif match_string_len  < len(value):
			remain_string = value[match_string_len:]
		return remain_string

	def get_domain_type(self):
		return self._domain_type
