#coding:utf-8
import config
from pdtb_parse import PDTB_PARSE
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper
from collections import Counter
import json

def expand_implicit_instance(to_file):
    # conn -> sense
    file = open(config.FREELY_OMISSIBLE_CONNECTIVES_PATH)

    conn_to_sense = {}
    for line in file:
        line = line.strip()
        conn, sense = line.split(" -> ")
        conn_to_sense[conn] = sense

    extra_implicit_relations = []
    sense_counter = Counter()
    conn_counter = Counter()

    #pdtb
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    relations = pdtb_parse.pdtb.explicit_relations
    for relation in relations:
        #需要获取语篇连接词的头
        raw_connective = relation["Connective"]["RawText"]
        chm = ConnHeadMapper()
        conn_head, indices = chm.map_raw_connective(raw_connective)

        if conn_head in conn_to_sense:
            sense = conn_to_sense[conn_head]
            #修改Type
            relation["Type"] = "Implicit"
            #修改sense
            relation["Sense"] = [sense]

            extra_implicit_relations.append(relation)

            sense_counter[sense] += 1
            conn_counter[conn_head] += 1

    print(sense_counter.most_common())
    print(conn_counter.most_common())
    print(len(extra_implicit_relations))

    #写入文件
    all_relations = pdtb_parse.pdtb.relations + extra_implicit_relations
    fout = open(to_file, 'w')
    for relation in all_relations:
        fout.write('%s\n' % json.dumps(relation))
    fout.close()

if __name__ == "__main__":
    to_file = config.TRAIN_PATH + "expanded_pdtb_data.json"
    expand_implicit_instance(to_file)