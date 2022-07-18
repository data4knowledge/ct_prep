import pandas as pd
import yaml
import json

SOURCE_DIR = "source_data"
OUTPUT_DIR = "json_data"
FILE_MAP = { 
  "adam": 
    { 
      "filename": "ADaM Terminology",
      "sheet_name": "ADaM"
    },
  "cdash": 
    { 
      "filename": "CDASH Terminology",
      "sheet_name": "CDASH"
    },
  "coa":  
    { 
      "filename": "COA Terminology",
      "sheet_name": "COA"
    },
  "define-xml":  
    { 
      "filename": "Define-XML Terminology",
      "sheet_name": "Def-XML"
    },
  "protocol":  
    { 
      "filename": "Protocol Terminology",
      "sheet_name": "Protocol"
    },
  "qrs":  
    { 
      "filename": "QRS Terminology",
      "sheet_name": "QRS"
    },
  "qs":  
    { 
      "filename": "QS Terminology",
      "sheet_name": "QS"
    },
  "qs-ft":  
    { 
      "filename": "QS-FT Terminology",
      "sheet_name": "QS-FT"
    },
  "sdtm":  
    { 
      "filename": "SDTM Terminology",
      "sheet_name": "SDTM"
    },
  "send":  
    { 
      "filename": "SEND Terminology",
      "sheet_name": "SEND"
    }
}
COLUMN_MAP = {
  "1": { "check": "equal", "check_col": -1, "CL": 1, "CLI": 0, "EXT": 2, "SUB": 4, "PT": 5, "DEF": 6, "SYN": 7, "NAME": 3 },
  "2": { "check": "equal", "check_col": -1, "CL": 1, "CLI": 0, "EXT": 2, "SUB": 4, "PT": 8, "DEF": 7, "SYN": 6, "NAME": 3 },
  "3": { "check": "empty", "check_col": 1, "CL": 0, "CLI": 0, "EXT": 2, "SUB": 4, "PT": 5, "DEF": 7, "SYN": 6, "NAME": 3 },
  "4": { "check": "empty", "check_col": 1, "CL": 0, "CLI": 0, "EXT": 2, "SUB": 4, "PT": 5, "DEF": 6, "SYN": 7, "NAME": 3 },
  "5": { "check": "empty", "check_col": 1, "CL": 0, "CLI": 0, "EXT": 2, "SUB": 4, "PT": 7, "DEF": 6, "SYN": 5, "NAME": 3 }
}

manifest = {}

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

def get_cell(row, index):
  if pd.isnull(row[index]):
    return ""
  else:
    return row[index]

def get_synonym(row, index):
  cell = get_cell(row, index)
  if cell == "":
    return []
  else:
    return [x.strip() for x in cell.split(';')]

def add_code_list(format, output, row):
  #print("ADD_CODE_LIST %s %s" % (format, row))
  synonyms = get_synonym(row, COLUMN_MAP[format]["SYN"])
  code_list = {
    "conceptId": get_cell(row, COLUMN_MAP[format]["CL"]),
    "definition": get_cell(row, COLUMN_MAP[format]["DEF"]),
    "extensible": get_cell(row, COLUMN_MAP[format]["EXT"]),
    "name": get_cell(row, COLUMN_MAP[format]["NAME"]),
    "preferredTerm": get_cell(row, COLUMN_MAP[format]["PT"]),
    "submissionValue": get_cell(row, COLUMN_MAP[format]["SUB"]),
    "synonyms": synonyms,
    "terms": []
  } 
  output["codelists"].append(code_list)
  return code_list
 
def add_code_list_item(format, output, row):
  #print("ADD_CODE_LIST_ITEM %s %s" % (format, row))
  synonyms = get_synonym(row, COLUMN_MAP[format]["SYN"])
  code_list_item = {
    "conceptId": get_cell(row, COLUMN_MAP[format]["CLI"]),
    "definition": get_cell(row, COLUMN_MAP[format]["DEF"]),
    "preferredTerm": get_cell(row, COLUMN_MAP[format]["PT"]),
    "submissionValue": get_cell(row, COLUMN_MAP[format]["SUB"]),
    "synonyms": synonyms
  } 
  output["terms"].append(code_list_item)
  return code_list_item

def process_sheet_format(df, format, output, item, date):
  #print(df)
  code_list = None
  for index, row in df.iterrows():
    ext = get_cell(row, COLUMN_MAP[format]["EXT"])
    if COLUMN_MAP[format]["check"] == "equal" and row[COLUMN_MAP[format]["CL"]] == row[COLUMN_MAP[format]["CLI"]] and ext != "":
      code_list = add_code_list(format, output, row)
    elif COLUMN_MAP[format]["check"] == "empty" and get_cell(row, COLUMN_MAP[format]["check_col"]) == "":
      code_list = add_code_list(format, output, row)
    else:
      add_code_list_item(format, code_list, row)
  return None

def set_format(item, date):
  #print("SET_FORMAT %s %s" % (item, date))
  info = manifest[date]["format"]
  if "api" in info:
    return "api"
  else:
    return info[0]

def sheet_name(format, item, date):
  if format == "1":
    return "CDISC %s Terminology" % (FILE_MAP[item]["sheet_name"])
  elif format == "2":
    return "CDISC %s Terminology" % (FILE_MAP[item]["sheet_name"])
  elif format == "3":
    return "%s Terminology %s" % (FILE_MAP[item]["sheet_name"], date)
  elif format == "4":
    return "%s Terminology" % (FILE_MAP[item]["sheet_name"])
  else:
    return "%s Terminology %s" % (FILE_MAP[item]["sheet_name"], date)

def read_sheet(format, item, date):
  if format == "api":
    return pd.DataFrame([])
  print("READ_SHEET %s %s %s" % (format, item, date))
  filename = "%s/%s/%s %s.xls" % (SOURCE_DIR, item, FILE_MAP[item]["filename"], date)
  df = pd.read_excel (filename, sheet_name(format, item, date))
  return df

def process_sheet(df, format, item, date):
  output = {}
  add_header(output, item, date)
  process_sheet_format(df, format, output, item, date)
  return output

def process_item(item, date):
  format = set_format(item, date)
  df = read_sheet(format, item, date)
  if not df.empty:
    output = process_sheet(df, format, item, date)
    with open("%s/%s/%s %s.json" % (OUTPUT_DIR, item, date, item), 'w') as outfile:
      json.dump(output, outfile, indent=2, sort_keys=True)

def process_release(date, info):
  package = info["package"]
  for item, value in info["items"].items():
    process_item(item, value)

filename = "%s/%s" % (SOURCE_DIR, "manifest/manifest.yaml")
with open(filename) as file:
  manifest = yaml.load(file, Loader=yaml.FullLoader)
  #print(manifest)
  for date, info in manifest.items():
    process_release(date, info)
