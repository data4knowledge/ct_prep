from py2neo.ogm import Model, Property

class RegistrationAuthority(Model):
  reference_uri = Property()
  uuid = Property()
  name = Property()
