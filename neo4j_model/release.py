from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.concept import Concept
from neo4j_model.skos_concept_scheme import SkosConceptScheme

class Release(Concept):
  consists_of = RelatedTo(SkosConceptScheme, "CONSISTS_OF")