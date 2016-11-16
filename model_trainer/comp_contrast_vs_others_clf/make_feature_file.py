#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree  import Syntax_tree
import config

def comp_contrast_make_feature_file_train(pdtb_parse, feature_function_list, to_file):
    print("为 comp_contrast 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
        features = [feature_function(relation, parse_dict) for feature_function in feature_function_list]
        #合并特征
        feature = mergeFeatures(features)
        #特征target
        if len(relation["Sense"]) == 1:
            sense = relation["Sense"][0]#暂时取第一个
            # 二分类
            if sense == "EntRel":
                target = 1
            else:
                target = 0
            #example
            example = Example(target, feature)
            example.comment = "%s" % (relation["ID"])

            example_list.append(example)

    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))

def comp_contrast_make_feature_file(pdtb_parse, feature_function_list, to_file):
    print("为 non_explicit 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
        features = [feature_function(relation, parse_dict) for feature_function in feature_function_list]
        #合并特征
        feature = mergeFeatures(features)
        #特征target
        sense = relation["Sense"][0]#暂时取第一个

        # 二分类
        if sense == "EntRel":
            target = 1
        else:
            target = 0

        #example
        example = Example(target, feature)
        example.comment = "%s" % (relation["ID"])

        example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))

if __name__ == "__main__":
    pass