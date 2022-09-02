from model.action import Action
from model.action_code_list import ActionCodeList
from model.ct_api import CtApi
from model.ct_file import CtFile
from neo4j_model.neo4j_database import Neo4jDatabase
from neo4j_model.semantic_version import SemanticVersion
from neo4j_model.scoped_identifier import ScopedIdentifier
from neo4j_model.registration_status import RegistrationStatus
from neo4j_model.skos_concept_scheme import SkosConceptScheme
from neo4j_model.namespace import Namespace
from neo4j_model.registration_authority import RegistrationAuthority
from neo4j_model.release import Release
from uuid import uuid4
from service_environment import ServiceEnvironment
from model.latest_db import LatestDB
from model.uri_db import URIDB
from model.nodes_and_relationships import NodesAndRelationships

class ActionScheme(Action):
  scheme: str
  date: str
  format: str
  parent_uri: str
  namespace_uri: str
  registration_authority_uri: str

  def __init__(self, *args, **kwargs):
    #print("ACTION_SCHEME.__INIT__: %s" % (kwargs))
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.release_date = kwargs.pop('release_date')
    self.format = kwargs.pop('format')
    self.parent_uri = kwargs.pop('parent_uri')
    self.namespace_uri = kwargs.pop('namespace_uri')
    self.registration_authority_uri = kwargs.pop('registration_authority_uri')
    #self.__db = Neo4jDatabase()
    #self.__repo = self.__db.repository()

  def process(self, manifest):
    uri_db = URIDB()
    latest_db = LatestDB()
    n_r = NodesAndRelationships()
    identifier = "%s CT" % (self.scheme.upper())

    sr = uri_db.find(self.parent_uri)
    #print(sr)
    ns = uri_db.find(self.namespace_uri)
    ra = uri_db.find(self.registration_authority_uri)
    previous = latest_db.latest(identifier)
    #sr = Release.match(db.graph()).where(uri=self.parent_uri).first()
    #ns = Namespace.match(db.graph()).where(uri=self.namespace_uri).first()
    #ra = RegistrationAuthority.match(db.graph()).where(uri=self.registration_authority_uri).first()
    #previous = SkosConceptScheme.latest(identifier)

    if previous == None:
      version = "1"
    else:
      version = "%s" % (previous.version() + 1)
    print("ACTIONSCHEME.PROCESS [1]: next version = %s" % (version))
    if self.release_date != self.date and previous != None:
      n_r.add_relationship(":PREVIOUS", sr.uuid, previous.uuid)
      #sr.consists_of.add(previous)
      #self.__repo.save(sr)
      return []
    else:
      print("ACTIONSCHEME.PROCESS [2]")
      sv = SemanticVersion(major = version, minor="0", patch="0")
      si = ScopedIdentifier(version=int(version), version_label=self.date, identifier=identifier, 
        semantic_version = sv.__str__(), uuid=str(uuid4()))
      #si.scoped_by.add(ns)
      rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "", uuid=str(uuid4()))
      #rs.managed_by.add(ra)
      uuid = str(uuid4())
      uri = "%sdataset/cdisc/ct/cs/%s/%s" % (ServiceEnvironment().get("BASE_URI"), self.date, self.scheme)
      cs = SkosConceptScheme(label = self.scheme, uuid = uuid, uri = uri)
      #if not previous == None:
      #  cs.previous.add(previous)
      cs.identified_by.add(si)
      uri_db.add(cs.uri, cs)
      latest_db.add(identifier, cs)
      
      #cs.has_status.add(rs)
      #sr.consists_of.add(cs)

      #db.repository().save(cs, si, rs, sr)
      n_r.add_nodes(cs, rs, si)
      n_r.add_relationship(":SCOPED_BY", si.uuid, ns.uuid)
      n_r.add_relationship(":MANAGED_BY", rs.uuid, ra.uuid)
      n_r.add_relationship(":HAS_STATUS", cs.uuid, rs.uuid)
      n_r.add_relationship(":IDENTIFIED_BY", cs.uuid, si.uuid)
      n_r.add_relationship(":CONSISTS_OF", sr.uuid, cs.uuid)
      if not previous == None:
        n_r.add_relationship(":PREVIOUS", cs.uuid, previous.uuid)

      list = self.code_list_list()
      #print("ACTIONSCHEME.PROCESS [3]: %s" % (list))
      for i in list:
        i['parent_uri'] = uri
        i['namespace_uri'] = self.namespace_uri
        i['registration_authority_uri'] = self.registration_authority_uri
      return [ActionCodeList(**i).preserve() for i in list]

  def code_list_list(self):
    if self.format == "api":
      results = []
      api = CtApi(self.scheme, self.date)
      for item in api.read_code_lists()['_links']['codelists']:
        identifier = item['href'].split("/")[-1]
        results.append({ 'identifier': identifier, 'scheme': self.scheme, 'date': self.date, 'format': "api" })  
      return results
    else:
      file = CtFile(self.scheme, self.date)
      file.read()
      return file.code_list_list()


