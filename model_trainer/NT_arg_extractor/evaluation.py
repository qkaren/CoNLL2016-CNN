#coding:utf-8
from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config
from pdtb import PDTB
from pdtb_parse import PDTB_PARSE
import util


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
    dev_feat_file = open(config.NT_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.NT_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pdtb_dev = dev_pdtb_parse.pdtb
    parse_dict = dev_pdtb_parse.parse_dict
    relations = pdtb_dev.relations
    gold_relation_dict = {}
    gold_relation_DocID_Sent_index = {}
    for relation in relations:
        if relation["Type"] =="Explicit":
            relation_ID = str(relation["ID"])
            DocID = relation["DocID"]
            sent_index = relation["Arg1"]["TokenList"][0][3]
            conn_name = relation["Connective"]["RawText"]
            conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]

            Arg1_token_indices = sorted([item[4] for item in relation["Arg1"]["TokenList"]])
            Arg2_token_indices = sorted([item[4] for item in relation["Arg2"]["TokenList"]])
            gold_relation_dict[relation_ID] = (Arg1_token_indices, Arg2_token_indices)
            gold_relation_DocID_Sent_index[relation_ID] = (DocID, sent_index, conn_name, conn_indices)



    feature_list = [line.strip() for line in dev_feat_file]

    # relation_dict[relation_ID] = {(['1', '2'],'Arg1')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = comment.split("|")[0].strip()
        constituent_indices = comment.split("|")[1].strip().split(" ")
        if relation_ID not in relation_dict:
            relation_dict[relation_ID] = [(constituent_indices, predicted)]
        else:
            relation_dict[relation_ID].append((constituent_indices, predicted))

    #对每一个relation的arg1,arg2进行合并
    for relation_ID in relation_dict.keys():
        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]

        list = relation_dict[relation_ID]
        Arg1_list = []
        Arg2_list = []
        for span, label in list:# 合并是请补上标点符号，亲！
            if label == "Arg1":
                Arg1_list.extend(span)
            if label == "Arg2":
                Arg2_list.extend(span)

        Arg1_list = sorted([int(item) for item in Arg1_list])
        Arg2_list = sorted([int(item) for item in Arg2_list])

        Arg1_list = merge_NT_Arg(Arg1_list, parse_dict, DocID, sent_index)
        Arg2_list = merge_NT_Arg(Arg2_list, parse_dict, DocID, sent_index)

        # if Arg1_list == [] or Arg2_list == []: #有空的pop掉，以免影响 P
        #     relation_dict.pop(relation_ID)
        # else:
        #     relation_dict[relation_ID] = (Arg1_list, Arg2_list)
        relation_dict[relation_ID] = (Arg1_list, Arg2_list)

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0

    for relation_ID in relation_dict.keys():
        gold_Arg1_indices, gold_Arg2_indices = gold_relation_dict[relation_ID]
        pred_Arg1_indices, pred_Arg2_indices = relation_dict[relation_ID]


        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)])

        if gold_Arg1_indices != pred_Arg1_indices:
            pass
            print("-"*100)
            print(" ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)]))
            print(Arg_raw)
            print(pred_Arg1_indices, pred_Arg2_indices)
            print(gold_Arg1_indices, gold_Arg2_indices)
            print(conn_name, " ".join([str(i) for i in conn_indices]))


        if gold_Arg1_indices == pred_Arg1_indices:

            # print "-"*100
            # print " ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)])
            # print Arg_raw
            # print pred_Arg1_indices, pred_Arg2_indices
            # print gold_Arg1_indices, gold_Arg2_indices
            # print conn_name, " ".join([str(i) for i in conn_indices])

            Arg1_right_count += 1

        if gold_Arg2_indices == pred_Arg2_indices:
            Arg2_right_count += 1

        if gold_Arg1_indices == pred_Arg1_indices and gold_Arg2_indices == pred_Arg2_indices:
            Arg1_and_Arg2_right_count += 1

    S = float(len(relation_dict))
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))

    # relation_dict = {}
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

    #对于所有的PS，直接认为前面一句为arg1，连接词所在的句子为Arg2（去连接词）
    # IPS_conns = pdtb_dev.IPS_conns
    # print "IPS size: %d" % (len(IPS_conns))
    not_one_SS_conns = pdtb_dev.not_one_SS_conns

    for connective in not_one_SS_conns:
        relation_ID = str(connective.relation_ID)
        DocID = connective.DocID
        sent_index = connective.sent_index
        conn_indices = connective.token_indices



        #获取前一句的长度
        prev_length = len(parse_dict[DocID]["sentences"][sent_index - 1]["words"])
        Arg1 = [(index, parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0]) for index in range(0, prev_length)]

        #去两边的标点
        Arg1 = util.list_strip_punctuation(Arg1)


        #当前句子的长度
        curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg2 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, curr_length)]
        #去根据连接词划分
        Arg2_part1 = Arg2[: conn_indices[0]]
        Arg2_part2 = Arg2[conn_indices[-1] + 1:]


        Arg2_part1 = util.list_strip_punctuation(Arg2_part1)
        Arg2_part2 = util.list_strip_punctuation(Arg2_part2)

        Arg2 = Arg2_part1 + Arg2_part2

        Arg1 = [item[0] for item in Arg1]
        Arg2 = [item[0] for item in Arg2]






        relation_dict[relation_ID] = (Arg1, Arg2)


        Ag1_text = " ".join([parse_dict[DocID]["sentences"][sent_index-1]["words"][index][0] for index in Arg1])
        Ag2_text = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in Arg2])

        # print "_"*80
        # print connective.name , connective.token_indices
        # print relation_ID, DocID, sent_index
        #
        #
        # print (Ag1_text, Ag2_text)
        # print (Arg1,Arg2)
        # print gold_relation_dict[relation_ID]


    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0

    for relation_ID in relation_dict.keys():
        gold_Arg1_indices, gold_Arg2_indices = gold_relation_dict[relation_ID]
        pred_Arg1_indices, pred_Arg2_indices = relation_dict[relation_ID]

        if gold_Arg1_indices == pred_Arg1_indices:
            Arg1_right_count += 1

        if gold_Arg2_indices == pred_Arg2_indices:
            Arg2_right_count += 1

        if gold_Arg1_indices == pred_Arg1_indices and gold_Arg2_indices == pred_Arg2_indices:
            Arg1_and_Arg2_right_count += 1

    S = float(len(relation_dict))
    print(S)
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))

