import json
from model.configuration import Configuration
from model.manifest import Manifest
from model.action_release import ActionRelease
from model.action_scheme import ActionScheme
from model.action_code_list import ActionCodeList
from model.action import Action
from model.ra_server import RaServer
from model.action_db import ActionDB
from neo4j_model.namespace import Namespace
from neo4j_model.registration_authority import RegistrationAuthority
from datetime import datetime
from model.uri_db import URIDB
from uuid import uuid4
from model.nodes_and_relationships import NodesAndRelationships

class ActionList(Action):
  
  def __init__(self, manifest):
    self.__manifest = manifest
    self.__config = Configuration(manifest)
    self.__actions = ActionDB()

  def add_releases(self):
    uri_db = URIDB()
    ns_json = RaServer().namespace_by_name("CDISC CT namespace")
    ns = Namespace(uri=ns_json['uri'], uuid=str(uuid4()))
    #print(ns_json)
    ra_json = RaServer().registration_authority_by_namespace_uuid(ns_json['uuid'])
    #print(ra_json)
    ra = RegistrationAuthority(uri=ra_json['uri'], uuid=str(uuid4()))
    
    #self.__repo.save(ns, ra)
    n_r = NodesAndRelationships()
    n_r.add_nodes(ns, ra)
    uri_db.add(ns.uri, ns)
    uri_db.add(ra.uri, ra)

    dates = self.__manifest.release_list(self.__config.start_date)
    self.__actions.add([ActionRelease(release_date=i, namespace_uri=ns.uri, registration_authority_uri=ra.uri).preserve() for i in dates])

  def next(self):
    #start_dt = datetime.now()
    data = self.__actions.first()
    klass = globals()[data['klass']]
    action = klass(**data['data'])
    #print("DATA", data)
    #print("KLASS", klass)
    #del self.__actions[0]
    new_actions = action.process(self.__manifest)
    #action_dt = datetime.now()
    #print("ACTIONLIST.NEXT [1] count =", len(json.dumps(new_actions)))
    self.__actions.add(new_actions)
    #store_dt = datetime.now()
    #action_duration = action_dt - start_dt
    #store_duration = store_dt - action_dt
    #action_duration_in_secs = action_duration.total_seconds()  
    #store_duration_in_secs = store_duration.total_seconds()  
    #print(f'ACTIONLIST.NEXT [2] action step = {action_duration_in_secs:.0f} secs, store step = {store_duration_in_secs:.0f} secs')
    return self.__actions.count()
    
  def list(self):
    return self.__actions.list()

  def first(self):
    return self.__actions.first()
    
  def more(self):
    return self.__actions.more()

  def peek(self):
    return self.__actions.peek()
