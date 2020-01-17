from xcodetools import *
import sys

# 获取执行脚本的参数
if len (sys.argv) < 5:
        print ('''
                usage:
                        请按以下方式启动 (需要在 ini 文件中完成所需配置)
                        python3 [.ini 配置文件路径] [xcode 工程路径] [ipa 存放路径] [ExportOption.plist 路径]
                ''')
        exit ()

config_path = sys.argv [1]

project_path = sys.argv [2]

ipa_path = sys.argv [3]

plist = sys.argv [4]

# 开始修改 xcode 配置
Xcode.modify (project_path, config_path)

# 开始打包
Package.build (project_path, ipa_path, plist)