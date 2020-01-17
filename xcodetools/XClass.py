class XClass(object):

	'''
	编辑iOS代码文件，添加内容
	'''

	def __init__(self, file_path):
		self._file_path = file_path
		with open(file_path, 'r') as fp:
			self._context = fp.read()

	def add_import(self, name):
		self._context = name + '\n' + self._context
		self._save()

	def write_below(self, below, text):
		self._context = self._context.replace(below, below + '\n' + text + '\n')
		self._save()

	def relpace(self, old, new):
		if new:
			self._context = self._context.replace(old, new)
			self._save()

	def _save(self):
		with open(self._file_path, 'w') as fp:
			fp.write(self._context)
