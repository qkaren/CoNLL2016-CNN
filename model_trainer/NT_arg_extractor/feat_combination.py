#coding:utf-8
import config
from .feature_functions import *
from pdtb_parse import PDTB_PARSE
import os
from example import Example
from util import mergeFeatures, write_example_list_to_file, write_shuffled_example_list_to_file
from feature import Feature
from model_trainer.mallet_classifier import *
from operator import itemgetter
import numpy as np
from . import evaluation

class Feat_examples:
    def __init__(self, name, dimension, target_list, feat_list, comment_list):
        self.name = name
        self.dimension = dimension
        self.target_list = target_list
        self.feat_list = feat_list
        self.comment_list = comment_list


# 特征文件名带有维度值
def make_feature_file(pdtb_parse, feature_function_list, to_file):

    print("为 NT 抽取特征：%s ." % (" ".join([f.__name__ for f in feature_function_list])))

    parse_dict = pdtb_parse.parse_dict

    one_SS_conns_not_parallel = pdtb_parse.pdtb.one_SS_conns_not_parallel

    example_list = []
    dimension = 0

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
            dimension = feature.dimension
            #特征target
            target = constituent.label
            #example
            example = Example(target, feature)
            #加node标示
            example.comment = "%s|%s" % (connective.relation_ID, " ".join([str(t) for t in constituent.get_indices()]))
            example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, "%s_%d" % (to_file, dimension))
    print("特征已经写入文件：%s ." % ("%s_%d" % (to_file, dimension)))


def generate_feat_file(feature_function_list):

    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    cwd = os.getcwd()

    for feature_function in feature_function_list:
        train_feature_path = cwd + "/feat_combination/train/%s" % (feature_function.__name__)
        dev_feature_path = cwd + "/feat_combination/dev/%s" % (feature_function.__name__)

        print("make train %s feature file ..." % (feature_function.__name__))
        make_feature_file(train_pdtb_parse, [feature_function], train_feature_path)

        print("make dev %s feature file ..." % (feature_function.__name__))
        make_feature_file(dev_pdtb_parse, [feature_function], dev_feature_path)

def load_feat_examples():
    train_feat_names = listdir_no_hidden('feat_combination/train')
    dev_feat_names = listdir_no_hidden('feat_combination/dev')

    train_feat_examples = []
    for feat_name in train_feat_names:
        train_feat_examples.append(get_feat_examples('feat_combination/train', feat_name))

    dev_feat_examples = []
    for feat_name in dev_feat_names:
        dev_feat_examples.append(get_feat_examples('feat_combination/dev', feat_name))

    return train_feat_examples, dev_feat_examples

# (feat_name, target, comment, [feat, feat, ])
def get_feat_examples(path, feat_name):
    file = open("%s/%s" % (path, feat_name))

    dimension = int(feat_name.split("_")[-1])
    feat_name = "_".join(feat_name.split("_")[:-1])

    feat_list = []
    target_list = []
    comment_list = []

    for line in file:
        line = line.strip()
        comment_list.append(line.split("#")[-1].strip())
        line = line.split("#")[0].strip()
        target_list.append(line.split(" ")[0])


        feat_string = " ".join(line.split(" ")[1:])

        feat = Feature(feat_name, dimension, {})
        feat.feat_string = feat_string

        feat_list.append(feat)

    return Feat_examples(feat_name, dimension, target_list, feat_list, comment_list)

# [(feat_name, target, comment, [feat, feat, ])....] -- > (feat_name, target, comment, [feat, feat, ])
def combine_feats(feat_list):
    feat_name = " ".join([item[0] for item in feat_list])
    feats = []

    _feats = [item[3] for item in feat_list]

    for item in zip(*_feats):
        feats.append(util.mergeFeatures(item, feat_name))

    return (feat_name, feat_list)


def get_dict_feat_examples(feat_examples_list):
    # name --> feat_examples
    dict_feat_examples = {}
    for feat_examples in feat_examples_list:
        dict_feat_examples[feat_examples.name] = feat_examples

    return dict_feat_examples

def get_feat_examples_by_feat_name_list(dict_feat_examples, feat_name_list):
    feat_examples_list = []
    for feat_name in feat_name_list:
        feat_examples_list.append(dict_feat_examples[feat_name])

    feat_examples = merge_feat_examples_list(feat_examples_list)

    return feat_examples

def merge_feat_examples_list(feat_examples_list):

    target_list = feat_examples_list[0].target_list
    dimension = sum([feat_examples.dimension for feat_examples in feat_examples_list])
    comment_list = feat_examples_list[0].comment_list

    feat_list = []
    feats_list = [feat_examples.feat_list for feat_examples in feat_examples_list]
    for item in zip(*feats_list):
        feat_list.append(util.mergeFeatures(item))

    return Feat_examples("merged_feat", dimension, target_list, feat_list, comment_list)

def make_feature_file_by_feat_examples(feat_examples, to_file):
    target_list = feat_examples.target_list
    feat_list = feat_examples.feat_list
    comment_list = feat_examples.comment_list

    fout = open(to_file, "w")
    for target, feature, comment in zip(target_list, feat_list, comment_list):
        example = "%s %s # %s" % (target, feature.feat_string, comment)
        fout.write("%s\n" % example)
    fout.close()


def listdir_no_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f




def get_evaluation(dev_feat_path, dev_result_file_path):
        cm = evaluation.get_evaluation(dev_result_file_path)
        cm.print_out()
        print("\n" + "-"*80 + "\n")
        return evaluation.get_Both_ACC_feat_combine(dev_feat_path, dev_result_file_path)

