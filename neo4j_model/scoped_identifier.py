from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.namespace import Namespace

class ScopedIdentifier(Model):
  uuid = Property()
  version = Property()
  version_label = Property()
  identifier = Property()
  semantic_version = Property()
  
  scoped_by = RelatedTo(Namespace, "SCOPED_BY")