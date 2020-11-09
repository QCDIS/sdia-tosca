import os
import unittest
from builtins import filter
from toscaparser.tosca_template import ToscaTemplate
import yaml
import logging

logger = logging.getLogger(__name__)
if not getattr(logger, 'handler_set', None):
    logger.setLevel(logging.INFO)
h = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)
logger.handler_set = True

class TestTosca(unittest.TestCase):
    def test(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))

        tosca_path =  os.path.join(cur_dir, '../examples')
        files = self.get_files(tosca_path)
        for file in files:
            logger.info('Testing: ' +file)
            tosca_template_dict = self.get_tosca_file_file(file)

            tt = ToscaTemplate(yaml_dict_tpl=tosca_template_dict)
        pass

    def get_files(self,dir_mame):
        listOfFile = os.listdir(dir_mame)
        completeFileList = []
        for file in listOfFile:
            completePath = os.path.join(dir_mame, file)
            if os.path.isdir(completePath):
                completeFileList = completeFileList + self.getFiles(completePath)
            else:
                completeFileList.append(completePath)

        return completeFileList


    def get_tosca_file_file(self, path):
        input_tosca_file_path = path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.assertEqual(True, os.path.exists(input_tosca_file_path),
                         'Starting from: ' + dir_path + ' Input TOSCA file: ' + input_tosca_file_path + ' not found')

        with open(input_tosca_file_path, 'r') as file:
            contents = file.read()
        return yaml.safe_load(contents)


if __name__ == '__main__':
    import unittest

    unittest.main()
