#!/usr/bin/python3
""" deploy code to the server """
import os.path
from fabric.api import env, put, run, local
from datetime import datetime


env.hosts = ["18.234.168.215", "52.72.71.162"]


def do_pack():
    """ pack web_static folder into a .tgz file """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """ Distributes an archive to web servers
    Args:
        archive_path(str): Path to the archive to distribute
    Return: True if succeed otherwise false """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run(
            "rm -rf /data/web_static/releases/{}/".format(
                name)).failed is True:
        return False
    if run(
            "mkdir -p /data/web_static/releases/{}/".format(
                name)).failed is True:
        return False
    if run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run(
            "rm -rf /data/web_static/releases/{}/web_static".format(
                name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(name)).failed is True:
        return False
    return True


def deploy():
    """ archive and deploy to web severs """
    f = do_pack()
    if f is None:
        return False
    return do_deploy(f)
