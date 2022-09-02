from datetime import datetime
from drive.drive import Drive

class CtFile():

  def __init__(self, scheme, date):
    self.scheme = scheme
    self.date = date
    self.__drive = Drive(scheme)
  
  def filename(self):
    return "%s %s.json" % (self.date, self.scheme)

  def read(self):
    self.__file = self.__drive.read(self.filename())

  def code_list_list(self):
    results = []
    for item in self.__file['codelists']:
      results.append({ 'identifier': item['conceptId'], 'scheme': self.scheme, 'date': self.date, 'format': "file" })  
    return results 

  def code_list(self, identifier):
    return next(item for item in self.__file['codelists'] if item["conceptId"] == identifier )
