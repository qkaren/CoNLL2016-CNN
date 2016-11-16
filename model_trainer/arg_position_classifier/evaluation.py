from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config

def get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    gold_list = [config.LABEL_TO_ARG_POSITION[item] for item in gold_list]

    predicted_list = get_mallet_predicted_list(result_file_path)
    predicted_list = [config.LABEL_TO_ARG_POSITION[item] for item in predicted_list]

    binary_alphabet = Alphabet()
    for key in list(config.LABEL_TO_ARG_POSITION.keys()):
        print(config.LABEL_TO_ARG_POSITION[key])
        binary_alphabet.add(config.LABEL_TO_ARG_POSITION[key])

    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)
    return cm

def get_evaluation_feat_combine(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)

    binary_alphabet = Alphabet()
    binary_alphabet.add("0")
    binary_alphabet.add("1")

    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)
    return cm



