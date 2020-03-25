### 环境要求
- Xcode 11
- Python 3

**安装 python 3**

```
brew install python3
```

**如果提示没有 brew 环境，先执行下面命令安装 brew**

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

**python3 安装后，执行下面命令安装依赖包**

```
pip3 install future
pip3 install openstep_parser
```

**可能遇到的错误**

```
xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
```

**解决办法**

```
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer/
```
