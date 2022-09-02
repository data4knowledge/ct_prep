import json
import yaml
import os
import pathlib
from service_environment import ServiceEnvironment

CT = "json_data/"
MANIFEST = "source_data/"

class Drive():
    
  def __init__(self, scheme):
    self.__scheme = scheme
    if scheme == "manifest":
      self.__dir = MANIFEST
    else:
      self.__dir = CT

  def read(self, filename):
    return self.read_from_cache(filename)

  def present(self, filename):
    list_result = self.__drive.list()
    files = list_result.get("names")
    if filename in files:
      return True
    return False

  def read_from_cache(self, filename):
    full_path = self.cache_full_path(filename)
    with open(full_path) as infile:
      if pathlib.Path(filename).suffix == ".yaml":
        data = yaml.safe_load(infile)
      else:
        data = json.load(infile)
    return data

  def cache_full_path(self, filename):
    return os.path.join(self.__dir, self.__scheme, filename)
    
