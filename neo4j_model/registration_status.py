from py2neo.ogm import Model, Property

from py2neo.ogm import Model, Property, RelatedTo
from neo4j_model.registration_authority import RegistrationAuthority

class RegistrationStatus(Model):
  uuid = Property()
  registration_status = Property()
  effective_date = Property()
  until_date = Property()
  
  managed_by = RelatedTo(RegistrationAuthority, "MANAGED_BY")