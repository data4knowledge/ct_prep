from typing import List
from datetime import date, datetime
from model.manifest import Manifest
import json

START_DATE = 'start_date'
INITIAL_RELEASE_DATE = "2007-01-01"
config_store = {}

class ConfigurationIn():
  start_date: date
  
class Configuration():
  start_date: date

  def __init__(self, manifest):
    self.__manifest = manifest
    self._read_start_date()

  def set_start_date(self, requested_date):
    global config_store
    self.start_date = self.__manifest.next_release_after(requested_date)
    config_store[START_DATE] = self.start_date

  def _read_start_date(self):
    global config_store
    if START_DATE in config_store:
      self.start_date = config_store[START_DATE]
    else:
      self.start_date = INITIAL_RELEASE_DATE
