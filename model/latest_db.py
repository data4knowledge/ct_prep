lastest_store = {}

class LatestDB():
  
  def add(self, identifier, item):
    global lastest_store
    #print("LDB1:", identifier)
    #print("LDB2:", lastest_store)
    lastest_store[identifier] = item

  def latest(self, identifier):
    global lastest_store
    if identifier in lastest_store:
      return lastest_store[identifier]
    else:
      #print("LDB3:", lastest_store)
      return None