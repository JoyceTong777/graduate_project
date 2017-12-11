import json

class Table:
	name = ''
	data = []
	anomaly = []

	def __init__(self, name):
		self.name = name
		self.data = []
		self.anomaly =[]

	def add_table_data(self, column_data):
		column_data_object = column_data.get_column_data_object()
		self.data.append(column_data_object)

	def add_table_anomaly(self, column_anomaly):
		anomaly_data_object = column_anomaly.get_column_anomaly_object()
		self.anomaly.append(anomaly_data_object)

	def get_table_data(self):
		return self.data

	def get_table_anomaly(self):
		return self.anomaly

	def get_table_object(self):
		dict = {
			"name": self.name,
			"data": self.data,
			"anomaly": self.anomaly
		}
		return dict


class ColumnData:
	header = ''
	colData = []
	def __init__(self, header, column):
		self.header = header
		self.colData = column
	def get_column_header(self):
		return self.header
	def get_column_data(self):
		return self.colData
	def get_column_data_object(self):
		dict = {
			"header": self.header,
			"colData": self.colData
		}
		return dict


class ColumnAnomaly:
	_column_header = ""
	_column_index = 0

	emptyOutlier = []
	patternInconsistent = []
	lengthOutlier = []	
	numericalOutlier = []

	def __init__(self, header):
		self._column_header = header
		# self._column_index = idx
		self.patternInconsistent = []
		self.lengthOutlier = []
		self.numericalOutlier = []
		self.emptyOutlier = []

	def add_pattern_inconsistent_anomaly(self, arr):
		self.patternInconsistent = arr

	def add_length_anomaly(self,arr):
		self.lengthOutlier = arr

	def add_number_anomaly(self, arr):
		self.numericalOutlier = arr

	def add_empty_anomaly(self, arr):
		self.emptyOutlier = arr

	def get_pattern_inconsistent_anomaly(self):
		return self.patternInconsistent

	def get_length_anomaly(self):
		return self.lengthOutlier

	def get_number_anomaly(self):
		return self.numericalOutlier

	def get_empty_anomaly(self):
		return self.emptyOutlier

	def get_column_anomaly_object(self):
		dict = {
			"patternInconsistent": self.patternInconsistent,
			"lengthOutlier": self.lengthOutlier,
			"numericalOutlier": self.numericalOutlier,
			"emptyOutlier": self.emptyOutlier
		}
		return dict