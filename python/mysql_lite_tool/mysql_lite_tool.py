#!/usr/bin/env python
# encoding: utf-8
# python 3-
"""这个脚本用于管理mysql，可以实现创建mysql实例，mysql主从，参数调整，备份，恢复功能"""
import os
import sys
import shlex
import time
from subprocess import Popen, PIPE
import MySQLdb

"""
脚本退出状态码说明
1 正常退出
2 文件不存在
3 IndexError
4 KeyError
5 文件已经存在

11 mysql实例已经存在
12 mysql端口已经存在
13 连接mysql失败
"""

# current_dir = os.path.dirname(__file__)
# current_lib_dir = os.path.abspath(os.path.join(current_dir, 'lib'))
# sys.path.append(current_lib_dir)
# 将当前lib加入sys.path中
CURRENT_DIR = sys.path[0]
CURRENT_LIB_DIR = os.path.join(CURRENT_DIR, 'lib')
sys.path.append(CURRENT_LIB_DIR)

from optparse import OptionParser
from parsemysql import MysqlConfig
# 单位格式化 1024k --> 1M
from chto import chto

MYSQL_DATA_DIR = '/mysql/data/'
MYSQL_CONF_DIR = '/mysql/config/'
MYSQL_BACKUP_DIR = '/mysql/backup/'
REPLICATION_USER = 'repl'
REPLICATION_PASS = 'mysql@123'
MYSQL_CNF = None
# MYSQL_PORT = None
INSTANCE_NAME = None
INSTANCE_PORT = None
INSTANCE_COMMAND = None


def opt():
    # usage = "%prog [option] "
    parser = OptionParser()
    parser.add_option('-n', '--name',
                      dest='name',
                      action='store',
                      default='myinstance',
                      )
    parser.add_option('-p', '--port',
                      dest='port',
                      action='store',
                      default='3306',
                      )
    parser.add_option('-c', '--create',
                      dest='command',
                      action='store',
                      default='check',
                      )
    return parser.parse_args()


def _init():
    """初始化目录"""
    # 初始化配置文件目录
    if not os.path.exists(MYSQL_CONF_DIR):
        os.makedirs(MYSQL_CONF_DIR)
    # 初始化数据文件目录
    if not os.path.exists(MYSQL_DATA_DIR):
        os.makedirs(MYSQL_DATA_DIR)
    # 初始化备份文件目录
    if not os.path.exists(MYSQL_BACKUP_DIR):
        os.makedirs(MYSQL_BACKUP_DIR)
    options, args = opt()
    global INSTANCE_NAME
    INSTANCE_NAME = options.name
    global INSTANCE_PORT
    INSTANCE_PORT = int(options.port)
    global INSTANCE_COMMAND
    INSTANCE_COMMAND = options.command


def _isCnfExist():
    # 检测配置文件是否存在
    if os.path.exists(MYSQL_CNF):
        pass
    else:
        print 'Config File %s is not existed.'
        sys.exit(2)

    # global MYSQL_PORT
    # obj = MysqlConfig(MYSQL_CNF)
    # if 'port' in obj.mysqld_vars_dict:
    #     MYSQL_PORT = int(obj.mysqld_vars_dict['port'])
    # else:
    #     print 'The Port is not existed in %s' % MYSQL_CNF
    #     sys.exit(4)


def _getCnfPath():
    """在创建时，没有配置文件，只有读取配置文件时生效"""
    global MYSQL_CNF
    MYSQL_CNF = os.path.join(MYSQL_CONF_DIR, '%s.cnf' % INSTANCE_NAME)


"""create section"""
def _checkInstanceExist():
    """根据配置文件名称，确定实例是否已经存在"""
    all_configs_list = _getAllConfigsList()
    exists_instance_name = [item.split('/')[-1][:-4] for item in all_configs_list]
    if INSTANCE_NAME in exists_instance_name:
        print >> sys.stderr, 'instance %s is exists' % INSTANCE_NAME
        sys.exit(11)


def _getAllConfigsList():
    """产生所有配置文件列表"""
    import glob
    all_configs_list = glob.glob(MYSQL_CONF_DIR + '*.cnf')
    return all_configs_list


def _checkPortExist():
    all_configs_list = _getAllConfigsList()
    exist_port_list = []
    for config in all_configs_list:
        obj = MysqlConfig(config)
        port = obj.mysqld_vars_dict['port']
        exist_port_list.append(port)
    if INSTANCE_PORT in exist_port_list:
        print >> sys.stderr, 'port %s is exists' % INSTANCE_PORT
        sys.exit(12)


