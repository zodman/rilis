import os
import yaml
import click
import sys
ROOT_DIR = BASE_DIR = os.path.dirname(sys.argv[0])

def get_conf(section=None):
    path_file = os.path.join(ROOT_DIR, "conf.yaml")
    click.echo("try to open {}".format(path_file))
    if not os.path.exists(path_file):
        raise Exception("File  yaml not found")
    content = yaml.load(open(path_file).read())
    if not section:
        return content
    else:
        return content.get(section)


if __name__ == '__main__':
    get_conf()
    pass