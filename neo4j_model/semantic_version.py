from py2neo.ogm import Model, Property

class SemanticVersion(Model):
  major = Property()
  minor = Property()
  patch = Property()

  def __str__(self):
    return "%s.%s.%s" % (self.major, self.minor, self.patch)