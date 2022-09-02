import csv
from stringcase import pascalcase, snakecase 
import os
import glob

node_store = {}
relationship_store = {}
id_number = 1
uuid_to_id = {}

DATA_DIR = "load_data"

class NodesAndRelationships():
  
  def add_nodes(self, *args):
    global node_store
    for item in args:
      label = item.__class__.__name__
      if not label in node_store:
        node_store[label] = []
      node_store[label].append(dict(item.__node__))

  def add_relationship(self, label, from_uri, to_uri):
    global relationship_store
    if not label in relationship_store:
      relationship_store[label] = []
    relationship_store[label].append({ "from": from_uri, "to": to_uri})

  def dump(self):
    global id_number
    global uuid_to_id
    id_number = 1
    self.clean()
    for k, v in node_store.items():
      print("NODE '%s': %s" % (k, len(v)))
      self.dump_nodes(k, v)
    for k, v in relationship_store.items():
      print("REL '%s': %s" % (k, len(v)))
      self.dump_relationships(k, v)

  def clean(self):
    files = glob.glob("%s/*.csv" % (DATA_DIR))
    for f in files:
      os.remove(f)
  
  def dump_nodes(self, type, data, block_size=100000):
    global id_number
    global uuid_to_id
    block_count = 0
    file_count = 1
    print(data[0])
    fields = list(data[0].keys())
    fieldnames = ["id:ID"] + fields
    for row in data:
      if block_count == 0:
        csv_filename = "%s/node-%s-%s.csv" % (DATA_DIR, snakecase(type), file_count)
        csv_file = open(csv_filename, mode='w', newline='')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        file_count += 1
      row["id:ID"] = id_number
      uuid_to_id[row["uuid"]] = id_number
      id_number += 1
      writer.writerow(row)
      block_count += 1
      if block_count >= block_size:
        block_count = 0

  def dump_relationships(self, type, items, block_size=100000):
    block_count = 0
    file_count = 1
    fieldnames = [ ":START_ID", ":END_ID" ]
    for row in items:
      if block_count == 0:
        csv_filename = "%s/rel-%s-%s.csv" % (DATA_DIR, type[1:].lower(), file_count)
        csv_file = open(csv_filename, mode='w', newline='')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        file_count += 1
      new_row = { ":START_ID": uuid_to_id[row["from"]], ":END_ID": uuid_to_id[row["to"]] }
      writer.writerow(new_row)
      block_count += 1
      if block_count >= block_size:
        block_count = 0



