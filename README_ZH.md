# webhookit

> 一个极简的命令行版本的 git webhok，部署容易，非常简单就可以部署一个 webhook server。支持**GitHub**, **GitLab**, **GitOsc**, **Gogs**, **Coding**。Python 2 / 3 都支持。

[在线实例展示](http://webhookit.hust.cc) | [English README](README.md)

[![Latest Stable Version](https://img.shields.io/pypi/v/webhookit.svg)](https://pypi.python.org/pypi/webhookit) [![Build Status](https://travis-ci.org/hustcc/webhookit.svg?branch=master)](https://travis-ci.org/hustcc/webhookit) ![GitHub](http://shields.hust.cc/Supported-GitHub-brightgreen.svg) ![GitLab](http://shields.hust.cc/Supported-GitLab-green.svg) ![GitOsc](http://shields.hust.cc/Supported-GitOsc-blue.svg) ![Gogs](http://shields.hust.cc/Supported-Gogs-yellowgreen.svg) ![Coding](http://shields.hust.cc/Supported-Coding-yellow.svg)


# 1. 安装

> **pip install webhookit**

支持 Python 2 / 3。安装之后，在系统中可以得到两个命令工具：`webhookit` and `webhookit_config`。


# 2. 使用

运行 `webhookit --help` 可以得到命令的帮助信息，具体的信息如下：

```sh
# webhookit --help
Usage: webhookit [OPTIONS]

Options:
  -c, --config PATH      The web hook configure file path.
  -p, --port INTEGER     The listening port of HTTP server.
  --help                 Show this message and exit.
```

运行 **`webhookit_config`** 可以得到工具配置的模版内容。

运行 **`webhookit -c config.py -p 18340`** 开启一个 webhook 的 http 服务器。


# 3. 一个示例

下面是一个简单的例子，用来展示如何使用本工具：

```sh
# 1. 安装 webhookit
pip install webhookit

# 2. 初始化一个配置模版
webhookit_config > /home/hustcc/webhook-configs/config4hustcc.py

# 3. 更新 config4hustcc.py 配置内容
vim config4hustcc.py

# 4. 运行 http server
webhookit -c config4hustcc.py
```

然后在浏览器中打开 `http://host:18340` 就可以看到下面的一些信息了：

1. webhook 执行的状态；
2. webhook 的 URL 地址；
3. webhook 的配置信息（隐藏私密信息）；


# 4. 配置文件说明

```py
# -*- coding: utf-8 -*-
'''
Created on Mar-03-17 15:14:34
@author: hustcc/webhookit
'''

# This means:
# When get a webhook request from `repo_name` on branch `branch_name`,
# will exec SCRIPT on servers config in the array.
WEBHOOKIT_CONFIGURE = {
    # a web hook request can trigger multiple servers.
    'repo_name/branch_name': [{
        # if exec shell on local server, keep empty.
        'HOST': '',  # will exec shell on which server.
        'PORT': '',  # ssh port, default is 22.
        'USER': '',  # linux user name
        'PWD': '',  # user password or private key.

        # The webhook shell script path.
        'SCRIPT': '/home/hustcc/exec_hook_shell.sh'
    }, 
	...],
	...
}
```

Python 变量名 `WEBHOOKIT_CONFIGURE` 不要去修改。

每个 webhook 都用仓库的名字和分支名字 `'repo_name/branch_name'` 作为它的键值，每个 webhook 可以触发一组服务器，这些服务器的配置信息存储在一个数组中。

服务器可以是远程的服务器，也可以是本地机器，如果要触发本机的脚本运行，那么请保持 `HOST`, `PORT`, `USER`, `PWD` 这些配置为空，或者不存在这些键值。


# 5. License

MIT@[hustcc](https://github.com/hustcc).



