from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter
from ghost_stack.preprocessors.output_md5 import OutputMd5Preprocessor

class GhostHTMLExporter(HTMLExporter):

  template_file = "ghost/index.html.j2"

  @property
  def preprocessors(self):     
      return [ OutputMd5Preprocessor ]
        
  @property
  def default_config(self):
    c = Config(
      {
        "OutputMd5Preprocessor" : {
           "prefix" : ""
        },
        "TemplateExporter" : {
          "template_paths" : [
            "/home/dnlennon/Workspace/repos/ghost-stack/templates",
            "/home/dnlennon/.local/share/virtualenvs/python3.11-qW6omolQ/share/jupyter/nbconvert/templates"
          ]
        }
      }
    )
    if super().default_config:
        c2 = super().default_config.copy()
        c2.merge(c)
        c = c2

    return c

  
if __name__ == '__main__':
  from traitlets.config import Config
  from ghost_stack.exporters.ghost_html_exporter import GhostHTMLExporter
  from nbconvert.writers.files import FilesWriter
  
  import nbformat
  import json
  from pathlib import Path

  # import a logger and send it to stdout
  # import logging, sys
  # from traitlets import log
  # logger = log.get_logger()
  # logger.setLevel(10)
  # handler = logging.StreamHandler(sys.stdout)
  # logger.addHandler(handler)
  
  notebook = "hessenberg"
  ipynb = f"{notebook}.ipynb"

  build_directory = Path("/home/dnlennon/Workspace/repos/ghost-data/staging/notebooks")
  output_files_dir = Path("content/images") / notebook

  with open(build_directory / ipynb, "r") as f:
    nbdata = f.read()
  nbjson = json.loads(nbdata)

  nb_content = nbformat.reads(nbdata, as_version = nbjson['nbformat'])

  c = Config()
  # c.OutputMd5Preprocessor.prefix = "localhost:2368"
  c.FilesWriter.build_directory = str(build_directory)
  
  exporter = GhostHTMLExporter(config = c)
  resources = {
     "output_files_dir" : output_files_dir
  }
  (body, resources) = exporter.from_notebook_node(nb_content, resources)

  writer = FilesWriter(config = c)
  writer.write(body, resources, notebook_name = notebook)


  
  
