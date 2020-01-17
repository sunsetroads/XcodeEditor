from pbxproj.pbxsections import *
from pbxproj.pbxextensions import FileOptions
import plistlib

class ProjectCapability(object):

	def add_capability_in_app_purchase(self):
		file_options = FileOptions(embed_framework=False)
		frameworks = self.get_or_create_group('Frameworks')
		self.add_file('System/Library/Frameworks/StoreKit.framework', 
					parent=frameworks,tree='SDKROOT', force=False, file_options=file_options)

	def add_capability_push_notification(self):
		path = None
		entitlements_name = self.__get_project_name() + '.entitlements'

		for item in os.listdir(self._source_root):
			if re.match('^.*\.entitlements$', item):
				path = os.path.join(self._source_root, item)
				self.__add_push_config(path, entitlements_name)

		dir = os.path.join(self._source_root, self.__get_project_name())
		for item in os.listdir(dir):
			if re.match('^.*\.entitlements$', item):
				path = os.path.join(dir, item)
				name = self.__get_project_name() + '/' + entitlements_name
				self.__add_push_config(path, name)

		if not path:
			path = os.path.join(dir, entitlements_name)
			with open(path, 'wb') as fp:
				plistlib.dump({}, fp)
				name = self.__get_project_name() + '/' + entitlements_name
				self.__add_push_config(path, name)

		with open(path, 'rb') as fp:
			entitlements = plistlib.load(fp)
			entitlements['aps-environment'] = 'development'

		with open(path, 'wb') as fp:
			plistlib.dump(entitlements, fp)

	def __add_push_config(self, file_path, flag):
		group =self.get_or_create_group(self.__get_project_name())
		self.add_file(file_path, group, force=False)
		self.set_flags('CODE_SIGN_ENTITLEMENTS', flag)

	def __get_project_name(self):
		return os.path.basename(os.path.dirname(self._pbxproj_path).split('.')[0])


		
