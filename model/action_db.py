action_store = []

class ActionDB():
  
  def add(self, items):
    global action_store
    action_store = items + action_store
    #print("ACTIONDB1:", len(action_store))
    #print("ACTIONDB2:", action_store[0])

  def first(self):
    global action_store
    if len(action_store) > 0:
      action = action_store[0]
      del action_store[0]
      return action
    else:
      return None

  def peek(self):
    global action_store
    if len(action_store) > 0:
      action = action_store[0]
      return action
    else:
      return None

  def list(self):
    global action_store
    return action_store

  def more(self):
    global action_store
    return len(action_store) > 0

  def count(self):
    global action_store
    return len(action_store)
