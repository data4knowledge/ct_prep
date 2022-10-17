import json
import yaml
import os

CT = "json_data/"
MANIFEST = "source_data/"
API = "api_data/"

class Drive():
    
  def __init__(self, scheme):
    self.__scheme = scheme
    if scheme == "manifest":
      self.__dir = MANIFEST
    elif scheme == "api":
      self.__dir = API
    else:
      self.__dir = CT

  def read(self, filename):
    return self.read_from_cache(filename)

  def read_from_cache(self, filename):
    full_path = self.cache_full_path(filename)
    with open(full_path) as in_file:
      if self.extension(filename) == ".yaml":
        data = yaml.safe_load(in_file)
      else:
        data = json.load(in_file)
    return data

  def write_to_cache(self, filename, data):
    full_path = self.cache_full_path(filename)
    with open(full_path, 'w') as out_file:
      if self.extension(filename) == ".yaml":
        yaml.dump(data, out_file, default_flow_style=False)
      else:
        json.dump(data, out_file)
    return data

  def dir_present(self, dir_name):
    dir_path = self.cache_dir_path(dir_name)
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)
    return True

  def file_present(self, filename):
    full_path = self.cache_full_path(filename)
    return os.path.exists(full_path)

  def cache_full_path(self, filename):
    return os.path.join(self.__dir, self.__scheme, filename)
    
  def cache_dir_path(self, dir_name):
    return os.path.join(self.__dir, self.__scheme, dir_name)

  def extension(self, filename):
    parts = os.path.splitext(filename)
    return parts[1]