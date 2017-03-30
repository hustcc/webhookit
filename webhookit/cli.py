# -*- coding: utf-8 -*-
'''
Created on 2017-03-03

@author: hustcc
'''
from __future__ import absolute_import
from tornado.options import define, options, parse_config_file
from webhookit import temp, app
import click
import os


@click.command()
@click.option('-c', '--config', type=click.Path(exists=True),
              help='The web hook configure file path.')
@click.option('-p', '--port', default=18340,
              type=click.INT,
              help='The listening port of HTTP server.')
def webhookit_server_entry(config, port):
    if not config:
        click.echo('webhookit: `config` should not be empty.')
        return

    config_path = os.path.join(os.path.abspath(os.curdir), config)
    # load pyfile configure
    define('WEBHOOKIT_CONFIGURE', type=dict)
    parse_config_file(config_path)
    app.WEBHOOKIT_CONFIGURE = options.WEBHOOKIT_CONFIGURE

    click.echo('webhookit: HTTP Server started. Listening %s...' % port)
    app.runserver(port=port)


def runserver():
    webhookit_server_entry()


@click.command()
def webhookit_config_entry():
    click.echo(temp.CONFIG_TEMP)


def config():
    webhookit_config_entry()


if __name__ == '__main__':
    # config()
    runserver()
