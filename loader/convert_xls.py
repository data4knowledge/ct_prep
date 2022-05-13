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
  print("CELL", cell)
  print("CELL", cell == None)
  if cell == "":
    return []
  else:
    return cell.split(";")

def add_code_list(output, row):
  synonyms = get_synonym(row, 7)
  code_list = {
    "conceptId": get_cell(row, 1),
    "definition": get_cell(row, 6),
    "extensible": get_cell(row, 2),
    "name": get_cell(row, 3),
    "preferredTerm": get_cell(row, 5),
    "submissionValue": get_cell(row, 4),
    "synonyms": synonyms,
    "terms": []
  } 
  output["codelists"].append(code_list)
  return code_list
 
def add_code_list_item(output, row):
  synonyms = get_synonym(row, 7)
  code_list_item = {
    "conceptId": get_cell(row, 0),
    "definition": get_cell(row, 6),
    "preferredTerm": get_cell(row, 5),
    "submissionValue": get_cell(row, 4),
    "synonyms": synonyms
  } 
  output["terms"].append(code_list_item)
  return code_list_item

def process_sheet_format_1(df, output, item, date):
  print(df)
  code_list = None
  for index, row in df.iterrows():
    if row['Code'] == row['Codelist Code']:
      code_list = add_code_list(output, row)
    else:
      add_code_list_item(code_list, row)

  return None

def process_sheet_format_2(df, output, item, date):
  return None

def process_sheet_format_3(df, output, item, date):
  return None

def process_sheet_format_4(df, output, item, date):
  return None

def process_sheet_format_5(df, output, item, date):
  return None

def set_format(item, date):
  print("SET_FORMAT %s %s" % (item, date))
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
    return None
  print("READ_SHEET %s %s %s" % (format, item, date))
  filename = "%s/%s/%s %s.xls" % (SOURCE_DIR, item, FILE_MAP[item]["filename"], date)
  df = pd.read_excel (filename, sheet_name(format, item, date))
  return df

def process_sheet(df, format, item, date):
  output = {}
  add_header(output, item, date)
  if format == "1":
    process_sheet_format_1(df, output, item, date)
  elif format == "2":
    process_sheet_format_2(df, output, item, date)
  elif format == "3":
    process_sheet_format_3(df, output, item, date)
  elif format == "4":
    process_sheet_format_4(df, output, item, date)
  else:
    process_sheet_format_5(df, output, item, date)
  return output

def process_item(item, date):
  format = set_format(item, date)
  df = read_sheet(format, item, date)
  output = process_sheet(df, format, item, date)
  with open("%s/%s %s.json" % (OUTPUT_DIR, item, date), 'w') as outfile:
    json.dump(output, outfile)

def process_release(date, info):
  package = info["package"]
  for item, value in info["items"].items():
    process_item(item, value)

filename = "%s/%s" % (SOURCE_DIR, "manifest.yaml")
with open(filename) as file:
  manifest = yaml.load(file, Loader=yaml.FullLoader)
  print(manifest)
  for date, info in manifest.items():
    process_release(date, info)
