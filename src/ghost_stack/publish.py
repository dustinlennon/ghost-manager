import logging
import sys, os
from typing import Optional
from pathlib import Path

import argparse
import nbformat

import json

from dataclasses import dataclass
from traitlets import log
from traitlets.config import Config

from ghost_stack.exporters.ghost_html_exporter import GhostHTMLExporter

from nbconvert.writers.files import FilesWriter

import requests
import jwt
from datetime import datetime as date


def get_logger():
  # import a logger and send it to stdout
  logger = log.get_logger()

  handler_names = [ handler.get_name() for handler in logger.handlers ]
  if __name__ not in handler_names:
    handler = logging.StreamHandler(sys.stdout)
    handler.set_name(__name__)
    logger.addHandler(handler)

  return logger

@dataclass
class ProgramArgs:
  notebook: str
  _prefix: str
  _ghost_data_path: str
  ghost_admin_api_key: str
  post_title: Optional[str] = None
  post_date: Optional[str] = None
 
  @property
  def notebook_file(self):
    return f"{self.notebook}.ipynb"
  
  @property
  def prefix(self):
    if self._prefix == 'local':
      prefix = ""
    elif self._prefix == 'dev':
      prefix = "http://localhost:2368"
    else:
      prefix = "https://dlennon.org/ghost"
    return prefix

  @property
  def ghost_data_path(self):
    return Path(self._ghost_data_path)
  
  @property
  def build_path(self):
    return Path(self.ghost_data_path) / "staging/notebooks"
  
  @property
  def output_path(self):
    return Path("content/images/notebooks") / self.notebook

def get_program_args(supplied_args = None):
  parser = argparse.ArgumentParser(
    prog = "publish"
  )
  parser.add_argument("notebook")
  parser.add_argument("--prefix", choices = ['local', 'dev', 'prod'], default = 'local', dest = "_prefix")
  parser.add_argument("--ghost-data-path", default = os.environ["GHOST_DATA_PATH"], dest = "_ghost_data_path")
  parser.add_argument("--ghost-admin-api-key", default = os.environ["GHOST_ADMIN_API_KEY"])
  parser.add_argument("--post-title")
  parser.add_argument("--post-date")

  args = parser.parse_args(supplied_args)
  return ProgramArgs(**vars(args))

def get_config(args : ProgramArgs):
  c = Config()
  c.OutputMd5Preprocessor.prefix = args.prefix
  c.FilesWriter.build_directory = str(args.build_path)

  return c

def convert(config: Config, args : ProgramArgs):
  # read the notebook
  with open(args.build_path / args.notebook_file, "r") as f:
    nbdata = f.read()
  nbjson = json.loads(nbdata)
  nb_content = nbformat.reads(nbdata, as_version = nbjson['nbformat'])

  # run the exporter
  exporter = GhostHTMLExporter(config = config)
  resources = {
     "output_files_dir" : str(args.output_path)
  }
  (body, resources) = exporter.from_notebook_node(nb_content, resources)

  # write the file
  writer = FilesWriter(config = config)
  writer.write(body, resources, notebook_name = args.notebook)

  return (body, resources)

def get_token(args : ProgramArgs):
  # Split the key into ID and SECRET
  id, secret = args.ghost_admin_api_key.split(':')

  # Prepare header and payload
  iat = int(date.now().timestamp())

  header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
  payload = {
      'iat': iat,
      'exp': iat + 5 * 60,
      'aud': '/admin/'
  }

  # Create the token (including decoding secret)
  token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

  return token


if __name__ == '__main__':
  from ghost_stack.publish import *
  import shlex

  # logger = get_logger()
  # logger.setLevel(10)  

  # test_args = shlex.split("hessenberg --post-title 'Hello World' --post-date 2020-01-01 ")
  args = get_program_args(["hessenberg"])
  config = get_config(args)
  body, resources = convert(config, args)

  # postprocess yaml header metadata
  header = resources['yaml_header']

  post_title = args.post_title or header['title']
  post_title = post_title.strip("'\"")

  post_date = args.post_date or header['date']
  post_date = date.fromisoformat(post_date).strftime("%Y-%m-%dT%H:%M:%S.000Z")

  # read the html file
  html_file = args.build_path / f"{args.notebook}.html"
  with open(html_file, "r") as f:
    html_data = f.read()

  # create the post
  post = {
    'title' : post_title,
    'html' : f"<!--kg-card-begin: html-->\n{html_data}\n<!--kg-card-end: html-->",
    'created_at' : post_date,
    'updated_at' : post_date,
    'published_at' : post_date,
    'status': "published"
  }

  # set up the call to the ghost admin api
  token = get_token(args) 
  url = 'http://localhost:2368/ghost/api/admin/posts/?source=html'
  headers = {'Authorization': 'Ghost {}'.format(token)}
  body = { 'posts': [ post ] }
  r = requests.post(url, json=body, headers=headers)
  r.raise_for_status()
  
  # j = r.json()
  # post_id = j['posts'][0]['id']

  # # delete post!
  # token = get_token(args) 
  # url = f"http://localhost:2368/ghost/api/admin/posts/{post_id}/"
  # headers = {'Authorization': 'Ghost {}'.format(token)}
  # body = {}
  # r = requests.delete(url, json=body, headers=headers)
