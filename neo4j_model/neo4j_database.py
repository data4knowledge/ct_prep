from py2neo.ogm import Repository
from utility.service_environment import ServiceEnvironment

class Neo4jDatabase():
  
  def __init__(self):
    sv = ServiceEnvironment()
    db_name = sv.get('NEO4J_DB_NAME')
    url = sv.get('NEO4J_URI')
    usr = sv.get('NEO4J_USERNAME')
    pwd = sv.get('NEO4J_PASSWORD')
    self.__repo = Repository(url, name=db_name, user=usr, password=pwd)

  def repository(self):
    return self.__repo

  def graph(self):
    return self.__repo.graph

  def clear(self):
    query = """
      CALL apoc.periodic.iterate('MATCH (n) RETURN n', 'DETACH DELETE n', {batchSize:1000})
    """
    self.__repo.graph.run(query)