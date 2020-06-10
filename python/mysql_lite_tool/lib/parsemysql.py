#!/usr/bin/env python
# encoding: utf-8

from ConfigParser import ConfigParser
import os

class MysqlConfig(ConfigParser):
    def __init__(self, config_file, **kwargs):
        ConfigParser.__init__(self, allow_no_value=True)
        #super(MysqlConfig, self).__init__(allow_no_value=True)
        self.mysqld_vars_dict = {}
        self.config_file = config_file
        self.kwargs = kwargs
        self.set_mysqld_vars(self.kwargs)
        if os.path.exists(self.config_file):
        # 初始化时就执行读取配置文件操作
            self.read(self.config_file)
            self.get_mysqld_vars()
        else:
            self.get_default_mysqld_vars()
         
    def set_mysqld_vars(self, kwargs):
        "设置类属性"
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.mysqld_vars_dict[k] = v

    def set_var(self, key, value):
        """主要用于接收没有value的选项，比如skip-slave-start"""
        self.mysqld_vars_dict[key] = value

    def get_mysqld_vars(self, section='mysqld'):
        """读取配置文件的参数存为类属性，默认是mysqld"""
        attr_dict = {}
        options = self.options(section)
        for item in options:
            attr_dict[item] = self.get(section, item)
        self.set_mysqld_vars(attr_dict)

    def save(self):
        if not self.has_section('mysqld'):
            self.add_section('mysqld')
        for k, v in self.mysqld_vars_dict.items():
            self.set('mysqld', k, v)
        with open(self.config_file, 'w') as fd:
            self.write(fd)    

    def get_default_mysqld_vars(self):
        defaults = {
             'key_buffer_size':'256M',
             'max_allowed_packet':'1M',
             'table_open_cache':'256',
             'sort_buffer_size':'1M',
             'read_buffer_size':'1M',
             'read_rnd_buffer_size':'4M',
             'myisam_sort_buffer_size':'64M',
             'thread_cache_size':'8',
             'query_cache_size':'16M',
             'thread_concurrency':'8',
             'user':'mysql',
             'character-set-server': 'utf8'
                   }
        self.set_mysqld_vars(defaults)

if __name__ == '__main__':
    conf_obj = MysqlConfig('/mysql/config/my01.cnf')
    #print conf_obj.get('mysqld', 'port')
    #conf_obj.set_var('port',3307)
    #conf_obj.set_var('skip-slave-start', None)
    conf_obj.save()
    for k, v in conf_obj.mysqld_vars_dict.items():
        print k, v
    print conf_obj.port
    print conf_obj.config_file
    print conf_obj.mysqld_vars_dict.items()
    print conf_obj.options('mysqld')
