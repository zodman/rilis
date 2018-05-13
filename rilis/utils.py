import os
import yaml
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

def get_conf(section=None):
    path_file = os.path.join(ROOT_DIR, "conf.yaml")
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