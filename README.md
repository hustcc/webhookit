# webhookit

> A simple cli tool to create http server for git webhook, **GitHub**, **GitLab**, **GitOsc**, **Gogs** are all supported.

[![Latest Stable Version](https://img.shields.io/pypi/v/webhookit.svg)](https://pypi.python.org/pypi/webhookit) [![Build Status](https://travis-ci.org/hustcc/webhookit.svg?branch=master)](https://travis-ci.org/hustcc/webhookit) ![GitHub](http://shields.hust.cc/Supported-GitHub-brightgreen.svg) ![GitLab](http://shields.hust.cc/Supported-GitLab-green.svg) ![GitOsc](http://shields.hust.cc/Supported-GitOsc-blue.svg) ![Gogs](http://shields.hust.cc/Supported-Gogs-yellowgreen.svg)


# 1. Install

> **pip install webhookit**

Python 2 / 3 are all supported. After install, you can get two commands named `webhookit` and `webhookit_config` in your system.


# 2. Usage

Run `webhookit --help` to get help content of the command. Help content below:


```sh
# webhookit --help
Usage: webhookit [OPTIONS]

Options:
  -c, --config PATH      The web hook configure file path.
  -p, --port INTEGER     The listening port of HTTP server.
  --help                 Show this message and exit.
```

Run **`webhookit_config`** to get the config template strings.

Run **`webhookit -c config.py -p 18340`**  to start the http server for git webhook.


# 3. Example

Here is an simple example to run the `webhookit` http server.

```sh
# 1. install webhookit
pip install webhookit

# 2. initial a webhookit config file
webhookit_config > /home/hustcc/webhook-configs/config4hustcc.py

# 3. update config4hustcc.py with your own config and save
vim config4hustcc.py

# 4. run webhookit http server
webhookit -c config4hustcc.py
```

Then open `http://host:18340` in your browser, can see: 

1. The webhook status.
2. The webhook url.
3. The webhook server configures.


# 4. configure file

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

The python var name `WEBHOOKIT_CONFIGURE` can not be modified.

Each webhook has it's key with format of `'repo_name/branch_name'`, Each webhook can trigger a group of servers, which is the value of the key.

Server can be remote and local, if local, keep `HOST`, `PORT`, `USER`, `PWD` be empty.


# 5. License

MIT@[hustcc](https://github.com/hustcc).



