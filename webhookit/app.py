# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2017

@author: hustcc
'''
from __future__ import absolute_import
from webhookit import utils, temp, parser
import flask
from flask import Flask
from flask.globals import request
from gevent.wsgi import WSGIServer
from gevent import monkey
import json


__version__ = '0.0.6.dev8'


monkey.patch_all()  # patch
flask_instance = Flask(__name__)


webhook_cnt = 0  # webhook 计数，每次重启都清空
webhook_last = ''
webhook_repo = ''  # webhook hook 哪一个 git 仓库


@flask_instance.route('/')
def index():
    global webhook_cnt, webhook_last, webhook_repo

    config = flask_instance.config.get('WEBHOOKIT_CONFIGURE', None) or {}
    config = utils.filter_sensitive(config)
    return flask.render_template_string(temp.INDEX_HTML_TEMP,
                                        version=__version__,
                                        count=webhook_cnt,
                                        date=webhook_last,
                                        repo=webhook_repo,
                                        config=json.dumps(config,
                                                          indent=4))


@flask_instance.route('/webhookit', methods=['POST', 'GET'])
def webhookit():
    global webhook_cnt, webhook_last, webhook_repo

    data = utils.get_parameter('hook', None)
    if data is None:
        data = request.data
    try:
        data = json.loads(data)  # webhook data
        # webhook configs
        config = flask_instance.config.get('WEBHOOKIT_CONFIGURE', None) or {}

        repo_name = parser.get_repo_name(data) or ''
        repo_branch = parser.get_repo_branch(data) or ''
        webhook_key = '%s/%s' % (repo_name, repo_branch)
        # 需要出发操作的服务器 server 数组
        servers = config.get(webhook_key, [])
        if servers and len(servers) > 0:
            # 存在 server，需要执行 shell 脚本
            cnt = 0
            for s in servers:
                # 遍历执行
                utils.log('Starting to execute %s' % s.get('SCRIPT', ''))
                utils.do_webhook_shell(s, data)
                webhook_cnt += 1
                cnt += 1
                # 更新最后执行的时间
                webhook_last = utils.current_date()
                # 更新最后执行的 git 仓库
                webhook_repo = webhook_key
            t = 'Processed in thread, total %s threads.' % cnt
            return utils.standard_response(True, t)
        else:
            t = ('Not match the repo and branch '
                 'or the webhook servers is not exist: %s') % webhook_key
            utils.log(t)
            return utils.standard_response(False, t)
    except Exception as e:
        t = ('Request trigger traceback: %s') % str(e)
        utils.log(t)
        utils.log(data)
        return utils.standard_response(False, t)


def runserver(port=18340):
    flask_instance.config['PORT'] = port
    # flask_instance.run('0.0.0.0', port, debug=False, threaded=True)
    http_server = WSGIServer(('0.0.0.0', port), flask_instance)
    http_server.serve_forever()


if __name__ == '__main__':
    runserver()
