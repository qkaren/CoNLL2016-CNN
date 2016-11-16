#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree  import Syntax_tree
import config

def non_explicit_make_feature_file_train(pdtb_parse, feature_function_list, to_file):
    print("为 non_explicit 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

        features = []
        for feature_function in feature_function_list:
            if "context" in feature_function.__name__:
                feature = feature_function(relation, parse_dict, pdtb_parse.pdtb.implicit_context_dict)
            else:
                feature = feature_function(relation, parse_dict)
            features.append(feature)

        #合并特征
        feature = mergeFeatures(features)
        #特征target
        if len(relation["Sense"]) == 1:
            sense = relation["Sense"][0]#暂时取第一个
            target = config.Sense_To_Label[sense]
            #example
            example = Example(target, feature)
            example.comment = "%s" % (relation["ID"])

            example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))

def non_explicit_make_feature_file(pdtb_parse, feature_function_list, to_file):
    print("为 non_explicit 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

        features = []
        for feature_function in feature_function_list:
            if "context" in feature_function.__name__:
                feature = feature_function(relation, parse_dict, pdtb_parse.pdtb.implicit_context_dict)
            else:
                feature = feature_function(relation, parse_dict)
            features.append(feature)

        #合并特征
        feature = mergeFeatures(features)
        #特征target
        sense = relation["Sense"][0]#暂时取第一个
        target = config.Sense_To_Label[sense]
        #example
        example = Example(target, feature)
        example.comment = "%s" % (relation["ID"])

        example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))

if __name__ == "__main__":
    from pdtb_parse import PDTB_PARSE
    from .feature_functions import *

    feature_function_list = [
        # word_pairs,
        production_rules, dependency_rules,
        firstlast_first3,
        polarity,
        modality,
        verbs,
        brown_cluster_pair,
        Inquirer,
        # main_verb_pair
        # money_date_percent,
        # Arg_word2vec
        # cp_production_rules
        # word2vec_cluster_pair,
    ]

    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # brown cluster pair
    non_explicit_make_feature_file_train(train_pdtb_parse, [brown_cluster_pair], config.FEATURE_SELECTION_BROWN_CLUSTER)

    # production rule
    # non_explicit_make_feature_file_train(train_pdtb_parse, [production_rules], config.FEATURE_SELECTION_PRODUCTION_RULES)
    pass