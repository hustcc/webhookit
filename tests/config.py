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
        # The webhook shell script path.
        'SCRIPT': '/home/hustcc/exec_hook_shell.sh'
    }, {
        # if exec shell on local server, keep empty.
        'HOST': '10.240.121.12',  # will exec shell on which server.
        'PORT': '21',  # ssh port, default is 22.
        'USER': 'hustcc',  # linux user name
        'PWD': 'hustcc_pwd',  # user password or private key.

        # The webhook shell script path.
        'SCRIPT': '/home/hustcc/exec_hook_shell.sh'
    }]
}
