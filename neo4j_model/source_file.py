from py2neo.ogm import Model, Property

class SourceFile(Model):
  filename = Property()
