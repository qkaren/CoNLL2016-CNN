#coding:utf-8
import config, util
from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
from pdtb_parse import PDTB_PARSE
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper

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
    dev_feat_file = open(config.PS_ARG1_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.PS_ARG1_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    # dev_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    print(len(dev_pdtb_parse.pdtb.IPS_relations))

    parse_dict = dev_pdtb_parse.parse_dict
    IPS_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_IPS_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_DocId_sent_index = {}
    gold_conn_name_indices = {}
    for relation in dev_pdtb_parse.pdtb.IPS_relations:
        relation_ID = relation["ID"]
        gold_arg_list = [item[4] for item in relation["Arg1"]["TokenList"]]
        gold_IPS_relations[(relation_ID, "Arg1")] = gold_arg_list


        DocID = relation["DocID"]
        # 一个句子长度的Arg1，Arg1
        Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
        sent1_index = Arg1_sent_indices[0]

        gold_DocId_sent_index[(relation_ID, "Arg1")] = (DocID, sent1_index)

        curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

        #去根据连接词划分
        conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]
        #conn head
        raw_connective = relation["Connective"]["RawText"]
        chm = ConnHeadMapper()
        conn_head, indices = chm.map_raw_connective(raw_connective)
        conn_head_indices = [conn_indices[index] for index in indices]


        #获取连接词到名称
        conn_name = " ".join([parse_dict[DocID]["sentences"][sent1_index + 1]["words"][word_token][0] \
                  for word_token in conn_head_indices ])

        gold_conn_name_indices[(relation_ID, "Arg1")] = (conn_head_indices, conn_name)


        #去两边的标点
        Arg1 = util.list_strip_punctuation(Arg1)

        #只去处标点的Arg1 － gold Arg1
        Arg1_token_list = [item[0] for item in Arg1]

        left_token_list = set(Arg1_token_list) - set(gold_arg_list)
        left_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(left_token_list)])
        gold_arg_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(gold_arg_list)])
        Arg1_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(Arg1_token_list)])

        # if left_words != "":
        #     print "**" * 45
        #     print left_words
        # print "**" * 45
        # print Arg1_words
        # print gold_arg_words


        IPS_relations[(relation_ID, "Arg1")] = Arg1

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

    #对每一个relation的arg1,arg1 ,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = IPS_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
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

                IPS_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in IPS_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1 进行精确匹配，评估！
    Arg1_right_count = 0

    #对分错的连接词进行统计
    err_conn_count = {}

    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_IPS_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            Arg1_right_count += 1
        else:
            DocID, sent_index = gold_DocId_sent_index[(relation_ID, "Arg1")]
            curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            next_length = len(parse_dict[DocID]["sentences"][sent_index + 1]["words"])
            Arg1_text = " ".join([str(index)+":"+parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg1_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg2_raw = " ".join([parse_dict[DocID]["sentences"][sent_index + 1]["words"][index][0] for index in range(next_length)])

            conn_indices, conn_name = gold_conn_name_indices[(relation_ID, "Arg1")]

            if conn_name not in err_conn_count:
                err_conn_count[conn_name] = 0
            err_conn_count[conn_name] += 1

            print("--" * 45)
            print(Arg1_text)
            print("[%s][%s]" % (Arg1_raw, Arg2_raw))
            print(pred_arg_list)
            print(gold_arg_list)
            print("%s:%s" % (conn_name, " ".join([str(i) for i in conn_indices])))

    print("--" * 45)
    print("\n".join("%s:%d" % (word,count) for word, count in sorted(iter(err_conn_count.items()), key=operator.itemgetter(1), reverse = True)))

    S = float(len(relation_dict))
    print(S)
    print("Arg1: %.2f%% ." % (Arg1_right_count/S*100))


def get_Arg1_Acc():
    dev_feat_file = open(config.PS_ARG1_DEV_FEATURE_OUTPUT_PATH)
    predicted_list = get_mallet_predicted_list(config.PS_ARG1_DEV_OUTPUT_PATH)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    # dev_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    print(len(dev_pdtb_parse.pdtb.IPS_relations))

    parse_dict = dev_pdtb_parse.parse_dict
    IPS_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_IPS_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_DocId_sent_index = {}
    gold_conn_name_indices = {}
    for relation in dev_pdtb_parse.pdtb.IPS_relations:
        relation_ID = relation["ID"]
        gold_arg_list = [item[4] for item in relation["Arg1"]["TokenList"]]
        gold_IPS_relations[(relation_ID, "Arg1")] = gold_arg_list


        DocID = relation["DocID"]
        # 一个句子长度的Arg1，Arg1
        Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
        sent1_index = Arg1_sent_indices[0]

        gold_DocId_sent_index[(relation_ID, "Arg1")] = (DocID, sent1_index)

        curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

        #去根据连接词划分
        conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]
        #conn head
        raw_connective = relation["Connective"]["RawText"]
        chm = ConnHeadMapper()
        conn_head, indices = chm.map_raw_connective(raw_connective)
        conn_head_indices = [conn_indices[index] for index in indices]


        #获取连接词到名称
        conn_name = " ".join([parse_dict[DocID]["sentences"][sent1_index + 1]["words"][word_token][0] \
                  for word_token in conn_head_indices ])

        gold_conn_name_indices[(relation_ID, "Arg1")] = (conn_head_indices, conn_name)


        #去两边的标点
        Arg1 = util.list_strip_punctuation(Arg1)

        #只去处标点的Arg1 － gold Arg1
        Arg1_token_list = [item[0] for item in Arg1]

        left_token_list = set(Arg1_token_list) - set(gold_arg_list)
        left_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(left_token_list)])
        gold_arg_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(gold_arg_list)])
        Arg1_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(Arg1_token_list)])

        # if left_words != "":
        #     print "**" * 45
        #     print left_words
        # print Arg1_words
        # print gold_arg_words


        IPS_relations[(relation_ID, "Arg1")] = Arg1

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

    #对每一个relation的arg1,arg1 ,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = IPS_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
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

                IPS_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in IPS_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1 进行精确匹配，评估！
    Arg1_right_count = 0

    #对分错的连接词进行统计
    err_conn_count = {}

    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_IPS_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            Arg1_right_count += 1
        else:
            DocID, sent_index = gold_DocId_sent_index[(relation_ID, "Arg1")]
            curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            next_length = len(parse_dict[DocID]["sentences"][sent_index + 1]["words"])
            Arg1_text = " ".join([str(index)+":"+parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg1_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg2_raw = " ".join([parse_dict[DocID]["sentences"][sent_index + 1]["words"][index][0] for index in range(next_length)])

            conn_indices, conn_name = gold_conn_name_indices[(relation_ID, "Arg1")]

            if conn_name not in err_conn_count:
                err_conn_count[conn_name] = 0
            err_conn_count[conn_name] += 1
            #
            # print "--" * 45
            # print Arg1_text
            # print "[%s][%s]" % (Arg1_raw, Arg2_raw)
            # print pred_arg_list
            # print gold_arg_list
            # print "%s:%s" % (conn_name, " ".join([str(i) for i in conn_indices]))

    # print "--" * 45
    # print "\n".join("%s:%d" % (word,count) for word, count in sorted(err_conn_count.iteritems(), key=operator.itemgetter(1), reverse = True))

    S = float(len(relation_dict))
    return Arg1_right_count / S * 100

def get_Arg1_Acc_feat_combine(dev_feat_output, dev_output):
    dev_feat_file = open(dev_feat_output)
    predicted_list = get_mallet_predicted_list(dev_output)

    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_ORIGIN_DEV_PATH, config.DEV)
    # dev_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    print(len(dev_pdtb_parse.pdtb.IPS_relations))

    parse_dict = dev_pdtb_parse.parse_dict
    IPS_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    gold_IPS_relations = {} # dict[(relation_ID,Arg)] = [1,2,3]
    gold_DocId_sent_index = {}
    gold_conn_name_indices = {}
    for relation in dev_pdtb_parse.pdtb.IPS_relations:
        relation_ID = relation["ID"]
        gold_arg_list = [item[4] for item in relation["Arg1"]["TokenList"]]
        gold_IPS_relations[(relation_ID, "Arg1")] = gold_arg_list


        DocID = relation["DocID"]
        # 一个句子长度的Arg1，Arg1
        Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
        sent1_index = Arg1_sent_indices[0]

        gold_DocId_sent_index[(relation_ID, "Arg1")] = (DocID, sent1_index)

        curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

        #去根据连接词划分
        conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]
        #conn head
        raw_connective = relation["Connective"]["RawText"]
        chm = ConnHeadMapper()
        conn_head, indices = chm.map_raw_connective(raw_connective)
        conn_head_indices = [conn_indices[index] for index in indices]


        #获取连接词到名称
        conn_name = " ".join([parse_dict[DocID]["sentences"][sent1_index + 1]["words"][word_token][0] \
                  for word_token in conn_head_indices ])

        gold_conn_name_indices[(relation_ID, "Arg1")] = (conn_head_indices, conn_name)


        #去两边的标点
        Arg1 = util.list_strip_punctuation(Arg1)

        #只去处标点的Arg1 － gold Arg1
        Arg1_token_list = [item[0] for item in Arg1]

        left_token_list = set(Arg1_token_list) - set(gold_arg_list)
        left_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(left_token_list)])
        gold_arg_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(gold_arg_list)])
        Arg1_words = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(Arg1_token_list)])

        # if left_words != "":
        #     print "**" * 45
        #     print left_words
        # print Arg1_words
        # print gold_arg_words


        IPS_relations[(relation_ID, "Arg1")] = Arg1

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

    #对每一个relation的arg1,arg1 ,删除为attri的部分
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes":
                implicit_Arg = IPS_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
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

                IPS_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in IPS_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    #对同一个句子的arg1 进行精确匹配，评估！
    Arg1_right_count = 0

    #对分错的连接词进行统计
    err_conn_count = {}

    for relation_ID, Arg in relation_dict.keys():
        gold_arg_list = gold_IPS_relations[relation_ID, Arg]
        pred_arg_list = relation_dict[(relation_ID, Arg)]

        if gold_arg_list == pred_arg_list:
            Arg1_right_count += 1
        else:
            DocID, sent_index = gold_DocId_sent_index[(relation_ID, "Arg1")]
            curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            next_length = len(parse_dict[DocID]["sentences"][sent_index + 1]["words"])
            Arg1_text = " ".join([str(index)+":"+parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg1_raw = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(curr_length)])
            Arg2_raw = " ".join([parse_dict[DocID]["sentences"][sent_index + 1]["words"][index][0] for index in range(next_length)])

            conn_indices, conn_name = gold_conn_name_indices[(relation_ID, "Arg1")]

            if conn_name not in err_conn_count:
                err_conn_count[conn_name] = 0
            err_conn_count[conn_name] += 1
            #
            print ("--" * 45)
            print (Arg1_text)
            print ("[%s][%s]" % (Arg1_raw, Arg2_raw))
            print (pred_arg_list)
            print (gold_arg_list)
            print ("%s:%s" % (conn_name, " ".join([str(i) for i in conn_indices])))

    print ("--" * 45)
    print ("\n".join("%s:%d" % (word,count) for word, count in sorted(err_conn_count.iteritems(), key=operator.itemgetter(1), reverse = True)))

    S = float(len(relation_dict))
    return Arg1_right_count / S * 100

if __name__ == "__main__":
    # do_my_evaluation()

    print(get_Arg1_Acc())


