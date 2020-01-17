import os
import plistlib

class Plist(object):

	@classmethod
	def generate_export_option(cls, plist_path, ipa_type, bundle_id, profile_name, certificate, team_id):
		
		'''
		使用命令行打包Xcode工程时，需要用到一个plist文件，通过此函数可以快速生成

		:param plist_path: 生成的plist存放路径
		:param ipa_type: 打包的类型，包含dev dis adhoc三种
		:param bundle_id: xcode工程的bundle_id
		:param profile_name: 打包的mobileprovision文件名称
		:param certificate: 打包的证书，在钥匙串中双击证书，底部的SHA-1值为此参数
		:param team_id: 在钥匙串中双击证书，组织单位为此参数
		'''
		
		option = {
			'dev': 'development',
			'dis': 'app-store',
			'adhoc': 'ad-hoc'
		}
		
		export_options = dict(
			compileBitcode = False,
			destination = 'export',
			method = option[ipa_type],
			provisioningProfiles = {bundle_id: profile_name},
			signingCertificate = certificate.replace(' ', ''),
			signingStyle = 'manual',
			stripSwiftSymbols = True,
			teamID = team_id,
			thinning = '<none>'
		)
		dir = os.path.dirname(plist_path)
		if not os.path.exists(dir):
			os.makedirs(dir)

		with open(plist_path, 'wb') as fp:
			plistlib.dump(export_options, fp)