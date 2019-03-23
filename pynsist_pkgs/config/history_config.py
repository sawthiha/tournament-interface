import config.config as config

history_config = config.config['HISTORY']
path = config.from_root(history_config['Path'])
format_dir = history_config['Dir_Format']
format_step = history_config['Step_Format']
format_final = history_config['Final_Format']
format_result = history_config['result_format']
format_tb = history_config['TB_Format']
format_date = history_config['Date_Format']
format_judges = history_config['Judges_Format']
meta_name = history_config['Meta_Name']
judges_record_path = config.from_root(history_config['judges_record'])
candidates_record_path = config.from_root(history_config['candidates_record'])