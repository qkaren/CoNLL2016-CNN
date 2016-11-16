#coding:utf-8
import config, util
from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
from pdtb_parse import PDTB_PARSE

def get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    binary_alphabet = Alphabet()
    binary_alphabet.add('yes')
    binary_alphabet.add('no')
    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, binary_alphabet)
    return cm

def do_my_evaluation():
    dev_feat_file = open(config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.IMPLICIT_ARG1_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict
    implicit_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_implicit_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_raw_implicit_relations = {}
    for relation in dev_pdtb_parse.pdtb.non_explicit_relations:
        if relation["Type"] == "Implicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                relation_ID = relation["ID"]
                gold_implicit_relations[(relation_ID, "Arg1")] = [item[4] for item in relation["Arg1"]["TokenList"]]
                gold_implicit_relations[(relation_ID, "Arg2")] = [item[4] for item in relation["Arg2"]["TokenList"]]



                DocID = relation["DocID"]
                sent1_index = Arg1_sent_indices[0]
                sent2_index = Arg2_sent_indices[0]
                curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])
                curr_length_2 = len(parse_dict[DocID]["sentences"][sent2_index]["words"])

                Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]
                Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length_2)]

                line = "-" * 100 + "\n"
                gold_raw_implicit_relations[(relation_ID, "Arg1")] = line + " ".join([str(index)+":"+word for index, word in Arg1])+"\n" + " ".join([word for index, word in Arg1])
                gold_raw_implicit_relations[(relation_ID, "Arg2")] = line + " ".join([str(index)+":"+word for index, word in Arg2])+"\n" + " ".join([word for index, word in Arg2])
                #去两边的标点
                Arg1 = util.list_strip_punctuation(Arg1)
                Arg2 = util.list_strip_punctuation(Arg2)

                implicit_relations[(relation_ID, "Arg1")] = Arg1
                implicit_relations[(relation_ID, "Arg2")] = Arg2

    feature_list = [line.strip() for line in dev_feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    #对每一个relation的arg1,arg2 ,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0
    Arg1_and_Arg2_right= {}


    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_implicit_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            if Arg == "Arg1":
                Arg1_right_count += 1
                if relation_ID in Arg1_and_Arg2_right:
                    Arg1_and_Arg2_right_count += 1
                Arg1_and_Arg2_right[relation_ID] = 0
            elif Arg == "Arg2":
                Arg2_right_count += 1
                if relation_ID in Arg1_and_Arg2_right:
                    Arg1_and_Arg2_right_count += 1
                Arg1_and_Arg2_right[relation_ID] = 0

        else:
            print(gold_raw_implicit_relations[(relation_ID, Arg)])
            print(pred_arg_list)
            print(gold_arg_list)



    S = float(len(relation_dict)/2)
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))


def do_my_evaluation_explicit():
    dev_feat_file = open(config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.IMPLICIT_ARG1_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict
    implicit_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_implicit_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_raw_implicit_relations = {}
    for relation in dev_pdtb_parse.pdtb.explicit_relations:
        if relation["Type"] == "Explicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1 and \
                Arg1_sent_indices[0] == Arg2_sent_indices[0] - 1:
                relation_ID = relation["ID"]
                gold_implicit_relations[(relation_ID, "Arg1")] = [item[4] for item in relation["Arg1"]["TokenList"]]
                gold_implicit_relations[(relation_ID, "Arg2")] = [item[4] for item in relation["Arg2"]["TokenList"]]



                DocID = relation["DocID"]
                sent1_index = Arg1_sent_indices[0]
                sent2_index = Arg2_sent_indices[0]
                curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])
                curr_length_2 = len(parse_dict[DocID]["sentences"][sent2_index]["words"])

                Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]
                Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length_2)]

                line = "-" * 100 + "\n"
                gold_raw_implicit_relations[(relation_ID, "Arg1")] = line + " ".join([str(index)+":"+word for index, word in Arg1])+"\n" + " ".join([word for index, word in Arg1])
                gold_raw_implicit_relations[(relation_ID, "Arg2")] = line + " ".join([str(index)+":"+word for index, word in Arg2])+"\n" + " ".join([word for index, word in Arg2])
                #去两边的标点
                Arg1 = util.list_strip_punctuation(Arg1)
                Arg2 = util.list_strip_punctuation(Arg2)

                implicit_relations[(relation_ID, "Arg1")] = Arg1
                implicit_relations[(relation_ID, "Arg2")] = Arg2

    feature_list = [line.strip() for line in dev_feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    #对每一个relation的arg1,arg2 ,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0
    Arg2_right_count = 0
    Arg1_and_Arg2_right_count = 0
    Arg1_and_Arg2_right= {}


    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_implicit_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            if Arg == "Arg1":
                Arg1_right_count += 1
                if relation_ID in Arg1_and_Arg2_right:
                    Arg1_and_Arg2_right_count += 1
                Arg1_and_Arg2_right[relation_ID] = 0
            elif Arg == "Arg2":
                Arg2_right_count += 1
                if relation_ID in Arg1_and_Arg2_right:
                    Arg1_and_Arg2_right_count += 1
                Arg1_and_Arg2_right[relation_ID] = 0

        else:
            if Arg == "Arg1":
                print(gold_raw_implicit_relations[(relation_ID, Arg)])
                print(pred_arg_list)
                print(gold_arg_list)



    S = float(len(relation_dict)/2)
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))
    print("Arg2: %.2f%% ." % (Arg2_right_count/S*100))
    print("Arg1&Arg2: %.2f%% ." % (Arg1_and_Arg2_right_count/S*100))

