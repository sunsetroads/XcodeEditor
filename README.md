## XcodeEditor 
一套 Xcode 脚本工具集，用于自动化配置 Xcode 和导出 ipa 包。

Xcode 配置包括对工程中 General、Capability、Info、Build Settgings、Build Phases 相关参数的修改，以及添加文件和系统库。

此脚本比较适用于 Untiy 开发自动化打 iOS 包，[这里](https://sunsetroads.github.io/2019/11/11/untiy-export-ipa/) 可以查看从 Untiy 工程到 iOS 包的整个自动化配置流程。

#### [安装说明](./INSTALL.md)

### 快速开始

安装完成后，进入脚本配置一下 tesh.sh 然后执行，之后就可以去 Xcode 工程中检查你的配置是否生效：
```
# .ini 包含了对 Xcode 各项设置的配置
ini='./test.ini'

# Xcode 工程路径
project='./demo'

# 手动打包时生成的 ExportOption.plsit
plist='./dev.plist'

# 最终生成的 ipa 路径
ipapath='/Users/zhangning/Desktop/package/test.ipa'

python3 ./test.py ${ini} ${project} ${ipapath} ${plist}
```

### 模块说明

**Xcode**

Xcode 模块会根据配置文件修改 Xcode 中的相关参数，配置规则在 [test.ini](./test.ini) 文件中有详细说明，使用时要根据需求加以修改。
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
