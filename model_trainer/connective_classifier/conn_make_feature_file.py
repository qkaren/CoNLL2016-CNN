#coding:utf-8
# from .feature_functions import *
from pdtb_parse import PDTB_PARSE
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from example import Example
import config
# from tools.multi_thread import run_multi_thread


def make_feature_file(pdtb_parse, feature_function_list, to_file):

    print("为连接词抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    disc_conns_dict = pdtb_parse.disc_conns_dict
    non_disc_conns_dict = pdtb_parse.non_disc_conns_dict
    parse_dict = pdtb_parse.parse_dict
    #
    total = float(len(disc_conns_dict) + len(non_disc_conns_dict))
    t = 0

    example_list = []
    #语篇连接词
    for DocID, sent_index in list(disc_conns_dict.keys()):
        t += 1
        print("Process: %.2f%%\r" % ( t/total * 100), end=' ')

        for conn_indices in disc_conns_dict[(DocID, sent_index)]:
            #根据 DocID, sent_index, conn_indices
            features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]

            # features = run_multi_thread(feature_function_list, parse_dict, DocID, sent_index, conn_indices)

            #合并特征
            feature = mergeFeatures(features)
            #特征target
            target = 1
            #example
            example = Example(target, feature)
            # comment
            conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])
            example.comment = "%s|%s|%s|%s" % (conn_name, DocID, str(sent_index), " ".join([str(i) for i in conn_indices]))
            example_list.append(example)
    #非语篇连接词
    for DocID, sent_index in list(non_disc_conns_dict.keys()):
        t += 1
        print("Process: %.2f%%\r" % (t/total * 100), end=' ')

        for conn_indices in non_disc_conns_dict[(DocID, sent_index)]:
            #根据 DocID, sent_index, conn_indices
            features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]
            # features = run_multi_thread(feature_function_list, parse_dict, DocID, sent_index, conn_indices)
            #合并特征
            feature = mergeFeatures(features)
            #特征target
            target = 0
            #example
            example = Example(target, feature)
            # comment
            conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])
            example.comment = "%s|%s|%s|%s" % (conn_name, DocID, str(sent_index), " ".join([str(i) for i in conn_indices]))
            example_list.append(example)

    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("连接词特征已经写入文件：%s ." % (to_file))


def make_train_feature_file(feature_function_list):
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    to_file = config.CONNECTIVE_TRAIN_FEATURE_OUTPUT_PATH

    make_feature_file(pdtb_parse, feature_function_list, to_file)

def make_dev_feature_file(feature_function_list):
    pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    to_file = config.CONNECTIVE_DEV_FEATURE_OUTPUT_PATH

    make_feature_file(pdtb_parse, feature_function_list, to_file)

if __name__ == "__main__":
    pass