def get_Arg1_Acc(dev_feat_path, dev_output_path):
    # dev_feat_file = open(config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH)
    # predicted_list = get_mallet_predicted_list(config.IMPLICIT_ARG1_DEV_OUTPUT_PATH)

    dev_feat_file = open(dev_feat_path)
    predicted_list = get_mallet_predicted_list(dev_output_path)


    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict
    implicit_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_implicit_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_raw_implicit_relations = {}
    for relation in dev_pdtb_parse.pdtb.non_explicit_relations:
        if relation["Type"] == "Implicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                relation_ID = relation["ID"]
                gold_implicit_relations[(relation_ID, "Arg1")] = [item[4] for item in relation["Arg1"]["TokenList"]]


                DocID = relation["DocID"]
                sent1_index = Arg1_sent_indices[0]
                curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

                Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

                line = "-" * 100 + "\n"
                gold_raw_implicit_relations[(relation_ID, "Arg1")] = line + " ".join([str(index)+":"+word for index, word in Arg1])+"\n" + " ".join([word for index, word in Arg1])
                #去两边的标点
                Arg1 = util.list_strip_punctuation(Arg1)

                implicit_relations[(relation_ID, "Arg1")] = Arg1

    feature_list = [line.strip() for line in dev_feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    #对每一个relation的arg1,删除为attri的部分
    for (relation_ID, Arg) in  relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0


    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_implicit_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            if Arg == "Arg1":
                Arg1_right_count += 1



    S = float(len(relation_dict))

    return (Arg1_right_count/S*100)


def get_Arg1_right_ids(dev_feat_path, dev_output_path):
    # dev_feat_file = open(config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH)
    # predicted_list = get_mallet_predicted_list(config.IMPLICIT_ARG1_DEV_OUTPUT_PATH)

    right_ids = []

    dev_feat_file = open(dev_feat_path)
    predicted_list = get_mallet_predicted_list(dev_output_path)


    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict
    implicit_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_implicit_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_raw_implicit_relations = {}
    for relation in dev_pdtb_parse.pdtb.non_explicit_relations:
        if relation["Type"] == "Implicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                relation_ID = relation["ID"]
                gold_implicit_relations[(relation_ID, "Arg1")] = [item[4] for item in relation["Arg1"]["TokenList"]]


                DocID = relation["DocID"]
                sent1_index = Arg1_sent_indices[0]
                curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

                Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

                line = "-" * 100 + "\n"
                gold_raw_implicit_relations[(relation_ID, "Arg1")] = line + " ".join([str(index)+":"+word for index, word in Arg1])+"\n" + " ".join([word for index, word in Arg1])
                #去两边的标点
                Arg1 = util.list_strip_punctuation(Arg1)

                implicit_relations[(relation_ID, "Arg1")] = Arg1

    feature_list = [line.strip() for line in dev_feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    #对每一个relation的arg1,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg1_right_count = 0


    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_implicit_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            if Arg == "Arg1":
                Arg1_right_count += 1
                right_ids.append(relation_ID)



    S = float(len(relation_dict))

    print((Arg1_right_count/S*100))

    return right_ids


def get_Arg2_right_ids(dev_feat_path, dev_result_file_path):
    right_ids = []

    dev_feat_file = open(dev_feat_path)
    predicted_list = get_mallet_predicted_list(dev_result_file_path)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    parse_dict = dev_pdtb_parse.parse_dict
    implicit_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_implicit_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_raw_implicit_relations = {}
    for relation in dev_pdtb_parse.pdtb.non_explicit_relations:
        if relation["Type"] == "Implicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                relation_ID = relation["ID"]
                gold_implicit_relations[(relation_ID, "Arg2")] = [item[4] for item in relation["Arg2"]["TokenList"]]


                DocID = relation["DocID"]
                sent2_index = Arg2_sent_indices[0]
                curr_length_2 = len(parse_dict[DocID]["sentences"][sent2_index]["words"])

                Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length_2)]
                #去两边的标点
                Arg2 = util.list_strip_punctuation(Arg2)

                implicit_relations[(relation_ID, "Arg2")] = Arg2

    feature_list = [line.strip() for line in dev_feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, predicted_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    #对每一个relation的arg1,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1，arg2 进行精确匹配，评估！
    Arg2_right_count = 0


    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_implicit_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            if Arg == "Arg2":
                Arg2_right_count += 1
                right_ids.append(relation_ID)



    S = float(len(relation_dict))

    print((Arg2_right_count/S*100))

    return right_ids



if __name__ == "__main__":
    # dev_feat_file = open()
    # predicted_list = get_mallet_predicted_list()

    Arg1_right_ids = get_Arg1_right_ids(config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH, config.IMPLICIT_ARG1_DEV_OUTPUT_PATH)

    Arg2_right_ids = get_Arg2_right_ids(config.IMPLICIT_ARG2_DEV_FEATURE_OUTPUT_PATH, config.IMPLICIT_ARG2_DEV_OUTPUT_PATH)

    print(len(set(Arg1_right_ids) & set(Arg2_right_ids)) / 521.0)

