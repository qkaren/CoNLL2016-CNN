#coding:utf-8
import config
from .feature_functions import *
from pdtb_parse import PDTB_PARSE
import os
from example import Example
from util import mergeFeatures, write_example_list_to_file, write_shuffled_example_list_to_file
from feature import Feature
from model_trainer.mallet_classifier import *
from . import evaluation
from operator import itemgetter

class Feat_examples:
    def __init__(self, name, dimension, target_list, feat_list, comment_list):
        self.name = name
        self.dimension = dimension
        self.target_list = target_list
        self.feat_list = feat_list
        self.comment_list = comment_list


# 特征文件名带有维度值

def implicit_arg2_make_feature_file(pdtb_parse, feature_function_list, to_file):
    print("为 implicit_arg2 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    implicit_relations = []
    for relation in pdtb_parse.pdtb.non_explicit_relations:
        if relation["Type"] == "Implicit":
            # 一个句子长度的Arg1，Arg1
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                implicit_relations.append(relation)

    example_list = []
    dimension = 0

    total = float(len(implicit_relations))
    for curr_index, relation in enumerate(implicit_relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
        for arg_clauses in dict_util.get_arg_clauses_with_label(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                features = [feature_function(arg_clauses, clause_index, parse_dict) for feature_function in feature_function_list]
                #合并特征
                feature = mergeFeatures(features)
                dimension = feature.dimension
                #特征target
                target = arg_clauses.clauses[clause_index][1]#yes/no
                #example
                example = Example(target, feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))

                example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, "%s_%d" % (to_file, dimension))
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("attri_non_conns 特征已经写入文件：%s ." % ("%s_%d" % (to_file, dimension)))



def generate_feat_file(feature_function_list):

    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    cwd = os.getcwd()

    for feature_function in feature_function_list:
        train_feature_path = cwd + "/feat_combination/train/%s" % (feature_function.__name__)
        dev_feature_path = cwd + "/feat_combination/dev/%s" % (feature_function.__name__)

        print("make train %s feature file ..." % (feature_function.__name__))
        implicit_arg2_make_feature_file(train_pdtb_parse, [feature_function], train_feature_path)

        print("make dev %s feature file ..." % (feature_function.__name__))
        implicit_arg2_make_feature_file(dev_pdtb_parse, [feature_function], dev_feature_path)

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
        cm =evaluation.get_evaluation(dev_result_file_path)
        cm.print_out()
        Arg1_Acc = evaluation.get_Arg2_Acc(dev_feat_path, dev_result_file_path)
        print("Arg1_Acc: %.2f" % Arg1_Acc)
        return Arg1_Acc

if __name__ == "__main__":

    feature_function_list = [
        lowercase_verbs,
        lemma_verbs,
        curr_first,
        curr_last,
        prev_last,
        next_first,
        prev_last_curr_first,
        curr_last_next_first,
        position,
        production_rule,
        is_curr_NNP_prev_PRP_or_NNP,
        prev_curr_production_rule,
        prev_curr_CP_production_rule,
        curr_next_CP_production_rule,
        prev2_pos_lemma_verb,
        curr_first_to_prev_last_path,
        clause_word_num,
        is_NNP_WP,

    ]

    generate_feat_file(feature_function_list)
    # [(feat_name, [feat, feat, ])....]
    train_feat_examples_list, dev_feat_examples_list = load_feat_examples()

    dict_train_feat_examples = get_dict_feat_examples(train_feat_examples_list)
    dict_dev_feat_examples = get_dict_feat_examples(dev_feat_examples_list)


    assert list(dict_train_feat_examples.keys()) == list(dict_dev_feat_examples.keys())

    cwd = os.getcwd()
    train_feat_file = cwd + "/feat_combination/train_feature.txt"
    dev_feat_file = cwd + "/feat_combination/dev_feature.txt"
    model_path = cwd + "/feat_combination/train.model"
    dev_result_file = cwd + "/feat_combination/dev_result.txt"

    # 所有的feats, ['A', "B]
    all_feats = list(dict_train_feat_examples.keys())

    best_feats = []
    curr_best_score = -1
    curr_best_features = ""

    dict_feat_functions_to_score = {}

    while len(best_feats) != len(all_feats):
        T = list(set(all_feats) - set(best_feats))
        score = [0] * len(T)
        for index, feat_name in enumerate(T):

            train_feat_names = best_feats + [feat_name]
            dev_feat_names = best_feats + [feat_name]

            train_feat_example = get_feat_examples_by_feat_name_list(dict_train_feat_examples, train_feat_names)
            dev_feat_example = get_feat_examples_by_feat_name_list(dict_dev_feat_examples, dev_feat_names)

            print("make training feature: %s" % " ".join(train_feat_names))
            make_feature_file_by_feat_examples(train_feat_example, train_feat_file)

            print("make dev feature: %s" % " ".join(dev_feat_names))
            make_feature_file_by_feat_examples(dev_feat_example, dev_feat_file)

            ''' classifier '''
            classifier = Mallet_classifier(NaiveBayes())

            #训练
            classifier.train_model(train_feat_file, model_path)
            #测试
            classifier.test_model(dev_feat_file, dev_result_file, model_path)
            #结果
            Arg1_Acc = get_evaluation(dev_feat_file, dev_result_file)
            score[index] = Arg1_Acc

            if Arg1_Acc > curr_best_score:
                curr_best_score = Arg1_Acc
                curr_best_features = " ".join(train_feat_names)

            print("##" * 45)
            print("Current Best : %.2f" % (curr_best_score))
            print("Current Best Features: %s" % curr_best_features)
            print("##" * 45)

            # 加入字典
            feat_func_name = " ".join(train_feat_names)
            dict_feat_functions_to_score[feat_func_name] = Arg1_Acc


        # 将最好的放入 best_feature_list
        best_index = score.index(max(score))
        best_feats.append(T[best_index])

    # 全部加入的
    train_feat_names = all_feats
    dev_feat_names = all_feats

    train_feat_example = get_feat_examples_by_feat_name_list(dict_train_feat_examples, train_feat_names)
    dev_feat_example = get_feat_examples_by_feat_name_list(dict_dev_feat_examples, dev_feat_names)

    print("make training feature: %s" % " ".join(train_feat_names))
    make_feature_file_by_feat_examples(train_feat_example, train_feat_file)

    print("make dev feature: %s" % " ".join(dev_feat_names))
    make_feature_file_by_feat_examples(dev_feat_example, dev_feat_file)

    ''' classifier '''
    classifier = Mallet_classifier(NaiveBayes())

    #训练
    classifier.train_model(train_feat_file, model_path)
    #测试
    classifier.test_model(dev_feat_file, dev_result_file, model_path)
    #结果
    Arg1_Acc = get_evaluation(dev_feat_file, dev_result_file)

    if Arg1_Acc > curr_best_score:
        curr_best_score = Arg1_Acc
        curr_best_features = " ".join(train_feat_names)

    print("##" * 45)
    print("Current Best : %.2f" % (curr_best_score ))
    print("Current Best Features: %s" % curr_best_features)
    print("##" * 45)

    # 加入字典
    feat_func_name = " ".join(train_feat_names)
    dict_feat_functions_to_score[feat_func_name] = Arg1_Acc

    #将各种特征的组合及对应的score写入文件, 按sore降排
    fout = open("feat_combination/result.txt", "w")
    for func_names, score in sorted(iter(dict_feat_functions_to_score.items()), key=itemgetter(1), reverse=True):
        fout.write("%s : %.2f\n" % (func_names, score ))
    fout.close()
