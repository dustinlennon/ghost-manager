from nbconvert.preprocessors import ExtractOutputPreprocessor
import yaml
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper
import re

class ExtractYamlPreprocessor(ExtractOutputPreprocessor):
  def preprocess_cell(self, cell, resources, cell_index):    
    if cell['cell_type'] == "raw" and cell_index == 0:
      src = cell['source']

      m = re.match(r"^---(\n.*)\n---$", src, re.DOTALL)

      try:
        content = m.group(1)
        resources['yaml_header'] = yaml.load(content, yaml.BaseLoader)
      except AttributeError:
        resources['yaml_header'] = dict()
    
    return cell, resources
  