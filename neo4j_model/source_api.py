from py2neo.ogm import Model, Property

class SourceApi(Model):
  package = Property()
  date = Property()
