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
    n_r = NodesAndRelationships()

    ns_c_json = RaServer().namespace_by_name("CDISC CT namespace")
    ns_c = Namespace(uri=ns_c_json['uri'], value=ns_c_json['value'], uuid=str(uuid4()))
    ra_c_json = RaServer().registration_authority_by_namespace_uuid(ns_c_json['uuid'])
    ra_c = RegistrationAuthority(uri=ra_c_json['uri'], uuid=str(uuid4()))

    print("A:", ns_c_json)
    print("B:", ra_c_json)
    print("C:", ns_c.uri)
    print("B:", ra_c.uri)

    ns_s_json = RaServer().namespace_by_name("d4k CT namespace")
    ns_s = Namespace(uri=ns_s_json['uri'], value=ns_s_json['value'], uuid=str(uuid4()))
    ra_s_json = RaServer().registration_authority_by_namespace_uuid(ns_s_json['uuid'])
    ra_s = RegistrationAuthority(uri=ra_s_json['uri'], uuid=str(uuid4()))

    print("1:", ns_s_json)
    print("2:", ra_s_json)
    print("3:", ns_s.uri)
    print("4:", ra_s.uri)
    
    n_r.add_nodes(ns_c, ra_c, ns_s, ra_s)
    uri_db.add(ns_c.uri, ns_c)
    uri_db.add(ra_c.uri, ra_c)
    uri_db.add(ns_s.uri, ns_s)
    uri_db.add(ra_s.uri, ra_s)

    print("N-R:", n_r)

    dates = self.__manifest.release_list(self.__config.start_date)
    items = []
    for item in dates:
      if item['owner'] == "CDISC":
        ns_uri = ns_c.uri
        ra_uri = ra_c.uri
      else:
        ns_uri = ns_s.uri
        ra_uri = ra_s.uri
      items.append(ActionRelease(release_date=item['date'], namespace_uri=ns_uri, registration_authority_uri=ra_uri).preserve())
    self.__actions.add(items)

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
