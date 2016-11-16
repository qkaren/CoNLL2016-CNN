#coding:utf-8
import sys
# import imp
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')
sys.path.append("./")
import json
import parser_util
import config
import cnn_test
import pickle

from model_trainer.connective_classifier.feature_functions \
    import all_features as _conn_clf_feature_function

from model_trainer.arg_position_classifier.feature_functions\
    import all_features as _arg_position_feature_function

from model_trainer.NT_arg_extractor.feature_functions \
    import all_features as _constituent_feat_func

from model_trainer.Explicit_classifier.feature_functions \
    import all_features as _explicit_feat_func

from model_trainer.Non_Explicit_classifier.feature_functions \
    import all_features as _non_explicit_feat_func, prev_context_conn


from model_trainer.PS_Arg2_extractor.feature_functions \
    import all_features as _ps_arg2_extractor_feat_func

from model_trainer.PS_Arg1_extractor.feature_functions \
    import all_features as _ps_arg1_extractor_feat_func

from model_trainer.Implicit_Arg1_extractor.feature_functions \
    import all_features as _implicit_arg1_feat_func

from model_trainer.Implicit_Arg2_extractor.feature_functions \
    import all_features as _implicit_arg2_feat_func

import codecs

def data_process_special(relations_file,parses_file):
    rf = open(relations_file)
    pf = open(parses_file)
    relations = [json.loads(x) for x in rf]
    parse_dict = json.load(codecs.open(parses_file, encoding='utf8'))
    relation = []
    flag= 0
    for r in relations:
        docid = r['DocID']
        type = r['Type']
        sense = r['Sense']
        if type == 'Explicit':
            continue
        ''' arg_offset_list = [sentence_index,wordinsentence_index] from TokenList in relations '''
        arg1_tokenlist = [[t[3],t[4]] for t in r['Arg1']['TokenList']]
        arg2_tokenlist = [[t[3],t[4]] for t in r['Arg2']['TokenList']]
        arg1_word = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][0] for sent_index,word_index in arg1_tokenlist]
        arg1_pos = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"] for sent_index,word_index in arg1_tokenlist]
        arg2_word = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][0] for sent_index,word_index in arg2_tokenlist]
        arg2_pos = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"] for sent_index,word_index in arg2_tokenlist]
        relation.append((arg1_word,arg2_word,arg1_pos,arg2_pos,sense,r))
    return relation

class DiscourseParser():
    def __init__(self, input_dataset, input_run):
        self.pdtb_parse = '%s/parses.json' % input_dataset
        self.raw_path = '%s/raw' % input_dataset
        self.input_run = input_run
        self.relations = []
        self.explicit_relations = []
        self.non_explicit_relations = []


        self.documents = json.loads(codecs.open(self.pdtb_parse, encoding="utf-8", errors="ignore").read())

        self.parse_dict = self.documents

        pass

    def parse(self):
        if 0:
            instances = json.loads(open("cnn-inst.json").read())
        else:
            dev_file_path = "data/conll16st-en-01-12-16-dev/"
            parses_file_name = dev_file_path+"parses.json"
            relations_file_name = dev_file_path+"relations.json"
            instances = data_process_special(relations_file_name,parses_file_name)
        # instances = parser_util.get_CNN_input(CNN_input_file_path)
        cnn_noexp_output = cnn_test.test(instances)

        self.relations = [i[5] for i in instances]
        from model_trainer.cnn_noexp_classifier import cnn_config
        import numpy as np
        for i,r in enumerate(self.relations):
            r['Arg1']['TokenList'] = [t[2] for t in r['Arg1']['TokenList']]
            r['Arg2']['TokenList'] = [t[2] for t in r['Arg2']['TokenList']]
            r["Sense"] = [cnn_config.Label_To_Sense[np.argmax(cnn_noexp_output[i])]]

if __name__ == '__main__':

    # input_dataset = sys.argv[1]
    # input_run = sys.argv[2]
    # output_dir = sys.argv[3]

    input_dataset = '/Users/tao/Documents/conll/conll2015_new/data/conll16st-en-01-12-16-dev'
    input_run = ''
    output_dir = '/Users/tao/Documents/conll/conll2015_new/data'

    parser = DiscourseParser(input_dataset, input_run)
    parser.parse()

    relations = parser.relations

    output = open('%s/output-testlastcnn.json' % output_dir, 'w')
    for relation in relations:
        output.write('%s\n' % json.dumps(relation))
    output.close()

    import os
    os.system("python2.7 /Users/tao/Documents/conll/conll16st-master-4/scorer.py /Users/tao/Documents/conll/conll2015_new/data/conll16st-en-01-12-16-dev/relations.json   "
            + '%s/output-testlastcnn.json' % output_dir)


