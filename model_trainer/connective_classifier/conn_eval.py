#coding:utf-8
from model_trainer.mallet_util import *
from operator import itemgetter
from model_trainer.confusion_matrix import ConfusionMatrix, Alphabet
from pdtb_parse import PDTB_PARSE
from pdtb import PDTB
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper

# gold_list = ['no', 'yes', 'no', 'yes', ...]
# predicted_list = ['yes', 'yes', 'no', 'yes', ...]
def compute_binary_eval_metric(predicted_list, gold_list, binary_alphabet):
    cm = ConfusionMatrix(binary_alphabet)
    FP = []
    FN = []
    TP = []
    TN = []

    for index, (predicted_span, gold_span) in enumerate(zip( predicted_list, gold_list)):
        if predicted_span == "1" and gold_span == "0":
            FP.append(index)
        if predicted_span == "0" and gold_span == "1":
            FN.append(index)

        if predicted_span == "1" and gold_span == "1":
            TP.append(index)
        if predicted_span == "0" and gold_span == "0":
            TN.append(index)

        cm.add(predicted_span, gold_span)
    return cm, FP, FN, TP, TN

# until|wsj_2267|3|24 25

def get_index_map(dev_feat_file):
    index_map = {}
    file = open(dev_feat_file)
    for index, line in enumerate(file.readlines()):
        conn_name, DocID, sent_index, indices_string = line.split("#")[-1].strip().split("|")
        index_map[index] = (conn_name, DocID, sent_index, indices_string)
    return index_map


def ___get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    binary_alphabet.add('1')
    binary_alphabet.add('0')
    cm, FP, FN, TP, TN = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)

    #
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict


    index_map = get_index_map(config.CONNECTIVE_DEV_FEATURE_OUTPUT_PATH)
    FP_instances = []
    for index in FP:
        FP_instances.append(index_map[index])
    FP_instances = sorted(FP_instances, key=itemgetter(0))

    err_conn_count = {}

    for instance in FP_instances:
        conn_name, DocID, sent_index, indices_string = instance
        sent_index = int(sent_index)
        curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        print("--" * 45)
        print(" ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)]))
        # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["NER_TAG"] for index in range(curr_length)])
        print(instance)

        if conn_name not in err_conn_count:
            err_conn_count[conn_name] = 0
        err_conn_count[conn_name] += 1

    print("**" * 45)
    for conn_name in err_conn_count:
        print("%s: %d" % (conn_name, err_conn_count[conn_name]))
    print("**" * 45)

    cm.print_out()

    print("-- right instances --")

    _conn_name = "and"
    get_right_instances_from_training_data(_conn_name)


    # TP_instances = []
    # for index in TP:
    #     TP_instances.append(index_map[index])


    # _conn_name = "until"
    # for instance in TP_instances:
    #     conn_name, DocID, sent_index, indices_string = instance
    #     if conn_name == _conn_name:
    #         sent_index = int(sent_index)
    #         curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    #         print "**" * 45
    #         print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
    #         # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["NER_TAG"] for index in range(curr_length)])
    #         print instance
    return cm

def get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    binary_alphabet.add('1')
    binary_alphabet.add('0')
    cm, FP, FN, TP, TN = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)
    return cm

def get_right_instances_from_training_data(conn_name):
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    parse_dict = train_pdtb_parse.parse_dict

    explicit_relations = train_pdtb_parse.pdtb.explicit_relations
    for relation in explicit_relations:
        DocID = relation["DocID"]
        sent_index = relation["Connective"]["TokenList"][0][3]
        conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
        #需要将获取语篇连接词的头
        raw_connective = relation["Connective"]["RawText"]
        chm = ConnHeadMapper()
        conn_head, indices = chm.map_raw_connective(raw_connective)
        conn_head_indices = [conn_token_indices[index] for index in indices]
        raw_conn_head = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_head_indices ])

        if raw_conn_head == conn_name:
            curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            print("**" * 45)
            print(" ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)]))
            # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["NER_TAG"] for index in range(curr_length)])
            print(conn_name)
            print(DocID, sent_index, conn_head_indices)


if __name__ == "__main__":
    import config
    dev_result_file_path = config.CONNECTIVE_DEV_OUTPUT_PATH
    cm = ___get_evaluation(dev_result_file_path)
