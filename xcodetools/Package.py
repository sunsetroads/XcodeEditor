import os
import re
import shutil

class Package(object):
	
	'''
	自动化打包脚本

	:param project_path: .xcodeproj所在的目录 例如 /Users/xx/document/xx
	:param ipa_path: 最终生成的ipa路径，例如：/Users/xx/document/xx/build/xx.ipa
	:param export_option_plist_path: 打包配置plist路径，可先通过手动打包获取，也可使
		用Plist的generate_export_option快速生成
	'''

	@classmethod
	def build(cls, project_path, ipa_path, export_option_plist_path):
		return Package(project_path, ipa_path, export_option_plist_path)
	
	def __init__(self, project_path, ipa_path, plist_path):
		if not project_path:
			raise('缺少Xcode工程路径参数')
		
		if not ipa_path:
			raise('缺少ipa路径参数')

		if not plist_path:
			raise('缺少ExportOption.plist路径参数')

		self._project_dir = project_path
		self._ipa_path = ipa_path
		self._plist_path = plist_path

		self._clean_project()
		self._archive_project()
		self._export_ipa()

	def _clean_project(self):
		os.system('open %s' % self._get_xcodeproj_path())
		os.system('sleep 10')
		print("\033[32m*********  开始构建项目  *********  \033[0m")
		os.system('xcodebuild clean -project %s  -scheme %s -configuration %s || exit' % 
		 	(self._get_xcodeproj_path(), self._get_scheme(), self._get_build_configuration()))

	def _archive_project(self):
		os.system('xcodebuild archive -project %s -scheme %s -configuration %s -archivePath %s || exit' % 
			(self._get_xcodeproj_path(), self._get_scheme(), self._get_build_configuration(), self._get_archive_path()))        	 

		if os.path.exists(self._get_archive_path()):
			print("\033[32;1m项目构建成功 🚀 🚀 🚀  \033[0m")
		else:
			print("\033[31;1marchive失败，请打开xcode检查错误信息 😢 😢 😢   \033[0m")
			exit()

	def _export_ipa(self):
		print("\033[32m*************************  开始导出ipa文件  *************************  \033[0m")
		ipa_dir = os.path.dirname(self._ipa_path)
		ipa_name = os.path.basename(self._ipa_path)

		os.system("xcodebuild -exportArchive -archivePath %s -exportOptionsPlist %s -exportPath %s || exit" 
			% (self._get_archive_path(),self._get_export_option_path(), ipa_dir)) 

		for item in os.listdir(ipa_dir):
			if re.match('^.*\.ipa$', item):
				os.chdir(ipa_dir)
				os.rename(item,ipa_name)

		if os.path.exists(self._ipa_path):
			print("\033[32;1m导出 %s 包成功 🎉  🎉  🎉   \033[0m" % self._ipa_path)
		else:
			print("\033[31;1m导出ipa包失败 😢 😢 😢     \033[0m")
			exit()

	def _get_xcodeproj_path(self):
		for item in os.listdir(self._project_dir):
			if re.match('^.*\.xcodeproj$', item):
				return os.path.join(self._project_dir, item)

	def _get_archive_path(self):
		project = os.path.basename(self._project_dir)
		return os.path.join(self._project_dir, 'temp/%s.xcarchive' % project)

	def _get_export_option_path(self):
		return self._plist_path

	def _get_build_configuration(self):
		return 'Release'

	def _get_scheme(self):
		
		return os.path.basename(self._get_xcodeproj_path()).split('.')[0]

