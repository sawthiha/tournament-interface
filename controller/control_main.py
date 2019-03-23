import controller.controller as control
import controller.tools as tools
import ui.tools as ui_tools

def create(root):
	def create(caller):
		title = caller.varTitle.get()
		judges = caller.varJudges.get()
		photos = caller.varPhotos.get()
		candidates = caller.varCandidates.get()
		step = caller.varStep.get()
		judge_list = caller.tags.all()
		if photos <= 0:
				caller.warn()
				return
		caller.destory()
		control.init_tournament(root, judge_list, title, judges, photos, candidates, step)
	
	judge_list = tools.get_judges()

	def logic(partial):
		return judge_list[judge_list['name'].str.contains(partial)]['name'].tolist()

	def decor_save_judge(func):
		def wrapper(judge):
			if not judge:
				return
			if judge not in judge_list['name'].values:
				judge_list.loc[len(judge_list) + 1] = judge
				tools.save_judges(judge_list)
			func(judge)
		return wrapper

	prompt = ui_tools.promptcreate(root, create, logic, decor_save_judge)

def history(root):
	pass

def settings(root):
	pass

def about(root):
	prompt = ui_tools.promptabout(root)