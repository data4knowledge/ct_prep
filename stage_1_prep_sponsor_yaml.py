import yaml
import json

SOURCE_DIR = "source_data"
OUTPUT_DIR = "json_data"

def add_header(output, item, date):
  output["codelists"] = []
  output["_links"] = { 
    "priorVersion": {
      "href": "",
      "title": "",
      "type": "Terminology"
    }, 
    "self": {
      "href": "",
      "title": "",
      "type": "Terminology"
    } 
  }

def get_synonym(synonyms):
  if synonyms == "":
    return []
  else:
    return [x.strip() for x in synonyms.split(';')]

def add_code_list(output, item):
  print(item)
  synonyms = get_synonym(item['alt_label'])
  code_list = {
    "conceptId": item['identifier'],
    "definition": item['definition'],
    "extensible": item['extensible'],
    'pref_label': item['pref_label'],
    "preferredTerm": item['pref_label'],
    "submissionValue": item['notation'],
    "synonyms": synonyms,
    "terms": []
  } 
  output["codelists"].append(code_list)
  return code_list
 
def add_code_list_item(output, item):
  synonyms = get_synonym(item['alt_label'])
  code_list_item = {
    "conceptId": item['identifier'],
    "definition": item['definition'],
    'name': item['pref_label'],
    "preferredTerm": item['pref_label'],
    "submissionValue": item['notation'],
    "synonyms": synonyms
  } 
  print(output)
  output["terms"].append(code_list_item)
  return code_list_item

def process_file(item, date):
  with open("%s/d4k/%s %s.yaml" % (SOURCE_DIR, item, date)) as file:
    ct = yaml.load(file, Loader=yaml.FullLoader)
    output = {}
    add_header(output, item, date)
    for cl in ct["root"]["code_lists"]:
      code_list = add_code_list(output, cl)
      for cli in cl["terms"]:
        add_code_list_item(code_list, cli)
  return output
  
def process_item(item, date):
  output = process_file(item, date)
  with open("%s/d4k/%s %s.json" % (OUTPUT_DIR, date, item), 'w') as outfile:
    json.dump(output, outfile, indent=2, sort_keys=True)

def process_release(date, info):
  for item, value in info["items"].items():
    process_item(item, value)

filename = "%s/%s" % (SOURCE_DIR, "manifest/manifest.yaml")
with open(filename) as file:
  manifest = yaml.load(file, Loader=yaml.FullLoader)
  #print(manifest)
  for date, info in manifest.items():
    if info['owner'] != "CDISC":
      process_release(date, info)
