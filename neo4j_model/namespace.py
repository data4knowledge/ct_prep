from py2neo.ogm import Model, Property

class Namespace(Model):
  reference_uri = Property()
  uuid = Property()
  value = Property()
  name = Property()