# Simple program to download the latest version of all the CDISC CT and
# convert into a semantic (SKOS) form.
from platform import release
import yaml
import json
import os
import requests
from beautifultable import BeautifulTable

# Get API key. Uses an environment variable.
API_KEY = os.getenv('CDISC_API_KEY')

# Information as to when items within a packahe were introduced or withdrawn.
with open("source_data/manifest/introduced_withdrawn.yaml") as file:
  data = yaml.load(file, Loader=yaml.FullLoader)
  introduced = data['introduced']
  withdrawn = data['withdrawn']

# Information as to when items within a packahe were introduced or withdrawn.
with open("source_data/manifest/manifest.yaml") as file:
  existing_manifest = yaml.load(file, Loader=yaml.FullLoader)

# 1.1 Get all the package information via the API
api_url = "https://api.library.cdisc.org/api/mdr/ct/packages"
headers =  {"Content-Type":"application/json", "api-key": API_KEY}
response = requests.get(api_url, headers=headers)
items = {}
types = {}
manifest = {}
for item in response.json()['_links']['packages']:
  reduced_title = item['title'].replace("Controlled Terminology Package ", "")
  reduced_title = reduced_title.replace("Effective ", "")
  title_items = reduced_title.split(' ')
  type = title_items[0].upper()
  types[type] = type
  package_number = title_items[1]
  release_date = title_items[2]
  if not package_number in items:
    items[package_number] = {}
  items[package_number][type] = {'release_date': release_date, 'package_number': package_number, 'type': type, 'href': item['href']}

# 1.2 Transform into a table of package to items
latest = {}
results = []
final_results = {}
keys = items.keys()
for key in keys:
  results.append(int(key))
results.sort()
table = BeautifulTable()
table.columns.header = ["Pk"] + list(types.keys())
for key in results:
  for package, item in items.items():
    if int(package) == key:
      table_row = [key]
      if not package in final_results:
        final_results[package] = []
      final_results[package].append(item)
      for k,v in types.items():
        if k in item:
          table_row.append(item[k]['release_date'])
          rel_date = item[k]['release_date']
          package = item[k]['package_number']
          if not rel_date in manifest:
            manifest[rel_date] = {'package': int(package), 'format': 'api', 'items': {}}
          manifest[rel_date]['items'][k.lower()] = rel_date
          latest[k.lower()] = rel_date
        else:
          if key < introduced[k]:
            table_row.append("NA")
          elif withdrawn[k] == None:
            table_row.append('^')
          elif key >= withdrawn[k]:
            table_row.append("W")
          else:
            table_row.append('^')
      table.rows.append(table_row)

print('')
print('NEW MANIFEST ENTRIES')
print('====================')
print('')
for k,v in manifest.items():
  if not k in existing_manifest: 
    print(k)
    print(json.dumps(v, sort_keys=True, indent=4))

# 1.3 Print the table, just useful information
table.maxwidth = 150
print('')
print('RELEASE TABLE')
print('=============')
print('')
print('Key: ')
print('')
print('Date indicates the version to be used for that package.')
print('^ = Use the previous version.') 
print('NA = Not applicable, file was not introduced at that date.')
print('W = file withdrawn, not to be used anymore.')
print('')
print(table)
print('')
print('')

