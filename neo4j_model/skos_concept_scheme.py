from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.concept import Concept
from neo4j_model.skos_concept import SkosConcept
from neo4j_model.neo4j_database import Neo4jDatabase

class SkosConceptScheme(Concept):
  top_level_concept = RelatedTo(SkosConcept, "TOP_LEVEL_CONCEPT")

  def latest_code_list(self, identifier):
    db = Neo4jDatabase()
    query = """
      MATCH (cs:SkosConceptScheme)-[:TOP_LEVEL_CONCEPT]->(a:SkosConcept)-[:IDENTIFIED_BY]->(si) 
        WHERE cs.label="%s" AND si.identifier='%s' AND NOT ()-[:PREVIOUS]->(a) RETURN a
    """ % (self.label, identifier)
    #print("CONCEPT.LATEST [1]: %s" % (query))
    results = db.graph().run(query).data()
    if len(results) == 0:
      return None
    return SkosConcept.wrap(results[0]['a'])