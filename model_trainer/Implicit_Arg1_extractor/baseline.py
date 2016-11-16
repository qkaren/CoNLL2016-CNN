#coding:utf-8
import config
from pdtb import PDTB
from pdtb_parse import PDTB_PARSE
import util
from connective import Connective

# 获取IPS的Arg1，Implicit的一个句子长度的Arg1，Arg2,不使用AltLex，不使用EntRel(没有Attribution)
# [(DocID, sent_index)]
def get_baseline_Arg1(pdtb_parse):

    right_relation_ids = []

    parse_dict = pdtb_parse.parse_dict
    pdtb = pdtb_parse.pdtb

    arg1_right = 0
    count = 0

    for relation in pdtb.non_explicit_relations:
        if relation["Type"] != "EntRel":

            # 一个句子长度的Arg1，
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) != 1 or len(set(Arg2_sent_indices)) != 1:#只考虑句子长度为1
                continue

            count += 1

            DocID = relation["DocID"]
            sent1_index = Arg1_sent_indices[0]

            curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

            Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]

            #去两边的标点
            Arg1 = util.list_strip_punctuation(Arg1)

            Arg1 = [item[0] for item in Arg1]

            Ag1_text = " ".join([str(index)+":"+parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in range(curr_length_1)])
            Arg1_raw = " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in range(curr_length_1)])


            gold_arg1 = sorted([item[4] for item in relation["Arg1"]["TokenList"]])

            if Arg1 != gold_arg1:

                    # if set(Arg1) > set(gold_arg1):
                    #     print "-"*100
                    #     print " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in range(curr_length_1) ])
                    #     left = [parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(list(set(Arg1) - set(gold_arg1))) ]
                    #     print " ".join(left)

                    # if Arg1[-1] - gold_arg1[-1] < 3 and Arg1[-1] - gold_arg1[-1] > -3 and Arg1[-1] != gold_arg1[-1]:
                    #
                    print("-"*100)
                    curr_length = len(parse_dict[DocID]["sentences"][sent1_index]["words"])
                    print([(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length)])
                    print(DocID, sent1_index)
                    print(Arg1_raw)
                    print(Ag1_text)
                    print(Arg1)
                    print(gold_arg1)
                    print(relation["ID"])

            if Arg1 == gold_arg1:
                arg1_right += 1
                right_relation_ids.append(relation["ID"])




    print("-"*100)
    print("implicit(No EntRel) Arg1 : %.2f%% "% ((arg1_right)/float(count)*100))
    print(count)

    return right_relation_ids


def get_baseline_Arg2(pdtb_parse):

    right_relation_ids =[]

    parse_dict = pdtb_parse.parse_dict
    pdtb = pdtb_parse.pdtb

    arg2_right = 0
    count = 0

    for relation in pdtb.non_explicit_relations:
        if relation["Type"] != "EntRel":

            # 一个句子长度的Arg1，
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) != 1 or len(set(Arg2_sent_indices)) != 1:#只考虑句子长度为1
                continue

            count += 1

            DocID = relation["DocID"]
            sent2_index = Arg2_sent_indices[0]

            curr_length_2 = len(parse_dict[DocID]["sentences"][sent2_index]["words"])

            Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length_2)]

            #去两边的标点
            Arg2 = util.list_strip_punctuation(Arg2)

            Arg2 = [item[0] for item in Arg2]

            Ag2_text = " ".join([str(index)+":"+parse_dict[DocID]["sentences"][sent2_index]["words"][index][0] for index in range(curr_length_2)])
            Arg2_raw = " ".join([parse_dict[DocID]["sentences"][sent2_index]["words"][index][0] for index in range(curr_length_2)])


            gold_arg2 = sorted([item[4] for item in relation["Arg2"]["TokenList"]])

            if Arg2 != gold_arg2:

                    # if set(Arg1) > set(gold_arg1):
                    #     print "-"*100
                    #     print " ".join([parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in range(curr_length_1) ])
                    #     left = [parse_dict[DocID]["sentences"][sent1_index]["words"][index][0] for index in sorted(list(set(Arg1) - set(gold_arg1))) ]
                    #     print " ".join(left)

                    # if Arg1[-1] - gold_arg1[-1] < 3 and Arg1[-1] - gold_arg1[-1] > -3 and Arg1[-1] != gold_arg1[-1]:
                    #
                    print("-"*100)
                    curr_length = len(parse_dict[DocID]["sentences"][sent2_index]["words"])
                    print([(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length)])
                    print(DocID, sent2_index)
                    print(Arg2_raw)
                    print(Ag2_text)
                    print(Arg2)
                    print(gold_arg2)
                    print(relation["ID"])

            if Arg2 == gold_arg2:
                arg2_right += 1
                right_relation_ids.append(relation["ID"])




    print("-"*100)
    print("implicit(No EntRel) Arg1 : %.2f%% "% ((arg2_right)/float(count)*100))
    print(count)

    return right_relation_ids





if __name__ == "__main__":
    # pdtb_parse_train =  PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    pdtb_parse_dev =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    # pdtb_train = PDTB(config.PDTB_TRAIN_PATH, config.TRAIN)

    Arg1_right_ids = get_baseline_Arg1(pdtb_parse_dev)
    Arg2_right_ids = get_baseline_Arg2(pdtb_parse_dev)

    print(len(set(Arg1_right_ids) & set(Arg2_right_ids)) / 521.0)