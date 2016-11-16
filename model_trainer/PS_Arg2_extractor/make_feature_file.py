#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree import Syntax_tree
import config
import ps_arg2_dict_util as dict_util

def ps_arg2_make_feature_file(pdtb_parse, feature_function_list, to_file):
    print("为 ps_arg2 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    IPS_relations = pdtb_parse.pdtb.IPS_relations
    parse_dict = pdtb_parse.parse_dict

    example_list = []

    total = float(len(IPS_relations))

    for curr_index, relation in enumerate(IPS_relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
        for arg_clauses in dict_util.get_arg_clauses_with_label(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                features = [feature_function(arg_clauses, clause_index, parse_dict) for feature_function in feature_function_list]
                #合并特征
                feature = mergeFeatures(features)
                #特征target
                target = arg_clauses.clauses[clause_index][1]#yes/no
                #example
                example = Example(target, feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))

                example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("attri_non_conns 特征已经写入文件：%s ." % (to_file))
