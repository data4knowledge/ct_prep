from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from model.ct_file import CtFile
from model.ct_api import CtApi
from neo4j_model.registration_authority import RegistrationAuthority
from neo4j_model.neo4j_database import Neo4jDatabase
from neo4j_model.semantic_version import SemanticVersion
from neo4j_model.scoped_identifier import ScopedIdentifier
from neo4j_model.registration_status import RegistrationStatus
from neo4j_model.skos_concept import SkosConcept
from neo4j_model.skos_concept_scheme import SkosConceptScheme
from neo4j_model.namespace import Namespace
from uuid import uuid4
from service_environment import ServiceEnvironment
from deepdiff import DeepDiff
from model.latest_db import LatestDB
from model.uri_db import URIDB
from model.nodes_and_relationships import NodesAndRelationships

class ActionCodeList(Action):
  identifier: str
  scheme: str
  date: str
  parent_uri: str
  namespace_uri: str
  registration_authority_uri: str

  def __init__(self, *args, **kwargs):
    self.identifier = kwargs.pop('identifier')
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.parent_uri = kwargs.pop('parent_uri')
    self.namespace_uri = kwargs.pop('namespace_uri')
    self.registration_authority_uri = kwargs.pop('registration_authority_uri')
    self.format = kwargs.pop('format')

  def process(self, manifest):
    previous_items = {}
    previous_dicts = {}

    uri_db = URIDB()
    latest_db = LatestDB()
    n_r = NodesAndRelationships()
    previous = latest_db.latest(self.identifier)
    scs = uri_db.find(self.parent_uri)

    #print("ACTIONCODELIST.PROCESS [1]:", previous)

    #scs = SkosConceptScheme.match(db.graph()).where(uri=self.parent_uri).first()
    #previous = scs.latest_code_list(self.identifier)
    if previous == None:
      version = "1"
      previous_dict = None
    else:
      version = "%s" % (previous.version() + 1)
      previous_dict = previous.dict()
      previous_dict.pop('uuid')
      previous_dict.pop('uri')
      previous_dict['terms'] = []
      #print("ACTIONCODELIST.PROCESS [2a]:", previous_dict)
      for item in previous.narrower:
        item_dict = item.dict()
        item_dict.pop('uuid')
        item_dict.pop('uri')
        previous_dict['terms'].append(item_dict)
        previous_items[item.identifier] = item
        previous_dicts[item.identifier] = item_dict
      #print("ACTIONCODELIST.PROCESS [2b]:", previous_dict['terms'])

    if self.format == "api":
      api = CtApi(self.scheme, self.date)
      codelist = api.read_code_list(self.identifier)
      #print("ACTIONCODELIST.PROCESS [4a]:", codelist['conceptId'])
    else:
      file = CtFile(self.scheme, self.date)
      file.read()
      codelist = file.code_list(self.identifier)
      #print("ACTIONCODELIST.PROCESS [4b]:", codelist['conceptId'])

    codelist['extensible'] = False
    if 'extensible' in codelist:
      codelist['extensible'] = codelist.pop('extensible')
    codelist.pop('conceptId')
    codelist['identifier'] = self.identifier
    codelist['label'] = codelist.pop('name')
    codelist['notation'] = codelist.pop('submissionValue')
    codelist['pref_label'] = codelist.pop('preferredTerm')
    if 'synonyms' in codelist:
      codelist['alt_label'] = ";".join(codelist['synonyms'])  
      codelist.pop('synonyms')
    else:
      codelist['alt_label'] = ""
    for term in codelist['terms']:
      term['identifier'] = term.pop('conceptId')
      term['label'] = term['preferredTerm']
      term['notation'] = term.pop('submissionValue')
      term['pref_label'] = term.pop('preferredTerm')
      if 'synonyms' in term:
        term['alt_label'] = ";".join(term['synonyms'])  
        term.pop('synonyms')
      else:
        term['alt_label'] = []
      term['extensible'] = False
    #print("ACTIONCODELIST.PROCESS [5a]: %s" % (codelist))
    #print("ACTIONCODELIST.PROCESS [5b]: %s" % (DeepDiff(previous_dict, codelist, ignore_order=True)))
    if (previous_dict == None) or (not previous_dict == None and DeepDiff(previous_dict, codelist, ignore_order=True)):
      #print("ACTIONCODELIST.PROCESS [5b]:")
      ns = uri_db.find(self.namespace_uri)
      ra = uri_db.find(self.registration_authority_uri)
      #ns = Namespace.match(db.graph()).where(uri=self.namespace_uri).first()
      #ra = RegistrationAuthority.match(db.graph()).where(uri=self.registration_authority_uri).first()
      sv = SemanticVersion(major=version, minor="0", patch="0")
      si = ScopedIdentifier(version = int(version), version_label = self.date, identifier = "%s" % (self.identifier), 
        semantic_version = sv.__str__(), uuid=str(uuid4()))
      #si.scoped_by.add(ns)
      rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "", uuid=str(uuid4()))
      #rs.managed_by.add(ra)
      n_r.add_relationship(":SCOPED_BY", si.uuid, ns.uuid)
      n_r.add_relationship(":MANAGED_BY", rs.uuid, ra.uuid)


      #n_r.add_nodes(cs, rs, si)
      #n_r.add_relationship(":HAS_STATUS", cs.uuid, rs.uuid)
      #n_r.add_relationship(":IDENTIFIED_BY", cs.uuid, si.uuid)
      #n_r.add_relationship(":CONSISTS_OF", sr.uuid, cs.uuid)



      uuid = str(uuid4())
      uri = "%sdataset/cdisc/ct/sc/%s/%s/%s" % (ns.value, self.date, self.scheme, self.identifier)
      cs = SkosConcept(label = codelist['label'],
        identifier = codelist['identifier'],
        notation = codelist['notation'],
        alt_label = codelist['alt_label'],
        pref_label = codelist['pref_label'],
        definition = codelist['definition'],
        extensible = codelist['extensible'],
        uuid = uuid,
        uri = uri
      )
      latest_db.add(self.identifier, cs)
      if not previous == None:
        n_r.add_relationship(":PREVIOUS", cs.uuid, previous.uuid)
      n_r.add_relationship(":TOP_LEVEL_CONCEPT", scs.uuid, cs.uuid)
      n_r.add_relationship(":HAS_STATUS", cs.uuid, rs.uuid)
      n_r.add_relationship(":IDENTIFIED_BY", cs.uuid, si.uuid)
      n_r.add_nodes(cs, rs, si)
      #if not previous == None:
      #  cs.previous.add(previous)
      #scs.top_level_concept.add(cs)
      #print("ACTIONCODELIST.PROCESS [2]")
      cs.identified_by.add(si)
      #cs.has_status.add(rs)
      for cl in codelist['terms']:
        if cl['identifier'] in previous_items:
          previous_term = previous_items[cl['identifier']]
          the_dict = previous_dicts[cl['identifier']]
        else:
          previous_term = None
          the_dict = None
        if previous_term != None:
          #print("ACTIONCODELIST.PROCESS [6b]: ", the_dict)
          #print("ACTIONCODELIST.PROCESS [6b]: ", cl)
          differences = DeepDiff(the_dict, cl, ignore_order=True)
          diff = differences != {}
          #print("ACTIONCODELIST.PROCESS [6c]: ", diff)
          #print("ACTIONCODELIST.PROCESS [6d]: ", DeepDiff(the_dict, cl, ignore_order=True))
        else:
          #print("ACTIONCODELIST.PROCESS [6e]: ")
          diff = True
        if diff:  
          uuid = str(uuid4())
          uri = "%sdataset/cdisc/ct/sc/%s/%s/%s/%s" % (ns.value, self.date, self.scheme, self.identifier, cl['identifier'])
          child = SkosConcept(label = cl['label'],
            identifier = cl['identifier'],
            notation = cl['notation'],
            alt_label = cl['alt_label'],
            pref_label = cl['pref_label'],
            definition = cl['definition'],
            extensible = False,
            uuid = uuid,
            uri = uri
          )
          n_r.add_nodes(child)
          if previous_term != None:
            #child.previous.add(previous_term)
            n_r.add_relationship(":PREVIOUS", child.uuid, previous_term.uuid)
        else:
          child = previous_term
        #print("ACTIONCODELIST.PROCESS [5]: ", child)
        cs.narrower.add(child)
        n_r.add_relationship(":NARROWER", cs.uuid, child.uuid)
      #db.repository().save(cs, scs)
    else:
      #scs.top_level_concept.add(previous)
      n_r.add_relationship(":TOP_LEVEL_CONCEPT", scs.uuid, previous.uuid)
      #db.repository().save(scs)
    #print("ACTIONCODELIST.PROCESS [5]:")
    return []

  def search(self, items, identifier):
    print("ACTIONCODELIST.SEARCH [1]: %s, %s" % (items, identifier))
    if items == None:
      return None
    for p in items['terms']:
      print("ACTIONCODELIST.SEARCH [2]: %s" % (p))
      if p['identifier'] == identifier:
        return p
    print("ACTIONCODELIST.SEARCH [3]: None")
    return None