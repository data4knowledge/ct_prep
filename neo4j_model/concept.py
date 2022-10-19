from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.scoped_identifier import ScopedIdentifier
from neo4j_model.registration_status import RegistrationStatus
from neo4j_model.extension import Extension
from neo4j_model.neo4j_database import Neo4jDatabase

class Concept(Model):
  uuid = Property()
  uri = Property()
  name = Property()
  
  identified_by = RelatedTo(ScopedIdentifier, "IDENTIFIED_BY")
  has_status = RelatedTo(RegistrationStatus, "HAS_STATUS")
  previous = RelatedTo('Concept', "PREVIOUS")
  extended_with = RelatedTo(Extension, "EXTENDED_WITH")

  def version(self):
    for item in self.identified_by:
      return int(item.version)
    return None

  def version_label(self):
    for item in self.identified_by:
      return item.version_label
    return None

  def dict(self):
    return dict(self.__ogm__.node)