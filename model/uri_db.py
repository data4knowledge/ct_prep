uri_store = {}

class URIDB():
  
  def add(self, uri, item):
    global uri_store
    uri_store[uri] = item

  def find(self, uri):
    global uri_store
    if uri in uri_store:
      return uri_store[uri]
    else:
      return None