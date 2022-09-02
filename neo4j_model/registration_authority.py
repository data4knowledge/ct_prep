from py2neo.ogm import Model, Property

class RegistrationAuthority(Model):
  uri = Property()
  uuid = Property()
