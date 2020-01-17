## XcodeEditor 
一套 Xcode 脚本工具集，用于自动化配置 Xcode 和导出 ipa 包。

Xcode 配置包括对工程中 General、Capability、Info、Build Settgings、Build Phases 相关参数的修改，以及添加文件和系统库。

此插件非常适用于 Untiy 开发，[点击这里](https://sunsetroads.github.io/2019/11/11/untiy-export-ipa/) 可以查看从 Untiy 工程到 iOS 包的自动化配置流程。

#### [安装说明](./INSTALL.md)

### 快速开始

```
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

# 根据配置文件修改 xcode 工程的各项配置
Xcode.modify (project_path, config_path)

# 开始打包
Package.build (project_path, ipa_path, plist)
```

### 模块说明

**Xcode**

根据配置文件修改 Xcode 中的相关参数，配置规则在 [test.ini](./test.ini) 文件中有详细说明。
```
from xcodetools import Xcode

config_path = './test.ini'

project_path = './demo'

# 根据 config.ini 修改 xcode
Xcode.modify (project_path, config_path)
```

**Package**

Package 模块用于自动化打包，打包时需要指定一个 plist 文件，其中包含了包的类型和相关证书等参数。plist 文件可借助 Plist 模块来快速生成，也可以先手动打包，生成 ipa 的同时会有一个 ExportOption.plist。
```
from xcodetools import Package

project_path = './demo'

plist = './dev.plist'

ipa_path = '/Users/zhangning/Desktop/IPA/test.ipa'

# 开始自动打包
Package.build (project_path, ipa_path, plist)
```

**XClass**

XClass 模块主要用于编辑 iOS 代码文件，添加内容
```
from xcodetools import Package

class_path = '/Users/zhangning/Desktop/ChannelBridge/Classes/UnityAppController.mm'

file = XClass (class_path)

# 修改 ios 代码文件
file.add_import ('#import <XLSDK/XLApplePay.h>')
```

**Plist**

Plist 模块根据指定参数生成命令行打包所需 Plist 文件，参数说明和获取方式请查看注释
```
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
