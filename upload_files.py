import os
from drive.drive import Drive
from pathlib import Path

drive = Drive()

dir_list = [
  { 
    "path": "source_data/manifest",
    "name": 'manifest'
  },
  { 
    "path": "json_data/adam",
    "name": 'adam'
  }, 
  { 
    "path": "json_data/cdash",
    "name": 'cdash'
  },
  { 
    "path": "json_data/coa",
    "name": 'coa'
  },
  { 
    "path": "json_data/define-xml",
    "name": 'define-xml'
  },
  { 
    "path": "json_data/protocol",
    "name": 'protocol'
  },
  { 
    "path": "json_data/qrs",
    "name": 'qrs'
  },
  { 
    "path": "json_data/qs",
    "name": 'qs'
  },
  { 
    "path": "json_data/qs-ft",
    "name": 'qs-ft'
  },
  { 
    "path": "json_data/sdtm",
    "name": 'sdtm'
  },
  { 
    "path": "json_data/send",
    "name": 'send'
  }
]

project_root = os.path.abspath(os.path.dirname(__file__))
for info in dir_list:
  output_path = os.path.join(project_root, info['path'])
  drive.upload_dir(output_path, info['name'])
