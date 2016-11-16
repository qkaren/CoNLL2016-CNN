#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree  import Syntax_tree
import NT_dict_util as dict_util

def NT_make_feature_file(pdtb_parse, feature_function_list, to_file):

    print("为 NT 抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    parse_dict = pdtb_parse.parse_dict

    one_SS_conns_not_parallel = pdtb_parse.pdtb.one_SS_conns_not_parallel



    example_list = []
    total = float(len(one_SS_conns_not_parallel))
    for curr_index, connective in enumerate(one_SS_conns_not_parallel):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

        constituents = dict_util.get_constituents_with_label(parse_dict, connective)
        constituents = sorted(constituents, key=lambda constituent: constituent.indices[0])   # sort by age
        #为每一个constituent抽取特征
        for i, constituent in enumerate(constituents):
            features = [feature_function(parse_dict, constituent, i, constituents) for feature_function in feature_function_list]
            #合并特征
            feature = mergeFeatures(features)
            #特征target
            target = constituent.label
            #example
            example = Example(target, feature)
            #加node标示
            example.comment = "%s|%s" % (connective.relation_ID, " ".join([str(t) for t in constituent.get_indices()]))
            example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("连接词特征已经写入文件：%s ." % (to_file))