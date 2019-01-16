import os
import os.path as path
import configparser as config
import pandas as pd
import config.history_config as history
import controller.tools as tools
import parse

FIELDS = ['No', 'Title', 'Photos', 'Date', 'URI']

def decor_walk(func):
	def wrapper(uri):
		for walked, dirs, files in os.walk(uri):
			return func(walked, files, dirs)
	return wrapper

@decor_walk
def list_dirs(walked, files, dirs):
	return dirs

@decor_walk
def list_files(walked, files, dirs):
	return files

def all_history():
	dirs = list_dirs(history.path)
	parser = config.ConfigParser()
	for d in dirs:
		dir_path = path.join(history.path, d)
		files = list_files(dir_path)
		if history.meta_name in files:
			meta_path = path.join(dir_path, history.meta_name)
			try:
				parser.read(meta_path)
				info = parser['META']
				yield int(info['No']), info['Title'], int(info['Photos']), info['Date'], info['URI']
			except KeyError:
				pass
 
RECORD = pd.DataFrame([entry for entry in all_history()], columns = FIELDS)
RECORD.set_index('No', inplace = True)
RECORD.sort_index(inplace = True)

def update_history(info):
	global RECORD
	row = pd.DataFrame([(info['META']['Title'], info['META']['Photos'], info['META']['Date'], info['META']['URI'])], columns = FIELDS[1:], index = [info['META']['No']])
	RECORD = RECORD.append([row], ignore_index = False)


def next_id():
	return 1 if RECORD.empty else RECORD.iloc[-1].name + 1

def decor_save(func):
	def wrapper(title, candidates, photos, date, judge_list, data, judges, t_step):
		no = next_id()
		info = config.ConfigParser()
		info.add_section('META')
		info['META']['No'] = str(no)
		info['META']['Title'] = title
		info['META']['Photos'] = str(photos)
		info['META']['Candidates'] = str(candidates)
		info['META']['Judges'] = ','.join(judge_list)
		info['META']['Date'] = date.strftime(history.format_date)
		info['META']['URI'] = path.join(history.path, history.format_dir.format(no))

		try:
			os.mkdir(info['META']['URI'])
			meta_path = path.join(info['META']['URI'], history.meta_name)
			with open(meta_path, 'w') as file:
				info.write(file)	
			update_history(info)
		except OSError:
			pass

		return func(info, data, judges, t_step)
	return wrapper

def save_process(parent, type, data, no):
	global FORMAT
	sub = history.format_step 
	sub = FORMAT[type].format(no)
	step_path = path.join(parent, sub)
	data.to_csv(step_path, sep = ',', encoding = 'utf-8')

def decor_read_process(func):
	def wrapper(process_no):
		global RECORD
		global FORMAT
		process_path = RECORD.loc[process_no, 'URI']
		files = list_files(process_path)
		stages = []
		finals = []
		info = config.ConfigParser()
		info.read(path.join(process_path, history.meta_name))
		judges = path.join(process_path, history.format_judges)
		for f in list_files(process_path):
			stage_no = parse.parse(FORMAT[process.STEP], f)
			final_no = parse.parse(FORMAT[process.FINAL], f)
			f_path = path.join(process_path, f)
			if stage_no:
				stages.append((stage_no[0], f_path))
			if final_no:
				finals.append((final_no[0], f_path))
		return func(info, judges, stages, finals)
	return wrapper