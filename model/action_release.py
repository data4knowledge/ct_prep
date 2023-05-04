from tkinter.font import names
from model.action import Action
from model.action_scheme import ActionScheme
from model.configuration import Configuration
from model.manifest import Manifest
from neo4j_model.neo4j_database import Neo4jDatabase
from neo4j_model.semantic_version import SemanticVersion
from neo4j_model.scoped_identifier import ScopedIdentifier
from neo4j_model.registration_status import RegistrationStatus
from neo4j_model.release import Release
from neo4j_model.namespace import Namespace
from neo4j_model.registration_authority import RegistrationAuthority
from uuid import uuid4
from model.latest_db import LatestDB
from model.uri_db import URIDB
from model.nodes_and_relationships import NodesAndRelationships

class ActionRelease(Action):
  release_date: str
  namespace_uri: str
  registration_authority_uri: str

  def __init__(self, *args, **kwargs):
    self.release_date = kwargs.pop('release_date')
    self.namespace_uri = kwargs.pop('namespace_uri')
    self.registration_authority_uri = kwargs.pop('registration_authority_uri')
    
  def process(self, manifest):
    uri_db = URIDB()
    latest_db = LatestDB()
    n_r = NodesAndRelationships()
    previous = latest_db.latest("CT")
    ns = uri_db.find(self.namespace_uri)
    ra = uri_db.find(self.registration_authority_uri)
    if previous == None:
      version = "1"
    else:
      version = "%s" % (previous.version() + 1)
    sv = SemanticVersion(major=version, minor="0", patch="0")
    si = ScopedIdentifier(version=int(version), version_label=self.release_date, identifier="CT", 
      semantic_version=sv.__str__(), uuid=str(uuid4()))
    rs = RegistrationStatus(registration_status="Released", effective_date=self.release_date, 
      until_date="", uuid=str(uuid4()))
    uri = "%sdataset/rel/%s" % (ns.value, self.release_date)
    rel = Release(label = "Controlled Terminology", uuid = str(uuid4()), uri = uri)
    rel.identified_by.add(si)
    latest_db.add(si.identifier, rel)
    uri_db.add(rel.uri, rel)
    n_r.add_nodes(rel, rs, si)
    n_r.add_relationship(":SCOPED_BY", si.uuid, ns.uuid)
    n_r.add_relationship(":MANAGED_BY", rs.uuid, ra.uuid)
    n_r.add_relationship(":HAS_STATUS", rel.uuid, rs.uuid)
    n_r.add_relationship(":IDENTIFIED_BY", rel.uuid, si.uuid)
    if not previous == None:
      n_r.add_relationship(":PREVIOUS", rel.uuid, previous.uuid)
    list = manifest.concept_scheme_list(self.release_date)
    for i in list:
      i['parent_uri'] = uri
      i['namespace_uri'] = self.namespace_uri
      i['registration_authority_uri'] = self.registration_authority_uri
    return [ActionScheme(**i).preserve() for i in list]