from deta import Deta
import json
import os

class Drive():
    
  def __init__(self, dir):
    self.__deta = Deta(os.environ['CDISC_CT_PREP_PROJ_KEY'])
    self.__store = self.__deta.Base("cdisc_ct")
    