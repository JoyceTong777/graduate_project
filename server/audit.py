import pandas as pd
import numpy as np
import math
import os, sys
from int_domain import int_domain
from float_domain import float_domain
from word_domain import word_domain
from space_domain import space_domain
from punct_domain import punct_domain
from default_domain import default_domain
from structure import Structure
from table import Table
from table import ColumnAnomaly
from table import ColumnData


int_domain_instance = int_domain()
float_domain_instance = float_domain()
word_domain_instance = word_domain()
punct_domain_instance = punct_domain()
default_domain_instance = default_domain()
domain_instance_array = []
domain_instance_array.append(float_domain_instance)
domain_instance_array.append(int_domain_instance)
domain_instance_array.append(word_domain_instance)
domain_instance_array.append(punct_domain_instance)
domain_instance_array.append(default_domain_instance)

def extract_cell_pattern(value):
	if value == "":
		return ("EMPTY","")
	pattern = ""
	value_component = []
	while value != "":
		for each_domain_instance in domain_instance_array:
			if each_domain_instance.match_domain_success(value):
				pattern_component = each_domain_instance.get_domain_type()
				pattern += pattern_component +':'
				value_component.append(each_domain_instance.get_value_component(value))
				value = each_domain_instance.get_remain_string(value)
				break
	if len(pattern) > 1:
		pattern = pattern[:len(pattern)-1]
	extract_result = (pattern, value_component)
	return extract_result

def detect_domain_and_pattern_stats(column):
	pattern_dict = {}
	for idx in range(len(column)):
		extract_result= extract_cell_pattern(column[idx])
		cell_pattern = extract_result[0]
		if cell_pattern == 'EMPTY':
			continue
		value_component = extract_result[1]

		if cell_pattern in pattern_dict.keys():
			structure_instance = pattern_dict.get(cell_pattern)
			structure_instance.add_match_row_index(idx)
			structure_instance.add_value_component(value_component)
			pattern_dict[cell_pattern] = structure_instance
		else:
			structure_instance = Structure(cell_pattern)
			structure_instance.add_match_row_index(idx)
			structure_instance.add_value_component(value_component)
			pattern_dict[cell_pattern] = structure_instance
	return pattern_dict

def detect_domain_and_pattern_stats(column):
	pattern_dict = {}
	for idx in range(len(column)):
		extract_result = extract_cell_pattern(column[idx])
		cell_pattern = extract_result[0]
		if cell_pattern == 'EMPTY':
			continue
		value_component = extract_result[1]
		if cell_pattern in pattern_dict.keys():
			structure_instance = pattern_dict.get(cell_pattern)
			structure_instance.add_match_row_index(idx)
			structure_instance.add_value_component(value_component)
			pattern_dict[cell_pattern] = structure_instance
		else:
			structure_instance = Structure(cell_pattern)
			structure_instance.add_match_row_index(idx)
			structure_instance.add_value_component(value_component)
			pattern_dict[cell_pattern] = structure_instance
	return pattern_dict

def detect_avg_max_len(column):
	max_len = len(column[0])
	sum_len = 0
	for idx in range(len(column)):
		if len(column[idx]) >= max_len:
			max_len = len(column[idx])
		sum_len += len(column[idx])
	avg_len = sum_len/len(column)
	avg_max_result = (avg_len, max_len)
	return avg_max_result

domain_instance_dict = {}
domain_instance_dict['FLOAT'] = float_domain()
domain_instance_dict['INT'] = int_domain()
domain_instance_dict['WORD'] = word_domain()
domain_instance_dict['SPACE'] = space_domain()
domain_instance_dict['PUNCT'] = punct_domain()
domain_instance_dict['DEFAULT'] = default_domain()

