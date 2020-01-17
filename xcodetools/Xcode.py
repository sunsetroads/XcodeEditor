from pbxproj import XcodeProject
from pbxproj.pbxextensions import FileOptions
from xcodetools.Parser import *
from xcodetools.XClass import *
import plistlib
import os
import json
import re

class Xcode():

	'''
	使用配置文件修改xcodexcode中General、Cpiality、Info、Build Settgings、Build Phases的相关参数

	:param project_path: .xcodeproj所在的目录 例如 /Users/xx/document/xx
	:param config_path: 脚本会根据此文件中的设置来配置xcode
	'''
	
	@classmethod
	def modify(cls, project_path, config_path):
		return Xcode(project_path, config_path)

	def __init__(self, project_path, config):
		self._project_dir = project_path
		self._config = Parser.load(config)
		self._project = XcodeProject.load(self._get_xcodeproj_path() + '/project.pbxproj')
		self._exclude = self._process_array(self._config.get('file', 'excludes').split(','))

		with open(self._get_info_plist_path(), 'rb') as fp:
			self._plist = plistlib.load(fp)
		self._start()

	def _start(self):
		print("\033[32m**********  开始配置xcode  ********* \033[0m")
		self._project.backup()
		self._config_plist()
		self._config_flags()
		self._config_system_frameworks()
		self._config_system_libs()
		self._config_dynamic_framework()
		self._config_script()
		self._config_sign()
		self._config_files()
		self._config_capability()
		self._project.save()
		with open(self._get_info_plist_path(), 'wb') as fp:
			plistlib.dump(self._plist, fp)
		print("\033[32;1mXcode配置完成 🚀 🚀 🚀   \033[0m")

	def _get_info_plist_path(self):
		path = os.path.join(self._project_dir, 'info.plist')
		if os.path.exists(path):
			return path
	
		project = os.path.basename(self._get_xcodeproj_path()).split('.')[0]
		path = '%s/%s/info.plist' % (self._project_dir, project)
		if os.path.exists(path):
			return path
		else:
			print('找不到info.plist,请修改info.plist位置，或修改脚本get_info_plist_path函数')
			exit()

	def _get_xcodeproj_path(self):
		for item in os.listdir(self._project_dir):
			if re.match('^.*\.xcodeproj$', item):
				return os.path.join(self._project_dir, item)

	def _config_flags(self):
		items = self._config.items('flag_add')
		for (key, value) in items:
			temp = self._process_array(value.split(','))
			if value:
				self._project.remove_flags(key, temp)
				self._project.add_flags(key, temp)
			
		sets = self._config.items('flag_set')
		for (key, value) in sets:
			if  value:
				temp = self._process_array(value.split(','))
				self._project.set_flags(key, temp)	

	def _config_system_libs(self):
		libs = self._config.get('build_phase', 'libs')
		items = self._process_array(libs.split(','))
		if items[0] == '':
			return
		
		file_options = FileOptions(embed_framework=False)
		frameworks = self._project.get_or_create_group('Frameworks')
		for item in items:
			temp = 'usr/lib/%s' % item
			self._project.add_file(temp, parent=frameworks, tree='SDKROOT', force=False, file_options=file_options)

	def _config_system_frameworks(self):
		libs = self._config.get('build_phase', 'frameworks')
		items = self._process_array(libs.split(','))
		if items[0] == '':
			return
		
		file_options = FileOptions(embed_framework=False)
		frameworks = self._project.get_or_create_group('Frameworks')
		for item in items:
			temp = 'System/Library/Frameworks/%s' % item
			self._project.add_file(temp, parent=frameworks, tree='SDKROOT', force=False, file_options=file_options)

	def _config_dynamic_framework(self):
		path = self._config.get('file', 'embedded_path')
		if not path:
			return

		groupName = os.path.basename(path)
		newPath = os.path.join(self._project_dir, groupName)
		self._project.remove_group_by_name(groupName)
		
		os.system('rm -rf %s' % newPath)
		os.system('cp -rf %s %s' % (path, self._project_dir))
		self._project.add_folder(newPath, excludes=self._exclude)		

	def _config_script(self):
		script = self._config.get('build_phase', 'script')
		if script:
			self._project.remove_run_script(script)
			self._project.add_run_script(script)

	def _config_files(self):
		key = 'file'
		paths = self._process_array(self._config.get(key, 'file_path').split(','))
		if paths[0] == '':
			return

		options = FileOptions(embed_framework=False)
		for path in paths:
			# 删除已存在的
			groupName = os.path.basename(path)
			newPath = os.path.join(self._project_dir, groupName)
			self._project.remove_group_by_name(groupName)

			# 移动文件到工程中
			os.system('rm -rf %s' % newPath)
			os.system('cp -rf %s %s' % (path, self._project_dir))

			self._project.add_folder(newPath, excludes=self._exclude, file_options=options)

	def _config_plist(self):
		key = 'general'

		bundle_id = self._config.get(key, 'bundle_id')
		if bundle_id:
			self._project.set_flags('PRODUCT_BUNDLE_IDENTIFIER', bundle_id)
			self._plist['CFBundleIdentifier'] = bundle_id

		display_name = self._config.get(key, 'display_name')
		if display_name:
			self._project.set_flags('PRODUCT_NAME', display_name)
			self._plist['CFBundleDisplayName'] = display_name

		bundle_version = self._config.get(key, 'version')
		if bundle_version:
			self._plist['CFBundleShortVersionString'] = bundle_version

		build_version = self._config.get(key, 'build')
		if build_version:
			self._plist['CFBundleVersion'] = build_version

		url_query = self._config.get(key, 'url_query')
		if url_query:
			temp = self._process_array(url_query.split(','))
			self._plist['LSApplicationQueriesSchemes'] = temp

		url_schemes = self._config.get(key, 'url_schemes')
		if url_schemes:
			temp = self._process_array(url_schemes.split(','))
			self._plist['CFBundleURLTypes']= [{'CFBundleURLSchemes':temp}]

		user_defined = self._config.get(key, 'user_defined')
		if user_defined:
			temp = json.loads(user_defined)
			for key, value in temp.items():
				self._plist[key] = value

		items = self._config.items('pirvacy')
		for (key, value) in items:
			if value:
				self._plist[key] = value

	def _config_sign(self):
		key = 'sign'
		sign_identity = self._config.get(key, 'code_sign_identity')
		team = self._config.get(key, 'development_team')
		profile = self._config.get(key, 'provisioning_profile_specifier')

		if sign_identity and team and profile:
			self._project.set_flags('CODE_SIGN_STYLE', 'Manual')
			self._project.add_code_sign(sign_identity, team, '', profile)

	def _config_capability(self):
		key = 'capability'
		push = self._config.get(key, 'push')
		if push:
			self._project.add_capability_push_notification()

		in_app_purchase = self._config.get(key, 'in_app_purchase')
		if in_app_purchase:
			self._project.add_capability_in_app_purchase()

	def _process_array(self, array):
		return list(map(lambda x: x.strip(), set(array)))