def _genDict():
    """需要单独定义的配置文件选项"""
    return {
        'pid-file': os.path.join(MYSQL_DATA_DIR, INSTANCE_NAME, '%s.pid' % INSTANCE_NAME),
        'socket': '/tmp/%s.sock' % INSTANCE_NAME,
        'port': INSTANCE_PORT,
        'datadir': '%s/' % os.path.join(MYSQL_DATA_DIR, INSTANCE_NAME),
        'log-error': os.path.join(MYSQL_DATA_DIR, INSTANCE_NAME, '%s.log' % INSTANCE_NAME)
    }


def _genNewConfig(**kwargs):
    """将附加选项添加到配置文件"""
    addons_conf_dict = _genDict()
    addons_conf_dict.update(kwargs)
    config_obj = MysqlConfig(MYSQL_CNF, **addons_conf_dict)
    config_obj.save()


def _genDataDir():
    data_dir = os.path.join(MYSQL_DATA_DIR, INSTANCE_NAME)
    if os.path.exists(data_dir):
        print 'datadir %s is existed' % data_dir
        sys.exit()
    else:
        os.makedirs(data_dir)
        os.system('chown mysql:mysql %s' % data_dir)


def _install_mysql():
    """初始化MYSQL到指定目录"""
    cmd = "mysql_install_db --defaults-file=%s" % MYSQL_CNF
    #print cmd
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    p.communicate()
    return p.returncode


def _run_mysql():
    cmd = "mysqld_safe --defaults-file=%s" % MYSQL_CNF
    # 这两种情况都可以正常运行
    # p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    time.sleep(3)
    # no return
    # return p.returncode
    return 1


def createInstance(**kwargs):
    _checkInstanceExist()
    _checkPortExist()
    _genDataDir()
    _genNewConfig(**kwargs)
    # print _install_mysql(NAME)
    # print "The %s is created" % NAME
    # print _run_mysql(NAME)
    # print "Mysql %s has started now." % NAME
    if not _install_mysql():
        print "The %s is created" % INSTANCE_NAME
        if _run_mysql():
            print "Mysql %s has started now." % INSTANCE_NAME
        else:
            print "Mysql %s can't start with error." % INSTANCE_NAME
    else:
        print "The %s is not created with error." % INSTANCE_NAME


def recovery(sql_file, **kwargs):
    """全量恢复"""
    createInstance(**kwargs)
    cmd = 'mysql -h 127.0.0.1 -P %s -u root --password="" < %s' % (INSTANCE_PORT, sql_file)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    p.communicate()
    p.returncode


"""backup section"""

def backup():
    """全量备份"""
    import datetime
    now = datetime.datetime.now()
    backup_time = now.strftime('%Y-%m-%d.%H-%M-%S')
    backup_dir = os.path.join(MYSQL_BACKUP_DIR, INSTANCE_NAME)
    print backup_dir
    if os.path.exists(backup_dir):
        pass
    else:
        os.makedirs(backup_dir)

    backup_file = os.path.join(backup_dir, backup_time)
    cmd = """mysqldump --events --ignore-table=mysql.user --lock-all-tables --flush-logs --all-databases \
    --master-data=1 --host=127.0.0.1 --port=%s --user=root --password="" > %s.sql""" % (INSTANCE_PORT, backup_file)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    # 正常情况下，这里的stdout, stderr都为空，当stderr有值时，说明备份出错，否则非分成功
    #print stderr
    if stderr:
        print 'backup failed.'
    else:
        print 'backup %s OK.' % INSTANCE_NAME


"""diff section"""
def _get_global_variables():
    cursor = _connect_mysql()
    sql = 'show global variables;'
    cursor.execute(sql)
    global_variables_dict = dict(cursor.fetchall())
    return global_variables_dict


def _is_legal_options(option):
    global_variables_dict = _get_global_variables()
    other_variables_list = ['skip-slave-start']
    if option in global_variables_dict or option in other_variables_list:
        return True
    else:
        print global_variables_dict
        return False


def diff_variables():
    mysql_global_variables = _get_global_variables()
    format_mysql_global_variables = {}
    for k, v in mysql_global_variables.items():
        if v and 'port' not in k:
            format_mysql_global_variables[k] = chto(v)
            # format_mysql_global_variables[k] = v
        else:
            format_mysql_global_variables[k] = v
    # print format_mysql_global_variables
    config_obj = MysqlConfig(MYSQL_CNF)
    # print config_obj.mysqld_vars_dict
    for k, v in config_obj.mysqld_vars_dict.items():
        k = k.replace('-', '_')
        if k in format_mysql_global_variables and v != format_mysql_global_variables[k]:
            print k, v, format_mysql_global_variables[k]
        else:
            pass


"""adjust section"""
def set_variables(k, v):
    config_obj = MysqlConfig(MYSQL_CNF)
    if _is_legal_options(k):
        config_obj.set_var(k, v)
        config_obj.save()
    else:
        print 'Option %s is illegal.' % k


