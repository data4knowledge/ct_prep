from py2neo.ogm import Model, Property, RelatedTo

class Extension(Model):
  label = Property()
  value = Property()
  data_type = Property()
  