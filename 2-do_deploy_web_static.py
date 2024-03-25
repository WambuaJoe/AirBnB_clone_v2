#!/usr/bin/python3
"""
distributes an archive to web serves using do_deploy function
"""

from fabric.api import *
from os.path import exists
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """distributing function"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, folder_name))
        run('rm /tmp/{}'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'
            .format(folder_name, folder_name))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(folder_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))
        return True
    except Exception as error:
        return False
