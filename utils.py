import os
import yaml
import click
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

ROOT_DIR = BASE_DIR = application_path

def get_conf(section=None):
    path_file = os.path.join(ROOT_DIR, "conf.yaml")
    click.echo("try to open {}".format(path_file))
    if not os.path.exists(path_file):
        raise Exception("File  {} not found".format(path_file))
    content = yaml.load(open(path_file).read())
    if not section:
        return content
    else:
        return content.get(section)


if __name__ == '__main__':
    get_conf()
    pass