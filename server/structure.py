class Structure:
	_struct_name = ""
	_match_row_index_list = []
	_value_component_list = []
	def __init__(self, struct_name):
		self._struct_name = struct_name
		self._match_row_index_list = []
		self._value_component_list=[]

	def add_match_row_index(self, match_row_index):
		self._match_row_index_list.append(match_row_index)

	def add_value_component(self, value_component):
		self._value_component_list.append(value_component)

	def get_match_row_index_list(self):
		return self._match_row_index_list

	def get_value_component_list(self):
		return self._value_component_list

	def get_struct_name(self):
		return self._struct_name