def get_Both_ACC():
    dev_feat_file = open(config.NT_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.NT_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pdtb_dev = dev_pdtb_parse.pdtb
    parse_dict = dev_pdtb_parse.parse_dict
    relations = pdtb_dev.relations
    gold_relation_dict = {}
    gold_relation_DocID_Sent_index = {}
    for relation in relations:
        if relation["Type"] =="Explicit":
            relation_ID = str(relation["ID"])
            DocID = relation["DocID"]
            sent_index = relation["Arg1"]["TokenList"][0][3]
            conn_name = relation["Connective"]["RawText"]
            conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]

            Arg1_token_indices = sorted([item[4] for item in relation["Arg1"]["TokenList"]])
            Arg2_token_indices = sorted([item[4] for item in relation["Arg2"]["TokenList"]])
            gold_relation_dict[relation_ID] = (Arg1_token_indices, Arg2_token_indices)
            gold_relation_DocID_Sent_index[relation_ID] = (DocID, sent_index, conn_name, conn_indices)



    feature_list = [line.strip() for line in dev_feat_file]

    # relation_dict[relation_ID] = {(['1', '2'],'Arg1')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = comment.split("|")[0].strip()
        constituent_indices = comment.split("|")[1].strip().split(" ")
        if relation_ID not in relation_dict:
            relation_dict[relation_ID] = [(constituent_indices, predicted)]
        else:
            relation_dict[relation_ID].append((constituent_indices, predicted))

    #对每一个relation的arg1,arg2进行合并
    for relation_ID in relation_dict.keys():
        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]

        list = relation_dict[relation_ID]
        Arg1_list = []
        Arg2_list = []
        for span, label in list:# 合并是请补上标点符号，亲！
            if label == "Arg1":
                Arg1_list.extend(span)
            if label == "Arg2":
                Arg2_list.extend(span)

        Arg1_list = sorted([int(item) for item in Arg1_list])
        Arg2_list = sorted([int(item) for item in Arg2_list])

        Arg1_list = merge_NT_Arg(Arg1_list, parse_dict, DocID, sent_index)
        Arg2_list = merge_NT_Arg(Arg2_list, parse_dict, DocID, sent_index)

        # if Arg1_list == [] or Arg2_list == []: #有空的pop掉，以免影响 P
        #     relation_dict.pop(relation_ID)
        # else:
        #     relation_dict[relation_ID] = (Arg1_list, Arg2_list)
        relation_dict[relation_ID] = (Arg1_list, Arg2_list)

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0

    for relation_ID in relation_dict.keys():
        gold_Arg1_indices, gold_Arg2_indices = gold_relation_dict[relation_ID]
        pred_Arg1_indices, pred_Arg2_indices = relation_dict[relation_ID]


        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)])

        if gold_Arg1_indices != pred_Arg1_indices:
            pass
            # print "-"*100
            # print " ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)])
            # print Arg_raw
            # print pred_Arg1_indices, pred_Arg2_indices
            # print gold_Arg1_indices, gold_Arg2_indices
            # print conn_name, " ".join([str(i) for i in conn_indices])


        if gold_Arg1_indices == pred_Arg1_indices:

            # print "-"*100
            # print " ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)])
            # print Arg_raw
            # print pred_Arg1_indices, pred_Arg2_indices
            # print gold_Arg1_indices, gold_Arg2_indices
            # print conn_name, " ".join([str(i) for i in conn_indices])

            Arg1_right_count += 1

        if gold_Arg2_indices == pred_Arg2_indices:
            Arg2_right_count += 1

        if gold_Arg1_indices == pred_Arg1_indices and gold_Arg2_indices == pred_Arg2_indices:
            Arg1_and_Arg2_right_count += 1

    S = float(len(relation_dict))
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))

    return Arg1_and_Arg2_right_count / S * 100


