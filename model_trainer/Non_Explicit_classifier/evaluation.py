from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config
from pdtb import PDTB
import json, os



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


    pdtb_dev = PDTB(config.PDTB_DEV_PATH, config.DEV)
    gold_relations = pdtb_dev.relations

    relation_ID_to_index = {}
    for index, relation in enumerate(gold_relations):
        relation_ID = str(relation["ID"])
        relation_ID_to_index[relation_ID] = index


    pred_relations = []

    dev_feature_file = open(config.NON_EXPLICIT_DEV_FEATURE_OUTPUT_PATH)
    lines = [line.strip() for line in dev_feature_file]
    for i, line in enumerate(lines):
        relation_ID = line.split("#")[1].strip()

        pred_relation = gold_relations[relation_ID_to_index[relation_ID]]

        pred_sense = predicted_list[i]
        pred_relation["Sense"] = [pred_sense]
        pred_relation["Arg1"]["TokenList"] = [item[2] for item in pred_relation["Arg1"]["TokenList"]]
        pred_relation["Arg2"]["TokenList"] = [item[2] for item in pred_relation["Arg2"]["TokenList"]]

        pred_relations.append(pred_relation)

    fout = open(config.JSON_DEV_OUTPUT_PATH, 'w')
    for relation in pred_relations:
        fout.write('%s\n' % json.dumps(relation))
    fout.close()



    cmd = "python " + config.SCORER_PATH + \
          " "+config.JSON_GOLD_NON_EXPLICIT_PATH+" "+config.JSON_DEV_OUTPUT_PATH+" "
    os.system(cmd)


def get_evaluation_LM(result_file_path):

    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    for key in list(config.Sense_To_Label.keys()):
        binary_alphabet.add(key)

    predicted_list = [ config.Label_To_Sense[item] for item in predicted_list]
    gold_list = [ config.Label_To_Sense[item] for item in gold_list]

    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)

    return write_result_to_json_LM(predicted_list)



def write_result_to_json_LM(predicted_list):


    pdtb_dev = PDTB(config.PDTB_DEV_PATH, config.DEV)
    gold_relations = pdtb_dev.relations

    relation_ID_to_index = {}
    for index, relation in enumerate(gold_relations):
        relation_ID = str(relation["ID"])
        relation_ID_to_index[relation_ID] = index


    pred_relations = []

    dev_feature_file = open(config.NON_EXPLICIT_DEV_FEATURE_OUTPUT_PATH)
    lines = [line.strip() for line in dev_feature_file]
    for i, line in enumerate(lines):
        relation_ID = line.split("#")[1].strip()

        pred_relation = gold_relations[relation_ID_to_index[relation_ID]]

        pred_sense = predicted_list[i]
        pred_relation["Sense"] = [pred_sense]
        pred_relation["Arg1"]["TokenList"] = [item[2] for item in pred_relation["Arg1"]["TokenList"]]
        pred_relation["Arg2"]["TokenList"] = [item[2] for item in pred_relation["Arg2"]["TokenList"]]

        pred_relations.append(pred_relation)

    fout = open(config.JSON_DEV_OUTPUT_PATH, 'w')
    for relation in pred_relations:
        fout.write('%s\n' % json.dumps(relation))
    fout.close()



    cmd = "python " + config.SCORER_PATH + \
          " "+config.JSON_GOLD_NON_EXPLICIT_PATH+" "+config.JSON_DEV_OUTPUT_PATH+" "
    result = os.popen(cmd)
    # 'Precision %s Recall %s F1 %s'
    F1 = float(result.readlines()[-1].strip().split(" ")[-1])

    return F1


if __name__ == "__main__":
   cm = get_evaluation(config.NON_EXPLICIT_DEV_OUTPUT_PATH)
   cm.print_out()