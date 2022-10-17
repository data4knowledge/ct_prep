import requests
import os
from drive.drive import Drive

API_KEY = os.getenv('CDISC_API_KEY')
BASE_URL = "https://api.library.cdisc.org/api/"

class CtApi():

  def __init__(self, package, date):
    self.__package = package
    self.__date = date
    self.__drive = Drive("api")
  
  def read_code_lists(self):
    if self.cached_cls(self.__package, self.__date):
      return self.read_cls(self.__package, self.__date)
    else:
      result = self.api_get("mdr/ct/packages/%sct-%s/codelists" % (self.__package, self.__date))
      self.write_cls(self.__package, self.__date, result)
      return result

  def read_code_list(self, identifier):
    if self.cached_cl(self.__package, self.__date, identifier):
      return self.read_cl(self.__package, self.__date, identifier)
    else:
      result = self.api_get("mdr/ct/packages/%sct-%s/codelists/%s" % (self.__package, self.__date, identifier))
      self.write_cl(self.__package, self.__date, identifier, result)
      return result

  def api_get(self, url):
    #print("CTAPI.API_GET [1]: %s" % (url))
    api_url = "https://api.library.cdisc.org/api/%s" % (url)
    #print("CTAPI.API_GET [2]: %s" % (api_url))
    headers =  {"Content-Type":"application/json", "api-key": API_KEY}
    response = requests.get(api_url, headers=headers)
    #print("CTAPI.API_GET [3]: %s %s" % (response.status_code, response.json()))
    return response.json()

  def cached_cls(self, package, date):
    return self.__drive.file_present("%s/%s/code_lists.json" % (package, date))
  
  def read_cls(self, package, date):
    return self.__drive.read_from_cache("%s/%s/code_lists.json" % (package, date))

  def write_cls(self, package, date, data):
    self.__drive.dir_present("%s" % (package))
    self.__drive.dir_present("%s/%s" % (package, date))
    self.__drive.write_to_cache("%s/%s/code_lists.json" % (package, date), data)

  def cached_cl(self, package, date, identifier):
    return self.__drive.file_present("%s/%s/%s.json" % (package, date, identifier))
  
  def read_cl(self, package, date, identifier):
    return self.__drive.read_from_cache("%s/%s/%s.json" % (package, date, identifier))
  
  def write_cl(self, package, date, identifier, data):
    self.__drive.dir_present("%s" % (package))
    self.__drive.dir_present("%s/%s" % (package, date))
    self.__drive.write_to_cache("%s/%s/%s.json" % (package, date, identifier), data)

