#coding:utf-8
from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config
from pdtb import PDTB
from pdtb_parse import PDTB_PARSE
import util
import string


def get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    alphabet = Alphabet()
    alphabet.add('Arg1')
    alphabet.add('Arg2')
    alphabet.add('NULL')
    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, alphabet)
    return cm

def do_my_evaluation():

    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    # dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pdtb_dev = dev_pdtb_parse.pdtb
    relations = pdtb_dev.relations
    gold_relation_dict = {}
    for relation in relations:
        if relation["Type"] =="Explicit":
            relation_ID = str(relation["ID"])
            Arg1_token_indices = sorted([item[4] for item in relation["Arg1"]["TokenList"]])
            Arg2_token_indices = sorted([item[4] for item in relation["Arg2"]["TokenList"]])
            gold_relation_dict[relation_ID] = (Arg1_token_indices, Arg2_token_indices)


    relation_dict = {}
    #one_SS_conns_parallel,if...then,either..or,neither nor,
    one_SS_conns_parallel = pdtb_dev.one_SS_conns_parallel


    parse_dict = dev_pdtb_parse.parse_dict

    for connective in one_SS_conns_parallel:
        if connective.name == "if then" or connective.name == "either or" \
                or connective.name == "neither nor" :
            relation_ID = str(connective.relation_ID)
            DocID = connective.DocID
            sent_index = connective.sent_index


            conn_1_index = connective.token_indices[0]
            conn_2_index = connective.token_indices[1]

            Arg1 = list(range(conn_1_index+1,conn_2_index))
            for i in range(conn_1_index, conn_2_index):
                if parse_dict[DocID]["sentences"][sent_index]["words"][i][0] in """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""":
                    Arg1 = list(range(conn_1_index+1,i))
                    break
            sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            Arg2 = list(range(conn_2_index+1,sent_length))
            for i in range(conn_2_index, sent_length):
                if parse_dict[DocID]["sentences"][sent_index]["words"][i][0] in """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""":
                    Arg2 = list(range(conn_2_index+1,i))
                    break
            relation_dict[relation_ID] = (Arg1, Arg2)

    relation_dict = {}
    #对于所有的IPS，直接认为前面一句为arg1，连接词所在的句子为Arg2（去连接词）
    IPS_conns = pdtb_dev.IPS_conns

    c = 0
    for connective in IPS_conns:
        relation_ID = str(connective.relation_ID)
        DocID = connective.DocID
        sent_index = connective.sent_index
        conn_indices = connective.token_indices

        #获取前一句的长度
        prev_length = len(parse_dict[DocID]["sentences"][sent_index - 1]["words"])
        Arg1 = [(index, parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0]) for index in range(0, prev_length)]

        #去两边的标点
        Arg1 = util.list_strip_punctuation(Arg1)

        # if Arg1[-1][-1] == "says":
        #     i = len(Arg1) - 1
        #     while i >= 0 and Arg1[i][-1] != "''":
        #         i -= 1
        #     if i >= 0:
        #         Arg1 = Arg1[:i]
        # Arg1 = util.list_strip_punctuation(Arg1)




        #当前句子的长度
        curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg2 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, curr_length)]
        #去根据连接词划分
        Arg2_part1 = Arg2[: conn_indices[0]]
        Arg2_part2 = Arg2[conn_indices[-1] + 1:]


        Arg2_part1 = util.list_strip_punctuation(Arg2_part1)
        Arg2_part2 = util.list_strip_punctuation(Arg2_part2)

        Arg2 = Arg2_part1 + Arg2_part2


        # if Arg2[-1][-1] == "says":
        #     i = len(Arg2) - 1
        #     while i >= 0 and Arg2[i][-1] != "''":
        #         i -= 1
        #     if i >= 0:
        #         Arg2 = Arg2[:i]
        # if Arg2[-1][-1] == "said":
        #     i = len(Arg2) - 1
        #     while i >= 0 and Arg2[i][-1] != "''":
        #         i -= 1
        #     if i >= 0:
        #         Arg2 = Arg2[:i]
        Arg2 = util.list_strip_punctuation(Arg2)



        Arg1 = [item[0] for item in Arg1]
        Arg2 = [item[0] for item in Arg2]




        relation_dict[relation_ID] = (Arg1, Arg2)


        Ag1_text = " ".join([parse_dict[DocID]["sentences"][sent_index-1]["words"][index][0] for index in range(prev_length)])
        Ag2_text = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])

        Ag1_text_indices = " ".join([ "%d:%s" % (index, parse_dict[DocID]["sentences"][sent_index-1]["words"][index][0]) for index in range(prev_length)])
        Ag2_text_indices = " ".join([ "%d:%s" % (index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(curr_length)])



        # print connective.name , connective.token_indices
        # print relation_ID, DocID, sent_index



        if connective.token_indices[0] < 3:
            c +=1

        Arg1_gold, Arg2_gold = gold_relation_dict[relation_ID]

        Arg1_gold_words = " ".join([parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0] for index in Arg1_gold])

        print("**" * 45)
        print(Arg1_gold_words)

        #只去处标点的Arg1 － gold Arg1

        left_token_list = set(Arg1) - set(Arg1_gold)
        left_words = " ".join([parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0] for index in sorted(left_token_list)])

        # print left_words

        # if Arg2 != Arg2_gold:
        #     print "_"*80
        #     print DocID, sent_index
        #     print Ag2_text_indices
        #     print (Ag2_text)
        #     print (Arg2)
        #     print Arg2_gold
        #     print connective.token_indices, connective.name

    # print c

    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0

    for relation_ID in list(relation_dict.keys()):
        gold_Arg1_indices, gold_Arg2_indices = gold_relation_dict[relation_ID]
        pred_Arg1_indices, pred_Arg2_indices = relation_dict[relation_ID]

        if gold_Arg1_indices == pred_Arg1_indices:
            Arg1_right_count += 1

        if gold_Arg2_indices == pred_Arg2_indices:
            Arg2_right_count += 1

        if gold_Arg1_indices == pred_Arg1_indices and gold_Arg2_indices == pred_Arg2_indices:
            Arg1_and_Arg2_right_count += 1

    S = float(len(relation_dict))
    print("IPS size: %d" % (len(IPS_conns)))
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))








do_my_evaluation()
