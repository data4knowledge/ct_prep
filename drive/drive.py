from deta import Deta
import json
import os

class Drive():
    
  def __init__(self):
    self.__deta = Deta(os.environ['CDISC_CT_PREP_PROJ_KEY'])
    
  def upload_dir(self, dir_path, name):
    drive = self.__deta.Drive("cdisc_ct.%s" % (name))
    for filename in os.listdir(dir_path):
      full_path = os.path.join(dir_path, filename)
      if os.path.isfile(full_path):
        drive.put(filename, path=full_path)
        print("Uploaded %s from %s" % (filename, dir_path))
