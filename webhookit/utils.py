# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2017

@author: hustcc
'''
from flask.globals import request
from functools import wraps
from threading import Thread
import json
import click
import datetime
import copy


# get / post data
def get_parameter(key, default=None):
    # post参数
    if request.method == 'POST':
        param = request.form.get(key, default)
    # get
    elif request.method == 'GET':
        param = request.args.get(key, default)
    else:
        return default
    return param


def standard_response(success, data):
    '''standard response
    '''
    rst = {}
    rst['success'] = success
    rst['data'] = data
    return json.dumps(rst)


def async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
    return wrapper


# log
def log(t):
    click.echo('%s: %s' % (current_date(), t))


def current_date():
    return datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")


# 过滤服务器配置信息的敏感信息
def filter_sensitive(config):
    config = copy.deepcopy(config)
    for v in config.values():
        for server in v:
            if is_remote_server(server):
                server['HOST'] = '***.***.***.***'
                server['PORT'] = '****'
                server['USER'] = '*******'
                server['PWD'] = '*******'
    return config


# if host port user pwd all is not empty, then it is a remote server.
def is_remote_server(s):
    # all is not empty or zero, then remote server
    return all([s.get('HOST', None),
                s.get('PORT', None),
                s.get('USER', None),
                s.get('PWD', None)])


# ssh to exec cmd
def do_ssh_cmd(ip, port, account, pkey, shell, push_data='', timeout=300):
    import paramiko
    import StringIO

    def is_msg_success(msg):
        for x in ['fatal', 'fail', 'error']:
            if msg.startswith(x) or msg.endswith(x):
                return False
        return True

    try:
        port = int(port)
    except:
        port = 22

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 首先以 ssh 密钥方式登陆
        pkey_file = StringIO.StringIO(pkey.strip() + '\n')  # 注意最后有一个换行
        private_key = paramiko.RSAKey.from_private_key(pkey_file)
        s.connect(ip, port, account, pkey=private_key, timeout=10)
        pkey_file.close()
    except:
        # 如果出现异常，则使用 用户密码登陆的方式
        s.connect(ip, port, account, password=pkey, timeout=10)

#     if push_data:
#     shell = shell + (" '%s'" % push_data)
    shell = shell.split('\n')
    shell = [sh for sh in shell if sh.strip()]
    shell = ' && '.join(shell)

    stdin, stdout, stderr = s.exec_command(shell, timeout=timeout)

    msg = stdout.read()
    err = stderr.read()

    success = True
    if not msg and err:
        success = False
        msg = err

    s.close()

    if success:
        success = is_msg_success(msg)

    return (success, msg)


# 使用线程来异步执行
@async
def do_webhook_shell(server, data):
    log('Start to process server: %s' % json.dumps(server))
    script = server.get('SCRIPT', '')
    if script:
        if is_remote_server(server):
            # ip, port, account, pkey, shell, push_data='', timeout=300
            log('Start to execute remote SSH command. %s' % script)
            (success, msg) = do_ssh_cmd(server.get('HOST', None),
                                        server.get('PORT', 0),
                                        server.get('USER', None),
                                        server.get('PWD', None),
                                        server.get('SCRIPT', ''),
                                        data)
        else:
            log('Start to execute local command. %s' % script)
            import commands
            # local
            (success, msg) = commands.getstatusoutput(server.get('SCRIPT', ''))
            success = success > 0 and False or True
    else:
        success = False
        msg = 'There is no SCRIPT configured.'
    # end exec, log data
    log('Completed execute: (%s, %s)' % (success, msg))
    return True
