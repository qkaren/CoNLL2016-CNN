import codecs
import sys
sys.path.append("./")
import json
from conn_head_mapper import ConnHeadMapper

trian_file_path = "../../data/conll16st-en-01-12-16-train/relations.json"
dev_file_path = "../../data/conll16st-en-01-12-16-dev/relations.json"
train = [json.loads(x) for x in open(trian_file_path)]
dev = [json.loads(x) for x in open(dev_file_path)]

# 1.read
d = {}
for r in train:
    if r['Type'] == 'Explicit':
        connective_raw = r['Connective']['RawText']
        connective_mapping = ConnHeadMapper.DEFAULT_MAPPING[connective_raw]
        if connective_mapping not in d:
            d[connective_mapping] = {}
        sense = r['Sense'][0]
        if sense not in d[connective_mapping]:
            d[connective_mapping][sense] = 0
        d[connective_mapping][sense] += 1

# 2.get-max
mostd = {}
for k in d:
    most = 0
    mstr = ""
    for one in d[k]:
        if d[k][one] > most:
            most = d[k][one]
            mstr = one
    mostd[k] = mstr

# 3.evaluate
all = 0
right = 0
for r in train:
    if r['Type'] == 'Explicit':
        all += 1
        connective_raw = r['Connective']['RawText']
        connective_mapping = ConnHeadMapper.DEFAULT_MAPPING[connective_raw]
        if(r['Sense'][0] == mostd[connective_mapping]):
            right += 1
print("train",right/all)
all = 0
right = 0
for r in dev:
    if r['Type'] == 'Explicit':
        all += 1
        connective_raw = r['Connective']['RawText']
        connective_mapping = ConnHeadMapper.DEFAULT_MAPPING[connective_raw]
        if(r['Sense'][0] == mostd[connective_mapping]):
            right += 1
print("dev",right/all)