if __name__ == "__main__":

    feature_function_list = [
        # CON_Str,
        # CON_LStr,
        # CON_Cat,
        # CON_iLSib,
        # CON_iRSib,
        # NT_Ctx,
        # CON_NT_Path,
        # CON_NT_Position,
        # CON_NT_Path_iLsib,
        # # mine
        # NT_prev_curr_Path,
        # prev_curr_some_clause,
        # CON_POS,
        #
        # # mine - conn
        # # CParent_to_root_path,
        # CParent_to_root_path_node_names,
        # # conn_connCtx,
        # # conn_parent_categoryCtx,
        # # conn_rightSiblingCtx,
        # # self_category,
        # parent_category,
        # # left_sibling_category,
        # # right_sibling_category,
        #
        # # mine : NT
        # NT_Linked_ctx,
        # NT_parent_linked_ctx,
        # NT_to_root_path,
        # NT_iLSib,
        # NT_iRSib,

        # mine : conn - NT
        NT_conn_level_distance,

        # mine : NT - NT
        NT_prev_curr_level_distance,
        NT_curr_next_level_distance,


    ]

    generate_feat_file(feature_function_list)

    # # [(feat_name, [feat, feat, ])....]
    # train_feat_examples_list, dev_feat_examples_list = load_feat_examples()
    #
    # dict_train_feat_examples = get_dict_feat_examples(train_feat_examples_list)
    # dict_dev_feat_examples = get_dict_feat_examples(dev_feat_examples_list)
    #
    #
    # assert dict_train_feat_examples.keys() == dict_dev_feat_examples.keys()
    #
    # cwd = os.getcwd()
    # train_feat_file = cwd + "/feat_combination/train_feature.txt"
    # dev_feat_file = cwd + "/feat_combination/dev_feature.txt"
    # model_path = cwd + "/feat_combination/train.model"
    # dev_result_file = cwd + "/feat_combination/dev_result.txt"
    #
    # # 所有的feats, ['A', "B]
    # all_feats = dict_train_feat_examples.keys()
    #
    # best_feats = []
    # curr_best_score = -1
    # curr_best_features = ""
    #
    # dict_feat_functions_to_score = {}
    #
    # while len(best_feats) != len(all_feats):
    #     T = list(set(all_feats) - set(best_feats))
    #     score = [0] * len(T)
    #     for index, feat_name in enumerate(T):
    #
    #         train_feat_names = best_feats + [feat_name]
    #         dev_feat_names = best_feats + [feat_name]
    #
    #         train_feat_example = get_feat_examples_by_feat_name_list(dict_train_feat_examples, train_feat_names)
    #         dev_feat_example = get_feat_examples_by_feat_name_list(dict_dev_feat_examples, dev_feat_names)
    #
    #
    #
    #         print "make training feature: %s" % " ".join(train_feat_names)
    #         make_feature_file_by_feat_examples(train_feat_example, train_feat_file)
    #
    #         print "make dev feature: %s" % " ".join(dev_feat_names)
    #         make_feature_file_by_feat_examples(dev_feat_example, dev_feat_file)
    #
    #         ''' classifier '''
    #         classifier = Mallet_classifier(MaxEnt())
    #
    #         #训练
    #         classifier.train_model(train_feat_file, model_path)
    #         #测试
    #         classifier.test_model(dev_feat_file, dev_result_file, model_path)
    #         #结果
    #         s = get_evaluation(dev_feat_file, dev_result_file)
    #         score[index] = s
    #
    #         if s > curr_best_score:
    #             curr_best_score = s
    #             curr_best_features = " ".join(train_feat_names)
    #
    #         print "##" * 45
    #         print "Current Best : %.2f" % curr_best_score
    #         print "Current Best Features: %s" % curr_best_features
    #         print "##" * 45
    #
    #         # 加入字典
    #         feat_func_name = " ".join(train_feat_names)
    #         dict_feat_functions_to_score[feat_func_name] = s
    #
    #
    #     # 将最好的放入 best_feature_list
    #     best_index = score.index(max(score))
    #     best_feats.append(T[best_index])
    #
    # # 全部加入的
    # train_feat_names = all_feats
    # dev_feat_names = all_feats
    #
    # train_feat_example = get_feat_examples_by_feat_name_list(dict_train_feat_examples, train_feat_names)
    # dev_feat_example = get_feat_examples_by_feat_name_list(dict_dev_feat_examples, dev_feat_names)
    #
    #
    #
    # print "make training feature: %s" % " ".join(train_feat_names)
    # make_feature_file_by_feat_examples(train_feat_example, train_feat_file)
    #
    # print "make dev feature: %s" % " ".join(dev_feat_names)
    # make_feature_file_by_feat_examples(dev_feat_example, dev_feat_file)
    #
    # ''' classifier '''
    # classifier = Mallet_classifier(MaxEnt())
    #
    # #训练
    # classifier.train_model(train_feat_file, model_path)
    # #测试
    # classifier.test_model(dev_feat_file, dev_result_file, model_path)
    # #结果
    # s = get_evaluation(dev_feat_file, dev_result_file)
    #
    # if s > curr_best_score:
    #     curr_best_score = s
    #     curr_best_features = " ".join(train_feat_names)
    #
    # print "##" * 45
    # print "Current Best : %.2f" % curr_best_score
    # print "Current Best Features: %s" % curr_best_features
    # print "##" * 45
    #
    # # 加入字典
    # feat_func_name = " ".join(train_feat_names)
    # dict_feat_functions_to_score[feat_func_name] = s
    #
    # #将各种特征的组合及对应的score写入文件, 按sore降排
    # fout = open("feat_combination/result.txt", "w")
    # for func_names, score in sorted(dict_feat_functions_to_score.iteritems(), key=itemgetter(1), reverse=True):
    #     fout.write("%s : %.2f\n" % (func_names, score))
    # fout.close()
