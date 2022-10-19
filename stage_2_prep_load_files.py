import sys
from model.configuration import *
from model.action_list import *
from neo4j_model.neo4j_database import Neo4jDatabase
from drive.drive import Drive

start_dt = datetime.now()
manifest = Manifest()
release_timings = {}

def config(start_date):
  saved_config = Configuration(manifest)
  saved_config.set_start_date(datetime.strptime(start_date, '%Y-%m-%d').date())
  actions = ActionList(manifest)
  actions.add_releases()

def list_actions():
  action = ActionList(manifest).first()
  return { 'status': 'ok', 'next': action['data'] }

def process_action():
  count = 0
  action = {'data': {}}
  actions = ActionList(manifest)
  #print(actions.list())
  if actions.more():
    count = actions.next()
    action = actions.peek()
    #print(action)
    if action == None:
      action = {'data': {}}
      count = 0
    elif action['klass'] == "ActionScheme":
      release_date = action['data']['release_date']
      scheme = action['data']['scheme']
      if not release_date in release_timings:
        release_timings[release_date] = {}
      release_timings[release_date][scheme] = (datetime.now() - start_dt).total_seconds()
  return { 'status': 'ok', 'action_count': count, 'next': action['data'] }

def action_until(until):
  execute = True
  until_dt = datetime.strptime(until, '%Y-%m-%d')
  previous_dt = datetime.now()
  while execute:
    print("")
    print("")
    data = process_action()
    print("Status: ", json.dumps(data, sort_keys=True, indent=4))
    if data['action_count'] == 0:
      print("Release timings", json.dumps(release_timings, sort_keys=True, indent=4))
      print('No more work ...')
      execute = False
    elif "release_date" in data['next']:
      current_dt = datetime.strptime(data['next']['release_date'], '%Y-%m-%d')
    elif "date" in data['next']:
      current_dt = datetime.strptime(data['next']['date'], '%Y-%m-%d')
    else:
      current_dt = datetime.strptime("2000-01-01", '%Y-%m-%d')
    if execute:
      now_dt = datetime.now()
      total_duration = now_dt - start_dt
      last_duration = now_dt - previous_dt
      total_duration_in_secs = total_duration.total_seconds()  
      last_duration_in_secs = last_duration.total_seconds()  
      print(f'Running for {total_duration_in_secs:.0f} secs [{total_duration_in_secs/3600.0:.2f} hrs]. Last step {last_duration_in_secs:.0f} secs')
      if current_dt >= until_dt:
        print("Release timings", json.dumps(release_timings, sort_keys=True, indent=4))
        print('End date encountered ...')
        execute = False
      else:
        previous_dt = now_dt
  n_r = NodesAndRelationships()
  n_r.dump()

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
  run_config = False
  start_date = "2000-01-01"
  until_date = "2023-01-01"
  kwargs = dict(arg.split('=') for arg in sys.argv[1:])
  if "config" in kwargs:
    run_config = str2bool(kwargs['config'])
  if "until" in kwargs:
    until_date = (kwargs['until'])
  if "start" in kwargs:
    start_date = (kwargs['start'])
  print("MAIN [1]: Start=%s, Until=%s, Run Configuration=%s" % (start_date, until_date, run_config))
  if run_config:
    print("MAIN [2]: Configuring")
    config(start_date)
  print("MAIN [3]: Running")
  action_until(until_date)