def adjust_variables(args):
    if len(args) == 1:
        k = args[0]
        v = None
    elif len(args) == 2:
        k = args[0]
        v = args[1]
    else:
        print "args number is 1 or 2"
        sys.exit(2)
    set_variables(k, v)


def _connect_mysql(host='127.0.0.1', user='root', passwd=''):
    try:
        print host, user, passwd, INSTANCE_PORT
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=INSTANCE_PORT)
    except:
        print 'Connect mysql failed.'
        sys.exit(13)
    else:
        cursor = conn.cursor()
        return cursor


def _grant_repl_user():
    sql = "grant replication slave on *.* to %s@'%%' identified by '%s'" % (REPLICATION_USER, REPLICATION_PASS)
    cursor = _connect_mysql()
    cursor.execute(sql)
    cursor.close()

def _changeMaster(host, port, user, password):
    """主从复制时使用"""
    sql = """change master to master_host = '%s',
    master_port = %s,
    master_user = '%s',
    master_password = '%s';""" % (host, port, user, password)
    #print sql
    cursor = _connect_mysql()
    cursor.execute(sql)
    cursor.close()

def _change2master(host, port, user, password, log_file, log_pos):
    """备份回复时使用"""
    sql = """change master to master_host = '%s',
    master_port = %s,
    master_user = '%s',
    master_password = '%s',
    master_log_file = '%s',
    master_log_pos = %s;""" % (host, port, user, password, log_file, log_pos)
    #print sql
    cursor = _connect_mysql()
    cursor.execute(sql)
    cursor.close()

def _getPosAndBinlog(sql_file):
    import re
    r = re.compile(r"CHANGE MASTER TO MASTER_LOG_FILE='(\S+)', MASTER_LOG_POS=(\d+);")
    with open(sql_file, 'r') as fd:
        for line in fd:
            if r.search(line):
                result = r.search(line)
                break
        else:
            print "can't find bin-log and postion in %s" % sql_file
            sys.exit(2)
    print result.groups()
    return result.group(1), int(result.group(2))

if __name__ == '__main__':
    _init()
    _getCnfPath()
    options, args = opt()
    if INSTANCE_COMMAND == 'create':
        if not args:
            print "create database %s ..." % INSTANCE_NAME
            """参数格式
            python mysql-tool -n instance_name -p port -c create"""
            createInstance()
        else:
            dbtype = args[0]
            server_id = args[1]
            repl_options = {'server-id': server_id}
            if dbtype == 'master':
                """参数格式
                python mysql-tool -n instance_name -p port -c create master server-id"""
                print 'create database master ...'
                repl_options['log-bin'] = 'mysql-bin'
                createInstance(**repl_options)
                _grant_repl_user()
            if dbtype == 'slave':
                """参数格式，远程主机同样适用
                python mysql-tool -n instance_name -p port -c create slave server-id master-host master-port"""
                print 'create database slave ...'
                repl_options['skip-slave-start'] = None
                repl_options['replicate-ignore-db'] = 'mysql'
                createInstance(**repl_options)
                master_host = args[2]
                master_port = args[3]
                master_user = REPLICATION_USER
                master_password = REPLICATION_PASS
                _changeMaster(master_host, master_port, master_user, master_password)

    elif INSTANCE_COMMAND == 'check':
        """参数格式
        python mysql-tool -n instance_name -p port -c check"""
        # 初始化cnf和port
        _isCnfExist()
        print 'checking ...'
        diff_variables()

    elif INSTANCE_COMMAND == 'adjust':
        """参数格式
        """
        # 初始化cnf和port
        _isCnfExist()
        print 'adjusting...'
        adjust_variables(args)

    elif INSTANCE_COMMAND == 'backup':
        # 初始化cnf和port
        print 'backup...'
        _isCnfExist()
        backup()

    elif INSTANCE_COMMAND == 'recovery':
        """ 参数格式：
        python recovery.py -n instance_name -p port -c recovery server_id master_host master_port sql_file"""
        # 初始化cnf和port
        server_id = args[0]
        sql_file = args[3]
        repl_options = {'server-id': server_id}
        repl_options['skip-slave-start'] = None
        repl_options['replicate-ignore-db'] = 'mysql'
        print 'recovery...'
        recovery(sql_file, **repl_options)

        master_host = args[1]
        master_port = args[2]
        master_user = REPLICATION_USER
        master_password = REPLICATION_PASS
        master_log_file, master_log_pos = _getPosAndBinlog(sql_file)
        print master_log_file, master_log_pos
        _change2master(master_host, master_port, master_user, master_password, master_log_file, master_log_pos)
