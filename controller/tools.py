import pandas as pd

def init_data(photos, judges):
	fields = judges + ['Total', 'Penalty']
	data = pd.DataFrame(0, index = range(1, photos + 1), columns = fields)
	data.index.name = 'ID'
	return data

def decor_csv(list_name, is_read):
	if list_name == 'judges':
		csv_path = 'resource/judges.csv'
	elif list_name == 'candidates':
		csv_path = 'resource/candidates.csv'
	
	def decor_read(func):
		def wrapper():
			return pd.read_csv(csv_path, sep = ',', index_col = 0, encoding = 'utf-8')
		return wrapper
	
	def decor_write(func):
		def wrapper(data):
			data.to_csv(csv_path, sep = ',', encoding = 'utf-8')
		return decor_read
	
	return decor_read if is_read else decor_write

@decor_csv(list_name = 'judges', is_read = True)
def get_judges():
	pass

@decor_csv(list_name = 'judges', is_read = False)
def save_judges():
	pass

@decor_csv(list_name = 'candidates', is_read = True)
def get_candidates():
	pass

@decor_csv(list_name = 'candidates', is_read = False)
def save_candidates():
	pass
