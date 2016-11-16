#coding:utf-8
from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config
from pdtb import PDTB
import json, os
from collections import Counter
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper



def get_evaluation(result_file_path):

    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    for key in list(config.Sense_To_Label.keys()):
        binary_alphabet.add(key)

    predicted_list = [ config.Label_To_Sense[item] for item in predicted_list]
    gold_list = [ config.Label_To_Sense[item] for item in gold_list]

    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)

    write_result_to_json(predicted_list)

    return cm



def write_result_to_json(predicted_list):
    output =[]

    pdtb_dev = PDTB(config.PDTB_DEV_PATH, config.DEV)
    relations = pdtb_dev.relations

    relations_exp =[]

    relation_ID_to_index = {}
    for index, relation in enumerate(relations):
        if relation["Type"] =="Explicit":
            relation_ID = str(relation["ID"])
            relation_ID_to_index[relation_ID] = index

    #关系分错的连接词的计数
    err_conn_count = Counter()
    err_conn_sense_count = {}

    dev_feature_file = open(config.EXPLICIT_DEV_FEATURE_OUTPUT_PATH)
    lines = [line.strip() for line in dev_feature_file]
    for i, line in enumerate(lines):
        relation_ID = line.split("#")[1].strip()

        relation = relations[relation_ID_to_index[relation_ID]]

        pred_sense = predicted_list[i]
        if pred_sense not in relation["Sense"]:#预测错误
            if relation["Connective"]["RawText"] == "as":
                print("--" * 45)
                print(relation["Arg1"]["RawText"], end=' ')
                print("%s" % relation["Connective"]["RawText"], end=' ')
                print(relation["Arg2"]["RawText"])
                print("[%s]" % relation["Connective"]["RawText"])
                print(pred_sense)
                print(" ".join(relation["Sense"]))

            raw_connective = relation["Connective"]["RawText"]
            chm = ConnHeadMapper()
            conn_head, indices = chm.map_raw_connective(raw_connective)
            err_conn_count[conn_head] += 1

            if conn_head not in err_conn_sense_count:
                err_conn_sense_count[conn_head] = Counter()

            err_conn_sense_count[conn_head]["%s->%s" % (" ".join(relation["Sense"]), pred_sense)] += 1




        relation["Sense"] = [pred_sense]
        relation["Arg1"]["TokenList"] =  [item[2] for item in relation["Arg1"]["TokenList"]]
        relation["Arg2"]["TokenList"] =  [item[2] for item in relation["Arg2"]["TokenList"]]
        relation["Connective"]["TokenList"] = [item[2] for item in relation["Connective"]["TokenList"]]

        #


        output.append(relation)

    fout = open(config.JSON_DEV_OUTPUT_PATH, 'w')
    for relation in output:
        fout.write('%s\n' % json.dumps(relation))
    fout.close()

    for x, count in err_conn_count.most_common():
        print(x, count)
    # for x, count in err_conn_count.most_common():
    #     print count
    #
    # for conn_head, _ in  err_conn_count.most_common():
    #     print " ".join(["%s:%d" % (x, y) for x, y in err_conn_sense_count[conn_head].most_common()])



    cmd = "python "+config.SCORER_PATH+" " \
          " "+config.JSON_GOLD_EXPLICIT_PATH+" "+config.JSON_DEV_OUTPUT_PATH+" "
    os.system(cmd)

def get_my_evaluation(result_file_path):

    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    for key in list(config.Sense_To_Label.keys()):
        binary_alphabet.add(key)

    predicted_list = [ config.Label_To_Sense[item] for item in predicted_list]
    gold_list = [ config.Label_To_Sense[item] for item in gold_list]

    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)


    return cm


if __name__ == "__main__":
    cm = get_evaluation(config.EXPLICIT_DEV_OUTPUT_PATH)
    cm.print_out()