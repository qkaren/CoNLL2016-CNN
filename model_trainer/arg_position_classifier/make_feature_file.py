#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
import config


def arg_position_make_feature_file(pdtb_parse, feature_function_list, to_file):

    print("为 argument position 抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    parse_dict = pdtb_parse.parse_dict

    SS_conns_dict = pdtb_parse.pdtb.SS_conns_dict
    PS_conns_dict = pdtb_parse.pdtb.PS_conns_dict

    total = float(len(SS_conns_dict) + len(PS_conns_dict))
    t = 0

    example_list = []
    for DocID, sent_index in list(SS_conns_dict.keys()):
        t += 1
        print("Process: %.2f%%\r" % (t/total * 100), end=' ')
        for conn_indices in SS_conns_dict[(DocID, sent_index)]:
            #根据 DocID, sent_index, conn_indices
            features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]
            #合并特征
            feature = mergeFeatures(features)
            #特征target
            target = config.ARG_POSITION_TO_LABEL["SS"]#ss
            #example
            example = Example(target, feature)
            example_list.append(example)

    for DocID, sent_index in list(PS_conns_dict.keys()):
        t += 1
        print("Process: %.2f%%\r" % (t/total * 100), end=' ')
        for conn_indices in PS_conns_dict[(DocID, sent_index)]:
            #根据 DocID, sent_index, conn_indices
            features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]
            #合并特征
            feature = mergeFeatures(features)
            #特征target
            target = config.ARG_POSITION_TO_LABEL["PS"]#ps
            #example
            example = Example(target, feature)
            example_list.append(example)


    #将example_list写入文件
    # write_example_list_to_file(example_list, to_file)
    write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("连接词特征已经写入文件：%s ." % (to_file))