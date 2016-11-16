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

    binary_alphabet.add("0")
    binary_alphabet.add("1")


    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)

    return cm

def write_result_to_file(cm, feature_function_list, to_file):
    f_out = open(to_file, "a")
    line = "--" * 45 + "\n"
    f_out.write(line)
    f_out.write("feature : %s\n" % (" ".join([f.__name__ for f in feature_function_list])))
    p, r, f1 = cm.get_average_prf()
    f_out.write("marco f1 : %.2f\n" % f1)

    f_out.write(cm.get_matrix() + "\n")
    f_out.write(cm.get_summary() + "\n")
    f_out.write(line)
    f_out.close()

import numpy as np

if __name__ == "__main__":
    cm = get_evaluation(config.COMP_CONTRAST_DEV_OUTPUT_PATH)
    print(cm.get_matrix())
    print(cm.get_summary())
    print(cm.get_average_prf())

    p, r, f1 = cm.get_average_prf()
    print(np.nan_to_num(r))
    if f1 == "nan":
        print(2)