def get_Both_ACC_feat_combine(dev_feat_path, dev_output_path):
    dev_feat_file = open(dev_feat_path)
    predicted_list = get_mallet_predicted_list(dev_output_path)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pdtb_dev = dev_pdtb_parse.pdtb
    parse_dict = dev_pdtb_parse.parse_dict
    relations = pdtb_dev.relations
    gold_relation_dict = {}
    gold_relation_DocID_Sent_index = {}
    for relation in relations:
        if relation["Type"] =="Explicit":
            relation_ID = str(relation["ID"])
            DocID = relation["DocID"]
            sent_index = relation["Arg1"]["TokenList"][0][3]
            conn_name = relation["Connective"]["RawText"]
            conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]

            Arg1_token_indices = sorted([item[4] for item in relation["Arg1"]["TokenList"]])
            Arg2_token_indices = sorted([item[4] for item in relation["Arg2"]["TokenList"]])
            gold_relation_dict[relation_ID] = (Arg1_token_indices, Arg2_token_indices)
            gold_relation_DocID_Sent_index[relation_ID] = (DocID, sent_index, conn_name, conn_indices)



    feature_list = [line.strip() for line in dev_feat_file]

    # relation_dict[relation_ID] = {(['1', '2'],'Arg1')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = comment.split("|")[0].strip()
        constituent_indices = comment.split("|")[1].strip().split(" ")
        if relation_ID not in relation_dict:
            relation_dict[relation_ID] = [(constituent_indices, predicted)]
        else:
            relation_dict[relation_ID].append((constituent_indices, predicted))

    #对每一个relation的arg1,arg2进行合并
    for relation_ID in relation_dict.keys():
        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]

        list = relation_dict[relation_ID]
        Arg1_list = []
        Arg2_list = []
        for span, label in list:# 合并是请补上标点符号，亲！
            if label == "Arg1":
                Arg1_list.extend(span)
            if label == "Arg2":
                Arg2_list.extend(span)

        Arg1_list = sorted([int(item) for item in Arg1_list])
        Arg2_list = sorted([int(item) for item in Arg2_list])

        Arg1_list = merge_NT_Arg(Arg1_list, parse_dict, DocID, sent_index)
        Arg2_list = merge_NT_Arg(Arg2_list, parse_dict, DocID, sent_index)

        # if Arg1_list == [] or Arg2_list == []: #有空的pop掉，以免影响 P
        #     relation_dict.pop(relation_ID)
        # else:
        #     relation_dict[relation_ID] = (Arg1_list, Arg2_list)
        relation_dict[relation_ID] = (Arg1_list, Arg2_list)

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0

    for relation_ID in relation_dict.keys():
        gold_Arg1_indices, gold_Arg2_indices = gold_relation_dict[relation_ID]
        pred_Arg1_indices, pred_Arg2_indices = relation_dict[relation_ID]


        DocID, sent_index, conn_name, conn_indices= gold_relation_DocID_Sent_index[relation_ID]
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)])

        if gold_Arg1_indices != pred_Arg1_indices:
            pass
            # print "-"*100
            # print " ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)])
            # print Arg_raw
            # print pred_Arg1_indices, pred_Arg2_indices
            # print gold_Arg1_indices, gold_Arg2_indices
            # print conn_name, " ".join([str(i) for i in conn_indices])


        if gold_Arg1_indices == pred_Arg1_indices:

            # print "-"*100
            # print " ".join([str(index)+":"+ parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, sent_length)])
            # print Arg_raw
            # print pred_Arg1_indices, pred_Arg2_indices
            # print gold_Arg1_indices, gold_Arg2_indices
            # print conn_name, " ".join([str(i) for i in conn_indices])

            Arg1_right_count += 1

        if gold_Arg2_indices == pred_Arg2_indices:
            Arg2_right_count += 1

        if gold_Arg1_indices == pred_Arg1_indices and gold_Arg2_indices == pred_Arg2_indices:
            Arg1_and_Arg2_right_count += 1

    S = float(len(relation_dict))
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))

    return Arg1_and_Arg2_right_count / S * 100


#[1,2,4,5,6,7]
def merge_NT_Arg(Arg_list, parse_dict, DocID, sent_index):
    punctuation = """!"#&'*+,-..../:;<=>?@[\]^_`|~""" + "``" + "''"
    if len(Arg_list) <= 1:
        return Arg_list
    temp = []
    #扫描丢失的部分，是否是标点符号，是则补上
    for i, item in enumerate(Arg_list):
        if i <= len(Arg_list) - 2:
            temp.append(item)
            next_item = Arg_list[i + 1]
            if next_item - item > 1:
                flag = 1
                for j in range(item + 1, next_item):
                    if parse_dict[DocID]["sentences"][sent_index]["words"][j][0] not in punctuation:
                        flag = 0
                        break
                if flag == 1:#都是标点，补齐
                    temp += list(range(item + 1, next_item))
    temp.append(Arg_list[-1])

    #两侧的逗号要删除
    Arg = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in temp]
    #去两边的标点
    Arg = util.list_strip_punctuation(Arg)

    Arg = [item[0] for item in Arg]

    return Arg





if __name__ == "__main__":
    # do_my_evaluation()
    print(get_Both_ACC())