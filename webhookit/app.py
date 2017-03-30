# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2017

@author: hustcc
'''
from __future__ import absolute_import
from webhookit import utils, temp, parser
import json
import tornado.ioloop
import tornado.web
import tornado.template


__version__ = '0.0.7.dev1'

webhook_cnt = 0  # webhook 计数，每次重启都清空
webhook_last = ''
webhook_repo = ''  # webhook hook 哪一个 git 仓库
WEBHOOKIT_CONFIGURE = None


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        global webhook_cnt, webhook_last, webhook_repo, WEBHOOKIT_CONFIGURE
        config = WEBHOOKIT_CONFIGURE or {}
        config = utils.filter_sensitive(config)
        t = tornado.template.Template(temp.INDEX_HTML_TEMP)
        self.write(t.generate(version=__version__,
                              count=webhook_cnt,
                              date=webhook_last,
                              repo=webhook_repo,
                              config=json.dumps(config,
                                                indent=4)))


class WebhookitHandler(tornado.web.RequestHandler):
    def post(self):
        global webhook_cnt, webhook_last, webhook_repo, WEBHOOKIT_CONFIGURE
        # gitosc: hook, github(application/x-www-form-urlencoded): payload
        data = self.get_argument('hook', self.get_argument('payload', None))
        if data is None:
            # gitlab and github(application/json)
            data = self.request.body or None
        try:
            data = json.loads(data)  # webhook data
            # webhook configs
            config = WEBHOOKIT_CONFIGURE or {}

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
                self.write(utils.standard_response(True, t))
            else:
                t = ('Not match the repo and branch '
                     'or the webhook servers is not exist: %s') % webhook_key
                utils.log(t)
                self.write(utils.standard_response(False, t))
        except Exception as e:
            t = ('Request trigger traceback: %s') % str(e)
            utils.log(t)
            utils.log('data is %s.' % (data or None))
            self.write(utils.standard_response(False, t))

    def get(self):
        return self.post()


application = tornado.web.Application([
    (r"/", IndexPageHandler),
    (r"/webhookit", WebhookitHandler),
])


def runserver(port=18340):
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    runserver()
