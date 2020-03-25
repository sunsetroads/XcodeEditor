## XcodeEditor
一套 Xcode 脚本工具集，根据 .ini 文件的配置信息，自动化修改 Xcode 配置和导出 ipa 包。

修改 Xcode 配置是指对 Xcode 工程的 General、Capability、Info、Build Settgings、Build Phases 中的参数进行修改，以及添加文件和 Framework 等。

**[安装说明](./INSTALL.md)**

**此插件主要用于 Untiy 的自动化出包，[点击这里](https://sunsetroads.github.io/2019/11/11/untiy-export-ipa/) 可以查看从 Untiy 工程到 iOS 包的自动化流程。**


### 快速开始

clone 此项目后，进入工程根目录：
```
git clone git@github.com:sunsetroads/XcodeEditor.git
```
```
cd XcodeEditor
```
修改 example.ini 中的参数，然后运行：
```
python3 test.py
```
之后就可以在 demo 工程中查看效果。

### 模块说明

**Xcode**

根据配置文件修改 Xcode 中的相关参数，配置规则在 [example.ini](./example.ini) 文件中有详细说明。
```py
from xcodetools import Xcode

config_path = './config.ini'

project_path = '/Users/zhangning/Desktop/testpbx'

# 根据 config.ini 修改 xcode
Xcode.modify (project_path, config_path)
```

**Package**

Package 模块用于自动化打包，打包时需要指定一个 plist 文件，其中包含了包的类型和相关证书等参数。plist 文件可借助 Plist 模块来快速生成，也可以先手动打包，生成 ipa 的同时会有一个 ExportOption.plist。
```py
from xcodetools import Package

project_path = '/Users/zhangning/Desktop/testpbx'

ipa_path = '/Users/zhangning/Desktop/IPA/test.ipa'

plist = '/Users/zhangning/Desktop/ExportOptions.plist'

# 开始自动打包
Package.build (project_path, ipa_path, plist)
```

**XClass**

XClass 模块主要用于编辑 iOS 代码文件，添加内容
```py
from xcodetools import Package

class_path = '/Users/zhangning/Desktop/ChannelBridge/Classes/UnityAppController.mm'

file = XClass (class_path)

# 修改 ios 代码文件
file.add_import ('#import <XLSDK/XLApplePay.h>')
```

**Plist**

Plist 模块根据指定参数生成命令行打包所需 Plist 文件，参数说明和获取方式请查看注释
```py
from xcodetools import Plist

Plist.generate_export_option (
        '/temp/dev.plist', 
        'dev', 
        'test.bundleid', 
        'dev_0815', 
        '83 95 25 24 0B 39 F6 EC AF 0B F2 D3 F1 48 7F 5A C9 57 3D 85', 
        'NJ37YVPET8'
        )
```
