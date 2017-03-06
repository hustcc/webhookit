# -*- coding: utf-8 -*-
'''
Created on 2017-03-03

@author: hustcc
'''

import click
import app
import os
import temp


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
    app.flask_instance.config.from_pyfile(config_path)
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
