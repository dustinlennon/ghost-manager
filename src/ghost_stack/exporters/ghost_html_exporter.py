from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter
from ghost_stack.preprocessors.output_md5 import OutputMd5Preprocessor
from ghost_stack.preprocessors.extract_yaml import ExtractYamlPreprocessor

class GhostHTMLExporter(HTMLExporter):

  # template_file = "ghost/index.html.j2"
  template_name = "ghost"

  @property
  def preprocessors(self):     
      return [ ExtractYamlPreprocessor, OutputMd5Preprocessor ]
        
  @property
  def default_config(self):
    c = Config(
      {
        "OutputMd5Preprocessor" : {
           "prefix" : ""
        }
      }
    )
    if super().default_config:
        c2 = super().default_config.copy()
        c2.merge(c)
        c = c2

    return c

