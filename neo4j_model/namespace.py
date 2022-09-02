from py2neo.ogm import Model, Property

class Namespace(Model):
  uri = Property()
  uuid = Property()
