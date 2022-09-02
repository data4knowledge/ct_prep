import json

class Action():
  
  def preserve(self):
    klass_name = self.__class__.__name__
    data = {}
    for k, v in vars(self).items():
      if not k.startswith("_%s" % (klass_name)):
        data[k] = v
        #print("PRESERVE [1]: %s = %s" % (k,v))
    result = { 'klass': klass_name, 'data': data}
    #print("PRESERVE [2]:", result)
    return result
