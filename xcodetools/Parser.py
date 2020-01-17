import configparser
import os

class Parser(configparser.ConfigParser):

    '''
    ini文件解析
    '''
    
    @classmethod
    def load(cls,path):
        abspath = os.path.abspath(path)
        if not os.path.exists(abspath):
            raise('配置文件不存在')

        a = Parser()
        a.read(abspath)
        return a
        
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
        
    def optionxform(self, optionstr):
        return optionstr