def get_column_majority_pattern(column, pattern_dict):
	dl = -1 
	best_pattern = ""
	number_of_values = len(column)
	avg_max_result = detect_avg_max_len(column)
	avg_value_len = avg_max_result[0]
	max_value_len = avg_max_result[1]

	for each_pattern in pattern_dict.keys():
		pattern_dl = 0
		split_each_pattern = each_pattern.split(":")
		number_of_pattern_component = len(split_each_pattern)
		pattern_dl += number_of_pattern_component * math.log(5) # there are 5 types of domain

		
		default_domain_instance = default_domain()
		pattern_dl += avg_value_len * math.log(default_domain_instance.get_cardinality(1)) 

		number_of_match_rows = len(pattern_dict[each_pattern].get_match_row_index_list())
		match_probability = number_of_match_rows/number_of_values

		pattern_dl += match_probability * number_of_pattern_component * math.log(max_value_len)

		value_component_list = pattern_dict[each_pattern].get_value_component_list()

		pattern_component_list = split_each_pattern

		for i in range(len(value_component_list)):
			for j in range(number_of_pattern_component):
				value_component_line = value_component_list[i]
				value_component = value_component_line[j]
				domain_name = pattern_component_list[j]
				domain_instance = domain_instance_dict[domain_name]
				domain_cardinality = domain_instance.get_cardinality(len(value_component))
				default_domain_instance = domain_instance_dict['DEFAULT']
				default_domain_cardinality = default_domain_instance.get_cardinality(len(value_component))
				pattern_dl += (match_probability/number_of_values) * math.log(domain_cardinality/default_domain_cardinality)
 		
		if dl == -1:
 			dl = pattern_dl
 			best_pattern = each_pattern
		elif pattern_dl < dl:
			dl = pattern_dl
			best_pattern = each_pattern

	return best_pattern


def detect_anomaly_number(pattern_dict, column):
	double_value_list = []
	total_idx_list = []
	anomaly_number_rows = []
	for each_pattern in pattern_dict.keys():
		if each_pattern != 'INT' and each_pattern != 'FLOAT':
			continue
		else:
			idx_list = pattern_dict[each_pattern].get_match_row_index_list()
			for idx, item in enumerate(idx_list):
				double_value_list.append(np.float(column[item]))
			total_idx_list.extend(idx_list)

	if len(total_idx_list) == 0:
		return anomaly_number_rows
	mean_value = np.mean(double_value_list)
	std_value = np.std(double_value_list)

	for idx, item in enumerate(total_idx_list):
		if abs(np.float(column[item])- mean_value) > 2 * std_value:
			anomaly_number_rows.append(item)

	return anomaly_number_rows

def detect_pattern_inconsistent_anomalies(best_pattern, pattern_dict):
	anomaly_rows = []
	for each_pattern in pattern_dict.keys():
		if each_pattern != best_pattern:
			structure_instance = pattern_dict[each_pattern]
			anomaly_rows.extend(structure_instance.get_match_row_index_list())
	return anomaly_rows

def detect_empty_anomalies(analyst_column):
	empty_rows = []
	for idx, item in enumerate(analyst_column):
		if item == '':
			empty_rows.append(idx)
	return empty_rows

def detect_anomaly_length(analyst_column):
	length_stat = []
	anomaly_length_rows = []
	for idx, item in enumerate(analyst_column):
		length_stat.append(np.float(len(item)))
	mean_value = np.mean(length_stat)
	std_value = np.std(length_stat)

	for idx, item in enumerate(analyst_column):
		if abs(np.float(len(item)) - mean_value) > 2 * std_value and item != "":
			anomaly_length_rows.append(idx)

	return anomaly_length_rows

def get_table_list():
	path = './dataset'
	table_list = []
	for file in os.listdir(path):
		if file.endswith(".csv"):
			#obj = {"name": file}
			table_list.append(file)
	print table_list
	return table_list

def get_audit_result(tableName):
	table_path = './dataset/' + tableName
	df = pd.read_csv(table_path,header = 0)
	df = df.replace(np.nan, '', regex=True)
	x = Table(tableName)
	for idx in df.columns:
		header = idx
		column = df[idx].tolist()
		x.add_table_data(ColumnData(header, column))
	number_columns = len(df.columns)

	for idx in df.columns:
		column_anomaly_instance = ColumnAnomaly(idx)
		analyst_column = df[idx].apply(lambda x: str(x))
 		
 	
		empty_rows = detect_empty_anomalies(analyst_column)
		column_anomaly_instance.add_empty_anomaly(empty_rows)

		pattern_dict = detect_domain_and_pattern_stats(analyst_column)
		best_pattern = get_column_majority_pattern(analyst_column, pattern_dict)

		pattern_anomaly = detect_pattern_inconsistent_anomalies(best_pattern, pattern_dict)

		column_anomaly_instance.add_pattern_inconsistent_anomaly(pattern_anomaly)
		
		anomaly_number_rows = detect_anomaly_number(pattern_dict, analyst_column)
		column_anomaly_instance.add_number_anomaly(anomaly_number_rows)	
		
		anomaly_length_rows = detect_anomaly_length(analyst_column)
		column_anomaly_instance.add_length_anomaly(anomaly_length_rows)	

		x.add_table_anomaly(column_anomaly_instance)

	return x



