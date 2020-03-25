from xcodetools import *
import sys

config_path = './example.ini'

project_path = './demo'

ipa_path = './test.ipa'

plist = './dev.plist'

# 开始修改 xcode 配置
Xcode.modify (project_path, config_path)

# 开始打包
Package.build (project_path, ipa_path, plist)