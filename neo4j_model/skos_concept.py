from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.concept import Concept

class SkosConcept(Concept):
  identifier = Property()
  notation = Property()
  alt_label = Property()
  pref_label = Property()
  definition = Property()
  extensible = Property()
  
  narrower = RelatedTo('SkosConcept', "NARROWER")
 