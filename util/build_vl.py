import glob
import os
from configparser import ConfigParser
from pathlib import Path
from jinja2 import Environment, PackageLoader, FileSystemLoader


def build_VL(config_dict=None, vl_file_path=None,examples_git=None):
    template_env = Environment(
        loader=FileSystemLoader('../templates'),
        trim_blocks=True,
        lstrip_blocks=True)
    template_vl = template_env.get_template('vl.jinja2')
    custom = {}
    shared_volume = {}
    if 'custom' in config_dict:
        custom = config_dict['custom']
    if 'shared_volume' in config_dict:
        shared_volume = config_dict['shared_volume']

    template_vl.stream(vl=config_dict['vl'], auth=config_dict['auth'],
                       github=config_dict['github'], registry=config_dict['registry'],
                       naavre_api_token=config_dict['naavre_api_token'],
                       vre=config_dict['vre'],
                       examples_git=config_dict['examples_git'],
                       search=config_dict['search'],
                       custom=custom,
                       shared_volume=shared_volume) \
        .dump(vl_file_path)


def as_dict(conf=None):
    dictionary = {}
    for section in conf.sections():
        dictionary[section] = {}
        for option in conf.options(section):
            dictionary[section][option] = conf.get(section, option)
    return dictionary


if __name__ == '__main__':
    vls_path = os.path.join(str(Path.home()), 'Downloads', 'envri-community-international-summer-school-2022', 'VLs')
    vls_conf_path = os.path.join(vls_path, 'conf')
    conf_files = glob.glob(vls_conf_path + '/*.ini')
    for conf_file in conf_files:
        vl_name = os.path.basename(conf_file).replace('ini', 'yaml').replace('-conf-', '-')
        vl_file_path = os.path.join(vls_path, 'helm', vl_name)
        config = ConfigParser()
        config.read(conf_file)
        config_dict = as_dict(config)
        build_VL(config_dict, vl_file_path=vl_file_path)
        vl_name = vl_name.replace('.yaml', '')
        print(
            'kubectl create ns ' + vl_name + ' ; helm install shared-volume-' + vl_name.replace('vl-',
                                                                                                '') +
            ' k8s-as-helm/pvc -n ' + vl_name + ' -f ../pvc/vl-pvc.yaml -n ' + vl_name + ' ; helm upgrade --install ' +
            vl_name + ' jupyterhub/jupyterhub -f ' + vl_name + '.yaml -n ' + vl_name+'; kubectl create secret tls HOST-tls --cert=Lets_Encrypt/fullchain.pem --key=Lets_Encrypt/privkey.pem -n '+vl_name)
        # print(
        #     'helm delete ' + vl_name+' -n ' + vl_name)
        # print(
        #     'helm delete shared-volume-' +  vl_name.replace('vl-','') +' -n ' + vl_name)