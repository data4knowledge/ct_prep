import requests
import os

API_KEY = os.getenv('CDISC_API_KEY')
BASE_URL = "https://api.library.cdisc.org/api/"

class CtApi():

  def __init__(self, package, date):
    self.__package = package
    self.__date = date
  
  def read_code_lists(self):
    return self.api_get("mdr/ct/packages/%sct-%s/codelists" % (self.__package, self.__date))

  def read_code_list(self, identifier):
    return self.api_get("mdr/ct/packages/%sct-%s/codelists/%s" % (self.__package, self.__date, identifier))

  def api_get(self, url):
    #print("CTAPI.API_GET [1]: %s" % (url))
    api_url = "https://api.library.cdisc.org/api/%s" % (url)
    #print("CTAPI.API_GET [2]: %s" % (api_url))
    headers =  {"Content-Type":"application/json", "api-key": API_KEY}
    response = requests.get(api_url, headers=headers)
    #print("CTAPI.API_GET [3]: %s %s" % (response.status_code, response.json()))
    return response.json()
