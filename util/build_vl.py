import os
from configparser import ConfigParser
from pathlib import Path
from jinja2 import Environment, PackageLoader, FileSystemLoader


def build(config_dict=None,vl_file_path=None):
    template_env = Environment(
        loader=FileSystemLoader('../templates'),
        trim_blocks=True,
        lstrip_blocks=True)
    template_vl = template_env.get_template('vl.jinja2')
    print(config_dict['vl']['base_url'])
    template_vl.stream(vl=config_dict['vl'], auth=config_dict['auth']) \
        .dump(vl_file_path)


def as_dict(conf=None):
    dictionary = {}
    for section in conf.sections():
        dictionary[section] = {}
        for option in conf.options(section):
            dictionary[section][option] = conf.get(section, option)
    return dictionary


if __name__ == '__main__':
    input_conf_file = os.path.join(str(Path.home()), 'Downloads', 'vl-conf.ini')
    vl_file_path = os.path.join(str(Path.home()), 'Downloads', 'vl.yaml')
    config = ConfigParser()
    config.read(input_conf_file)
    config_dict = as_dict(config)
    build(config_dict,vl_file_path=vl_file_path)
