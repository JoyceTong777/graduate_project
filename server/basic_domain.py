from abc import ABCMeta, abstractmethod
class basic_domain:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.domain_type = ''

	@abstractmethod
	def get_cardinality(self):pass

	@abstractmethod
	def match_domain_success(self):pass

	@abstractmethod
	def get_match_result(self):pass

	@abstractmethod
	def get_remain_string(self):pass

	def get_domain_type(self):
		return self.domain_type