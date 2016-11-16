#coding:utf-8
import config
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree  import Syntax_tree
import exp_dict_util as dict_util

def Explicit_make_feature_file_train(pdtb_parse, feature_function_list, to_file):

    print("为 Explicit 抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    parse_dict = pdtb_parse.parse_dict

    conns_list = pdtb_parse.pdtb.conns_list

    example_list = []

    total = float(len(conns_list))
    for curr_index, connective in enumerate(conns_list):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')


        features = [feature_function(parse_dict, connective) for feature_function in feature_function_list]
        #合并特征
        feature = mergeFeatures(features)

        # for sense in connective.sense:
        #     example = Example(config.Sense_To_Label[sense], feature)
        #     example.comment = "%s" % (connective.relation_ID)
        #     example_list.append(example)

        if len(connective.sense) == 1:
            sense = connective.sense[0]
            example = Example(config.Sense_To_Label[sense], feature)
            example.comment = "%s" % (connective.relation_ID)

            example_list.append(example)

    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("连接词特征已经写入文件：%s ." % (to_file))

def Explicit_make_feature_file(pdtb_parse, feature_function_list, to_file):

    print("为 Explicit 抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    parse_dict = pdtb_parse.parse_dict

    conns_list = pdtb_parse.pdtb.conns_list

    example_list = []

    total = float(len(conns_list))
    for curr_index, connective in enumerate(conns_list):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')


        features = [feature_function(parse_dict, connective) for feature_function in feature_function_list]
        #合并特征
        feature = mergeFeatures(features)

        #example

        #加node标示
        # example.comment = "%s|%s" % (connective.relation_ID, " ".join([str(t) for t in constituent.get_indices()]))
        # for sense in connective.sense:
        sense = connective.sense[0]
        example = Example(config.Sense_To_Label[sense], feature)
        example.comment = "%s" % (connective.relation_ID)

        example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("连接词特征已经写入文件：%s ." % (to_file))