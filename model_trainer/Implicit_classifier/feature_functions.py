#coding:utf-8
from feature import Feature
from util import mergeFeatures
import util
from syntax_tree import Syntax_tree
import non_exp_dict_util as dict_util
from non_explicit_dict import Non_Explicit_dict
import pickle, config, string
import os
import re, operator
from connective import Connectives_dict

def all_features(relation, parse_dict):
    feature_function_list = [
        # word_pairs,
        production_rules, dependency_rules,
        firstlast_first3,
        # polarity,
        modality,
        verbs,
        brown_cluster_pair,
        Inquirer,
        MPQA_polarity,
        # LM_exp_conn_1,
        # LM_exp_conn_3,
        prev_context_conn
    ]

    features = [feature_function(relation, parse_dict) for feature_function in feature_function_list]
    #合并特征
    feature = mergeFeatures(features)
    return feature

def word_pairs(relation, parse_dict):
    ''' load dict '''
    dict_word_pairs = Non_Explicit_dict().dict_word_pairs

    ''' feature '''
    word_pairs = dict_util.get_word_pairs(relation, parse_dict)#["a|b", "b|e"]

    return get_feature_by_feat_list(dict_word_pairs, word_pairs)

def cp_production_rules(relation, parse_dict):
    ''' load dict '''
    dict_cp_production_rules = Non_Explicit_dict().cp_production_rules

    ''' feature '''
    cp_production_rules = dict_util.get_cp_production_rules(relation, parse_dict)#["a|b", "b|e"]

    return get_feature_by_feat_list(dict_cp_production_rules, cp_production_rules)

# def production_rules(relation, parse_dict):
#     '''load dict '''
#     dict_production_rules = Non_Explicit_dict().dict_production_rules
#
#     ''' feature '''
#     Arg1_production_rules = dict_util.get_Arg_production_rules(relation, "Arg1", parse_dict)
#     Arg2_production_rules = dict_util.get_Arg_production_rules(relation, "Arg2", parse_dict)
#     Arg1_and_Arg2_production_rules = list(set(Arg1_production_rules) & set(Arg2_production_rules))
#
#     feat_Arg1 = get_feature_by_feat_list(dict_production_rules, Arg1_production_rules)
#     feat_Arg2 = get_feature_by_feat_list(dict_production_rules, Arg2_production_rules)
#     feat_Arg1_and_Arg2 = get_feature_by_feat_list(dict_production_rules, Arg1_and_Arg2_production_rules)
#
#     return util.mergeFeatures([feat_Arg1, feat_Arg2, feat_Arg1_and_Arg2])

def production_rules(relation, parse_dict):
    '''load dict '''
    dict_production_rules = Non_Explicit_dict().dict_production_rules

    ''' feature '''
    Arg1_production_rules = dict_util.get_Arg_production_rules(relation, "Arg1", parse_dict)
    Arg2_production_rules = dict_util.get_Arg_production_rules(relation, "Arg2", parse_dict)
    Arg1_and_Arg2_production_rules = list(set(Arg1_production_rules) & set(Arg2_production_rules))

    Arg1_production_rules = ["Arg1_%s" % rule for rule in Arg1_production_rules]
    Arg2_production_rules = ["Arg2_%s" % rule for rule in Arg2_production_rules]
    Both_production_rules = ["Both_%s" % rule for rule in Arg1_and_Arg2_production_rules]

    rules = Arg1_production_rules + Arg2_production_rules + Both_production_rules

    return get_feature_by_feat_list(dict_production_rules, rules)

# def arg_brown_cluster(relation, parse_dict):
#     # load dict
#     dict_brown_cluster = Non_Explicit_dict().dict_Arg_brown_cluster
#     ''' feature '''
#     Arg1_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg1", parse_dict)
#     Arg2_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg2", parse_dict)
#     Both_brown_cluster = list(set(Arg1_brown_cluster) & set(Arg2_brown_cluster))
#
#     Arg1_brown_cluster = ["Arg1_%s" % x for x in Arg1_brown_cluster]
#     Arg2_brown_cluster = ["Arg2_%s" % x for x in Arg2_brown_cluster]
#     Both_brown_cluster = ["Both_%s" % x for x in Both_brown_cluster]
#
#     cluster = Arg1_brown_cluster + Arg2_brown_cluster + Both_brown_cluster
#
#     return get_feature_by_feat_list(dict_brown_cluster, cluster)

# 跟他论文一样
def arg_brown_cluster(relation, parse_dict):
    # load dict
    dict_brown_cluster = Non_Explicit_dict().dict_Arg_brown_cluster
    ''' feature '''
    Arg1_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg1", parse_dict)
    Arg2_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg2", parse_dict)
    Both_brown_cluster = list(set(Arg1_brown_cluster) & set(Arg2_brown_cluster))

    Arg1_only = list(set(Arg1_brown_cluster) - set(Arg2_brown_cluster))
    Arg2_only = list(set(Arg2_brown_cluster) - set(Arg1_brown_cluster))

    Arg1_brown_cluster = ["Arg1_%s" % x for x in Arg1_only]
    Arg2_brown_cluster = ["Arg2_%s" % x for x in Arg2_only]
    Both_brown_cluster = ["Both_%s" % x for x in Both_brown_cluster]

    cluster = Arg1_brown_cluster + Arg2_brown_cluster + Both_brown_cluster

    return get_feature_by_feat_list(dict_brown_cluster, cluster)


def dependency_rules(relation, parse_dict):
    ''' load dict '''
    dict_dependency_rules = Non_Explicit_dict().dict_dependency_rules

    ''' feature '''
    Arg1_dependency_rules = dict_util.get_Arg_dependency_rules(relation, "Arg1", parse_dict)
    Arg2_dependency_rules = dict_util.get_Arg_dependency_rules(relation, "Arg2", parse_dict)
    Arg1_and_Arg2_dependency_rules = list(set(Arg1_dependency_rules) & set(Arg2_dependency_rules))

    feat_Arg1 = get_feature_by_feat_list(dict_dependency_rules, Arg1_dependency_rules)
    feat_Arg2 = get_feature_by_feat_list(dict_dependency_rules, Arg2_dependency_rules)
    feat_Arg1_and_Arg2 = get_feature_by_feat_list(dict_dependency_rules, Arg1_and_Arg2_dependency_rules)

    return util.mergeFeatures([feat_Arg1, feat_Arg2, feat_Arg1_and_Arg2])

def firstlast_first3(relation, parse_dict):
    # load dict
    dict_Arg1_first = Non_Explicit_dict().dict_Arg1_first
    dict_Arg1_last = Non_Explicit_dict().dict_Arg1_last
    dict_Arg2_first = Non_Explicit_dict().dict_Arg2_first
    dict_Arg2_last = Non_Explicit_dict().dict_Arg2_last
    dict_Arg1_first_Arg2_first = Non_Explicit_dict().dict_Arg1_first_Arg2_first
    dict_Arg1_last_Arg2_last = Non_Explicit_dict().dict_Arg1_last_Arg2_last
    dict_Arg1_first3 = Non_Explicit_dict().dict_Arg1_first3
    dict_Arg2_first3 = Non_Explicit_dict().dict_Arg2_first3

    ''' feature '''
    Arg1_first, Arg1_last, Arg2_first, Arg2_last,\
    Arg1_first_Arg2_first, Arg1_last_Arg2_last,\
    Arg1_first3, Arg2_first3 \
         = dict_util.get_firstlast_first3(relation, parse_dict)

    features = []
    features.append(get_feature_by_feat(dict_Arg1_first,Arg1_first))
    features.append(get_feature_by_feat(dict_Arg1_last,Arg1_last))
    features.append(get_feature_by_feat(dict_Arg2_first,Arg2_first))
    features.append(get_feature_by_feat(dict_Arg2_last,Arg2_last))
    features.append(get_feature_by_feat(dict_Arg1_first_Arg2_first,Arg1_first_Arg2_first))
    features.append(get_feature_by_feat(dict_Arg1_last_Arg2_last,Arg1_last_Arg2_last))
    features.append(get_feature_by_feat(dict_Arg1_first3,Arg1_first3))
    features.append(get_feature_by_feat(dict_Arg2_first3,Arg2_first3))

    return util.mergeFeatures(features)


#polarity
def polarity(relation, parse_dict):
    vec_arg1 = dict_util.get_polarity_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_polarity_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# MPQA polarity
def MPQA_polarity(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# MPQA polarity score
def MPQA_polarity_score(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_score_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_score_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# 不考虑，strong, weak
def MPQA_polarity_no_strong_weak(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_no_strong_weak_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_no_strong_weak_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# # modality
# def modality(relation, parse_dict):
#
#     '''feature'''
#     Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
#     Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
#
#     Arg1_modality_vec = dict_util.get_modality_vec(Arg1_words)
#     Arg2_modality_vec = dict_util.get_modality_vec(Arg2_words)
#     # cp = util.cross_product(Arg1_modality_vec, Arg2_modality_vec)
#
#     features = []
#     # features.append(get_feature_by_list(Arg1_modality_vec))
#     # features.append(get_feature_by_list(Arg2_modality_vec))
#     # features.append(get_feature_by_list(cp))
#     Arg1_feat = 0
#     if sum(Arg1_modality_vec) > 0:
#         Arg1_feat = 1
#
#     Arg2_feat = 0
#     if sum(Arg2_modality_vec) > 0:
#         Arg2_feat = 1
#
#     feat_1 = Feature("", 2, {1:Arg1_feat, 2: Arg2_feat})
#     # 0_0 ,0_1, 1_1,1_0
#     dict = {"0_0": 1, "0_1": 2, "1_0": 3, "1_1": 4}
#     feat_2 = get_feature_by_feat(dict, "%d_%d" % (Arg1_feat, Arg2_feat))
#
#
#     return util.mergeFeatures([feat_1, feat_2])

# modality
def modality(relation, parse_dict):

    '''feature'''
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)

    # 具体的modal
    Arg1_modality_vec = dict_util.get_modality_vec(Arg1_words)
    Arg2_modality_vec = dict_util.get_modality_vec(Arg2_words)
    cp = util.cross_product(Arg1_modality_vec, Arg2_modality_vec)

    # # presence or absence
    # Arg1_has_modal = [0, 0]
    # Arg2_has_modal = [0, 0]
    # if sum(Arg1_modality_vec) > 0:
    #     Arg1_has_modal[1] = 1
    # else:
    #     Arg1_has_modal[0] = 1
    #
    # if sum(Arg2_modality_vec) > 0:
    #     Arg2_has_modal[1] = 1
    # else:
    #     Arg2_has_modal[0] = 1

    # has_cp = util.cross_product(Arg1_has_modal, Arg2_has_modal)

    features = []
    features.append(get_feature_by_list(Arg1_modality_vec))
    features.append(get_feature_by_list(Arg2_modality_vec))
    features.append(get_feature_by_list(cp))

    # features.append(get_feature_by_list(Arg1_has_modal))
    # features.append(get_feature_by_list(Arg2_has_modal))
    # features.append(get_feature_by_list(has_cp))

    return util.mergeFeatures(features)

def verbs(relation, parse_dict):
    #load dict
    dict_verb_classes = Non_Explicit_dict().dict_verb_classes

    '''feature'''
    # 1. the number of pairs of verbs in Arg1 and Arg2 from same verb class
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)

    count = 0
    for w1, w2 in [(w1.lower(), w2.lower()) for w1 in Arg1_words for w2 in Arg2_words]:
        if w1 in dict_verb_classes and w2 in dict_verb_classes:
            c1 = dict_verb_classes[w1]
            c2 = dict_verb_classes[w2]
            if set(c1.split("#")) & set(c2.split("#")) != set([]):
                count += 1
    feat_1 = Feature("", 1, {1: count})
    # print feat_1.feat_string

    # # 2. 动词短语的平均长度,int
    # Arg1_average_length_verb_phrase = dict_util.get_Arg_average_length_verb_phrase(relation, "Arg1", parse_dict)
    # Arg2_average_length_verb_phrase = dict_util.get_Arg_average_length_verb_phrase(relation, "Arg2", parse_dict)
    # cp_average_length_verb_phrase = Arg1_average_length_verb_phrase * Arg2_average_length_verb_phrase
    #
    # feat_2 = Feature("", 3, {1:Arg1_average_length_verb_phrase, 2: Arg2_average_length_verb_phrase})
    # # print feat_2.feat_string

    #3. POS of main verb
    Arg1_MV_POS = dict_util.get_main_verb_pos(relation, "Arg1", parse_dict)
    Arg2_MV_POS = dict_util.get_main_verb_pos(relation, "Arg2", parse_dict)

    # cp_MV_POS = util.cross_product(Arg1_MV_POS, Arg2_MV_POS)

    MV_POS_feature_list = Arg1_MV_POS + Arg2_MV_POS

    MV_POS_feature = get_feature_by_list(MV_POS_feature_list)

    # print Arg1_MV_POS_feature.feat_string
    # print Arg2_MV_POS_feature.feat_string

    return util.mergeFeatures([feat_1, MV_POS_feature])


def Inquirer(relation, parse_dict):
    vec_arg1 = dict_util.get_inquirer_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_inquirer_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)
    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

def brown_cluster_pair(relation, parse_dict):
    ''' load dict '''
    dict_word_pairs = Non_Explicit_dict().dict_brown_cluster
    ''' feature '''
    brown_cluster_pairs = dict_util.get_brown_cluster_pairs(relation, parse_dict)

    return get_feature_by_feat_list(dict_word_pairs, brown_cluster_pairs)

#
def money_date_percent(relation, parse_dict):
    Arg1_MDP = _find_Arg_money_date_percent(relation, "Arg1", parse_dict)
    Arg2_MDP = _find_Arg_money_date_percent(relation, "Arg2", parse_dict)
    cp = util.cross_product(Arg1_MDP, Arg2_MDP)

    return get_feature_by_list(Arg1_MDP + Arg2_MDP + cp)

#[0, 1, 2]
def _find_Arg_money_date_percent(relation, Arg, parse_dict):
    MDP = [0] * 2
    ner_tags = dict_util.get_Arg_NER_TAG_List(relation, Arg, parse_dict)
    for tag in ner_tags:
        if tag == "MONEY":
            MDP[0] = 1
        # if tag == "DATE":
        #     MDP[1] = 1
        if tag == "PERCENT":
            MDP[1] = 1
    return MDP

# main verb pair

def main_verb_pair(relation, parse_dict):
    # load dict
    dict_main_verb_pair = Non_Explicit_dict().dict_main_verb_pair
    #feature
    main_verb_pair = dict_util.get_main_verb_pair(relation, parse_dict)

    return get_feature_by_feat(dict_main_verb_pair, main_verb_pair)

''' word embedding '''

def Arg_word2vec(relation, parse_dict):
    ''' load dict '''
    dict_word2vec = Non_Explicit_dict().word2vec_dict

    ''' feature '''
    Arg1_words = dict_util._get_lower_case_lemma_words(relation, "Arg1", parse_dict)
    Arg2_words = dict_util._get_lower_case_lemma_words(relation, "Arg2", parse_dict)

    Arg1_words = list(set(Arg1_words))
    Arg2_words = list(set(Arg2_words))

    Arg1_vec = [0.0] * 300
    Arg1_length = 0
    for word in Arg1_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg1_vec = util.vec_plus_vec(Arg1_vec, vec)
            Arg1_length += 1

    Arg2_vec = [0.0] * 300
    Arg2_length = 0
    for word in Arg2_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg2_vec = util.vec_plus_vec(Arg2_vec, vec)
            Arg2_length += 1

    # 取平均
    if Arg1_length != 0:
        Arg1_vec = [v/Arg1_length for v in Arg1_vec]
    if Arg2_length != 0:
        Arg2_vec = [v/Arg2_length for v in Arg2_vec]

    feat1 = get_feature_by_list(Arg1_vec)
    feat2 = get_feature_by_list(Arg2_vec)

    return util.mergeFeatures([feat1, feat2])




def word2vec_cluster_pair(relation, parse_dict):
    ''' load dict '''
    dict_word2vec_cluster_pairs = Non_Explicit_dict().dict_word2vec_cluster_pairs
    ''' feature '''
    word2vec_cluster_pairs = dict_util.get_word2vec_cluster_pairs(relation, parse_dict)

    return get_feature_by_feat_list(dict_word2vec_cluster_pairs, word2vec_cluster_pairs)


def arg_tense_pair(relation, parse_dict):
    # load dict
    dict_arg_tense_pair = Non_Explicit_dict().dict_arg_tense_pair
    ''' feature '''
    arg_tense_pair = dict_util.get_arg1_arg2_tense_pair(relation, parse_dict)

    return get_feature_by_feat(dict_arg_tense_pair, arg_tense_pair)

def arg1_tense(relation, parse_dict):
    # load dict
    dict_arg1_tense = Non_Explicit_dict().dict_arg1_tense
    ''' feature '''
    arg1_tense = dict_util.get_arg1_tense(relation, parse_dict)

    return get_feature_by_feat(dict_arg1_tense, arg1_tense)

def arg2_tense(relation, parse_dict):
    # load dict
    dict_arg2_tense = Non_Explicit_dict().dict_arg2_tense
    ''' feature '''
    arg2_tense = dict_util.get_arg2_tense(relation, parse_dict)

    return get_feature_by_feat(dict_arg2_tense, arg2_tense)

def arg_first3_conn_pair(relation, parse_dict):
    # load dict
    dict_arg_first3_conn_pair = Non_Explicit_dict().dict_arg_first3_conn_pair
    ''' feature '''
    arg_first3_conn_pair = dict_util.get_arg_first3_conn_pair(relation, parse_dict)

    return get_feature_by_feat(dict_arg_first3_conn_pair, arg_first3_conn_pair)

def arg1_first3_conn(relation, parse_dict):
    # load dict
    dict_arg1_first3_conn = Non_Explicit_dict().dict_arg1_first3_conn
    ''' feature '''
    arg1_first3_conn = dict_util.get_arg1_first3_conn(relation, parse_dict)

    return get_feature_by_feat(dict_arg1_first3_conn, arg1_first3_conn)

def arg2_first3_conn(relation, parse_dict):
    # load dict
    dict_arg2_first3_conn = Non_Explicit_dict().dict_arg2_first3_conn
    ''' feature '''
    arg2_first3_conn = dict_util.get_arg2_first3_conn(relation, parse_dict)

    return get_feature_by_feat(dict_arg2_first3_conn, arg2_first3_conn)


def verb_pair(relation, parse_dict):
    # load dict
    dict_verb_pair = Non_Explicit_dict().dict_verb_pair
    # feature
    verb_pair = dict_util.get_verb_pair(relation, parse_dict)

    return get_feature_by_feat_list(dict_verb_pair, verb_pair)


def prev_context_conn(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_context_conn = Non_Explicit_dict().dict_prev_context_conn
    # feature
    prev_context_conn = dict_util.get_prev_context_conn(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_context_conn, prev_context_conn)

def prev_context_sense(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_context_sense = Non_Explicit_dict().dict_prev_context_sense
    # feature
    prev_context_sense = dict_util.get_prev_context_sense(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_context_sense, prev_context_sense)

def prev_context_conn_sense(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_context_conn_sense = Non_Explicit_dict().dict_prev_context_conn_sense
    # feature
    prev_context_conn_sense = dict_util.get_prev_context_conn_sense(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_context_conn_sense, prev_context_conn_sense)

def next_context_conn(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_next_context_conn = Non_Explicit_dict().dict_next_context_conn
    # feature
    next_context_conn = dict_util.get_next_context_conn(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_next_context_conn, next_context_conn)


def prev_next_context_conn(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_next_context_conn = Non_Explicit_dict().dict_prev_next_context_conn
    # feature
    prev_next_context_conn = dict_util.get_prev_next_context_conn(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_next_context_conn, prev_next_context_conn)


def _LM_conn(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. sent1 ,sent2 之间插入 implicit connective
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    implicit_conn_list = list(dict_pdtb_impilicit_connective.keys())

    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open(config.INPUT_LM, "w")
    for conn in implicit_conn_list:
        fout.write("%s %s %s\n\n" % (Arg1_tokens, conn, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 > %s" % (config.INPUT_LM, config.LM, config.OUTPUT_LM)
    os.system(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(config.OUTPUT_LM)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(implicit_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))

    # 7. 取前面一个连接词，作为特征
    n = 10
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, top_n_conn_list)

def LM_impl_conn_1(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. sent1 ,sent2 之间插入 implicit connective
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    implicit_conn_list = list(dict_pdtb_impilicit_connective.keys())

    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open(config.INPUT_LM, "w")
    for conn in implicit_conn_list:
        fout.write("%s %s %s\n\n" % (Arg1_tokens, conn, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 " % (config.INPUT_LM, config.LM)
    r = os.popen(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(r)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(implicit_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))
    write_LM_sorted_conns(sorted_conns, relation)

    # 7. 取前面n个连接词，作为特征
    n = 20
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, top_n_conn_list)


# 读文件，dict[ID] = [conn1, conn2,..]
dict_LM_impl_conn1 = {}
fin = open(config.CWD + "data/LM_sorted_conns")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_LM_impl_conn1[ID] = conn_list
fin.close()

def LM_impl_conn_1_from_file(relation, parse_dict):
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    ID = str(relation["ID"])
    conn_list = dict_LM_impl_conn1[ID]
    # 取 top n
    top_n = 7

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, conn_list[:top_n])

def LM_impl_conn_1_from_file_by_top_n(relation, parse_dict, top_n):
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    ID = str(relation["ID"])
    conn_list = dict_LM_impl_conn1[ID]
    # 取 top n
    # n = 60

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, conn_list[:top_n])

# 读文件，dict[ID] = [conn1, conn2,..]
dict_LM_impl_conn2 = {}
fin = open(config.CWD + "data/LM_impl_conn2.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_LM_impl_conn2[ID] = conn_list
fin.close()

def LM_impl_conn_2_from_file(relation, parse_dict):
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    _implicit_conn_list = list(dict_pdtb_impilicit_connective.keys())

    implicit_conn_list = ["mid_%s" % conn for conn in _implicit_conn_list] + ["first_%s" % conn for conn in _implicit_conn_list]
    dict_pdtb_impilicit_connective = dict(list(zip(implicit_conn_list, list(range(1, len(implicit_conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_LM_impl_conn2[ID]
    # 取 top n
    top_n = 5

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, conn_list[:top_n])

def LM_impl_conn_2_from_file_by_top_n(relation, parse_dict, top_n):

    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    _implicit_conn_list = list(dict_pdtb_impilicit_connective.keys())

    implicit_conn_list = ["mid_%s" % conn for conn in _implicit_conn_list] + ["first_%s" % conn for conn in _implicit_conn_list]
    dict_pdtb_impilicit_connective = dict(list(zip(implicit_conn_list, list(range(1, len(implicit_conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_LM_impl_conn2[ID]
    # 取 top n

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, conn_list[:top_n])


# 读文件，dict[ID] = [conn1, conn2,..]
dict_LM_exp_conn1 = {}
fin = open(config.CWD + "data/LM_exp_conn1.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_LM_exp_conn1[ID] = conn_list
fin.close()

def LM_exp_conn1_from_file(relation, parse_dict):
    _exp_conn_list = Connectives_dict().sorted_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn1[ID]
    # 取 top n
    top_n = 6

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])

def LM_exp_conn1_from_file_by_top_n(relation, parse_dict, top_n):

    _exp_conn_list = Connectives_dict().sorted_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn1[ID]

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])

# 读文件，dict[ID] = [conn1, conn2,..]
dict_LM_exp_conn2 = {}
fin = open(config.CWD + "data/LM_exp_conn2.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_LM_exp_conn2[ID] = conn_list
fin.close()

def LM_exp_conn2_from_file(relation, parse_dict):
    _exp_conn_list = Connectives_dict().xuyu_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn2[ID]
    # 取 top n
    top_n = 9

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])

def LM_exp_conn2_from_file_by_top_n(relation, parse_dict, top_n):

    _exp_conn_list = Connectives_dict().xuyu_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn2[ID]

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])


# 读文件，dict[ID] = [conn1, conn2,..]
dict_LM_exp_conn3 = {}
fin = open(config.CWD + "data/LM_exp_conn3.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_LM_exp_conn3[ID] = conn_list
fin.close()

def LM_exp_conn3_from_file(relation, parse_dict):
    exp_conn_list = Connectives_dict().freely_omissible_conn_list
    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn3[ID]
    # 取 top n
    top_n = 9

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])

def LM_exp_conn3_from_file_by_top_n(relation, parse_dict, top_n):

    exp_conn_list = Connectives_dict().freely_omissible_conn_list
    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))


    ID = str(relation["ID"])
    conn_list = dict_LM_exp_conn3[ID]

    return get_feature_by_feat_list(dict_exp_conn, conn_list[:top_n])




# ID|conn:ppl|conn:ppl|...
def write_LM_sorted_conns(sorted_conns, relation):
    ID = relation["ID"]
    s = "|".join(["%s:%s" % (conn, str(ppl)) for conn, ppl in sorted_conns])
    file = open("LM_sorted_conns", "a")
    file.write("%s|%s\n" % (ID, s))
    file.close()

# ID|conn:ppl|conn:ppl|...
def write_LM_sorted_conns_to_file(sorted_conns, relation, to_file):
    ID = relation["ID"]
    s = "|".join(["%s:%s" % (conn, str(ppl)) for conn, ppl in sorted_conns])
    file = open(to_file, "a")
    file.write("%s|%s\n" % (ID, s))
    file.close()


def read_LM_output(r):
        ppl_list = []

        for line in r.readlines():
            pattern = re.compile(r'logprob=(.*)ppl= (.*)ppl1=(.*)')
            match = pattern.search(line)
            if match:
                ppl_list.append(float(match.group(2)))

        return ppl_list

def _read_LM_output(filename):
        ppl_list = []

        for line in open(filename):
            pattern = re.compile(r'logprob=(.*)ppl= (.*)ppl1=(.*)')
            match = pattern.search(line)
            if match:
                ppl_list.append(float(match.group(2)))

        return ppl_list

def LM_impl_conn_2(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. conn sent1. sent2  and sent1. conn sent2
    dict_pdtb_impilicit_connective = Non_Explicit_dict().dict_pdtb_impilicit_connective
    _implicit_conn_list = list(dict_pdtb_impilicit_connective.keys())

    implicit_conn_list = ["mid_%s" % conn for conn in _implicit_conn_list] + ["first_%s" % conn for conn in _implicit_conn_list]
    dict_pdtb_impilicit_connective = dict(list(zip(implicit_conn_list, list(range(1, len(implicit_conn_list)+1)))))

    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open(config.INPUT_LM, "w")
    for conn in implicit_conn_list:
        position, conn_name = conn.split("_")
        if position == "mid":
            fout.write("%s %s %s\n\n" % (Arg1_tokens, conn_name, Arg2_tokens))
        if position == "first":
            fout.write("%s %s %s\n\n" % (conn_name, Arg1_tokens, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 " % (config.INPUT_LM, config.LM)
    r = os.popen(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(r)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(implicit_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))
    write_LM_sorted_conns_to_file(sorted_conns, relation, "LM_impl_conn2.txt")

    # 7. 取前面n个连接词，作为特征
    n = 20
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    return get_feature_by_feat_list(dict_pdtb_impilicit_connective, top_n_conn_list)

def LM_exp_conn_1(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. conn sent1. sent2  and sent1. conn sent2
    _exp_conn_list = Connectives_dict().sorted_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)


    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open("input_lm_exp", "w")
    for conn in exp_conn_list:
        position, conn_name = conn.split("_")
        if position == "parallel":
            conn1 = conn_name.split("..")[0]
            conn2 = conn_name.split("..")[1]
            fout.write("%s %s %s %s\n\n" % (conn1, Arg1_tokens, conn2, Arg2_tokens))
        if position == "mid":
            fout.write("%s %s %s\n\n" % (Arg1_tokens, conn_name, Arg2_tokens))
        if position == "first":
            fout.write("%s %s %s\n\n" % (conn_name, Arg1_tokens, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 " % ("input_lm_exp", config.LM)
    r = os.popen(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(r)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(exp_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))
    # write_LM_sorted_conns_to_file(sorted_conns, relation, "LM_exp_conn1.txt")

    # 7. 取前面n个连接词，作为特征
    n = 6
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))

    return get_feature_by_feat_list(dict_exp_conn, top_n_conn_list)

# 使用xuyu的conns
def LM_exp_conn_2(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. conn sent1. sent2  and sent1. conn sent2
    _exp_conn_list = Connectives_dict().xuyu_conns_list
    exp_conn_list = []
    for exp_conn in _exp_conn_list:
        # parallel connective
        if ".." in exp_conn:
            exp_conn_list.append("parallel_%s" % exp_conn)
        else:
            exp_conn_list.append("first_%s" % exp_conn)
            exp_conn_list.append("mid_%s" % exp_conn)


    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open(config.INPUT_LM, "w")
    for conn in exp_conn_list:
        position, conn_name = conn.split("_")
        if position == "parallel":
            conn1 = conn_name.split("..")[0]
            conn2 = conn_name.split("..")[1]
            fout.write("%s %s %s %s\n\n" % (conn1, Arg1_tokens, conn2, Arg2_tokens))
        if position == "mid":
            fout.write("%s %s %s\n\n" % (Arg1_tokens, conn_name, Arg2_tokens))
        if position == "first":
            fout.write("%s %s %s\n\n" % (conn_name, Arg1_tokens, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 " % (config.INPUT_LM, config.LM)
    r = os.popen(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(r)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(exp_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))
    # write_LM_sorted_conns_to_file(sorted_conns, relation, "LM_exp_conn2.txt")

    # 7. 取前面n个连接词，作为特征
    n = 9
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))

    return get_feature_by_feat_list(dict_exp_conn, top_n_conn_list)


def LM_exp_conn_3(relation, parse_dict):
    # 1. 获取arg1, arg2 所在的两个句子
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

    Arg1_sent_length = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
    Arg2_sent_length = len(parse_dict[DocID]["sentences"][Arg2_sent_index]["words"])

    Arg1_tokens = " ".join([parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]
                            for index in range(0, Arg1_sent_length)])

    Arg2_tokens = " ".join([parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]
                            for index in range(0, Arg2_sent_length)])

    # 2. conn sent1. sent2  and sent1. conn sent2
    exp_conn_list = Connectives_dict().freely_omissible_conn_list

    Arg1_tokens = Arg1_tokens.lower()
    Arg2_tokens = Arg2_tokens.lower()

    fout = open(config.INPUT_LM, "w")
    for conn in exp_conn_list:
        fout.write("%s %s %s\n\n" % (Arg1_tokens, conn, Arg2_tokens))
    fout.close()

    # 3. 计算 ppl
    cmd = "ngram -ppl %s -order 5 -lm %s -debug 1 " % (config.INPUT_LM, config.LM)
    r = os.popen(cmd)

    # 4. 获取每个句子的ppl
    ppl_list = read_LM_output(r)

    # 5. conn -> ppl
    dict_conn_ppl = dict(list(zip(exp_conn_list, ppl_list)))

    # 6. 按升序排
    # [('A', 1), ('C', 2), ('B', 3)]
    sorted_conns = sorted(iter(dict_conn_ppl.items()), key=operator.itemgetter(1))
    write_LM_sorted_conns_to_file(sorted_conns, relation, "LM_exp_conn3.txt")

    # 7. 取前面n个连接词，作为特征
    n = 9
    top_n_conn_list = [conn for conn, ppl in sorted_conns[:n]]

    # 8. 特征

    dict_exp_conn = dict(list(zip(exp_conn_list, list(range(1, len(exp_conn_list) + 1)))))

    return get_feature_by_feat_list(dict_exp_conn, top_n_conn_list)


# use word2vec to predict explicit connective for implicit relation
def word2vec_predicted_conn_1(relation, parse_dict):
    ''' load dict '''
    dict_word2vec = Non_Explicit_dict().word2vec_dict

    ''' feature '''
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)

    Arg1_words = list(set(Arg1_words))
    Arg2_words = list(set(Arg2_words))

    # Arg1_words = dict_util._get_lower_case_lemma_words(relation, "Arg1", parse_dict)
    # Arg2_words = dict_util._get_lower_case_lemma_words(relation, "Arg2", parse_dict)



    Arg1_vec = [0.0] * 300
    Arg1_length = 0
    for word in Arg1_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg1_vec = util.vec_plus_vec(Arg1_vec, vec)
            Arg1_length += 1

    Arg2_vec = [0.0] * 300
    Arg2_length = 0
    for word in Arg2_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg2_vec = util.vec_plus_vec(Arg2_vec, vec)
            Arg2_length += 1


    # Arg1, Arg2 合并成一个 300维的向量
    Arg_vec = util.vec_plus_vec(Arg1_vec, Arg2_vec)
    Arg_length = Arg1_length + Arg2_length

    # 取平均
    if Arg_length != 0:
        Arg_vec = [v/Arg_length for v in Arg_vec]

    # 获取Arg_vec 与 conn_vec 按cosine 降排的conn_list
    sorted_conn_list = get_word2vec_predicted_conn_list(Arg_vec)
    write_word2vec_predict_conns_to_file(sorted_conn_list, relation, "word2vec_predict_conns_1.txt")

    # 取 top_n 作为特征
    top_n = 8


    conn_list = [conn.replace("..", " ") for conn in Connectives_dict().sorted_conns_list]
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    return get_feature_by_feat_list(dict_conn, sorted_conn_list[:top_n])

# use word2vec to predict explicit connective for implicit relation
def word2vec_predicted_conn_2(relation, parse_dict):
    ''' load dict '''
    dict_word2vec = Non_Explicit_dict().word2vec_dict

    ''' feature '''
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)


    Arg1_vec = [0.0] * 300
    Arg1_length = 0
    for word in Arg1_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg1_vec = util.vec_plus_vec(Arg1_vec, vec)
            Arg1_length += 1

    Arg2_vec = [0.0] * 300
    Arg2_length = 0
    for word in Arg2_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg2_vec = util.vec_plus_vec(Arg2_vec, vec)
            Arg2_length += 1


    # Arg1 - Arg2
    # 取平均
    if Arg1_length != 0:
        Arg1_vec = [v/Arg1_length for v in Arg1_vec]
    if Arg2_length != 0:
        Arg2_vec = [v/Arg2_length for v in Arg2_vec]

    Arg_vec = util.vec_minus_vec(Arg1_vec, Arg2_vec)



    # 获取Arg_vec 与 conn_vec 按cosine 降排的conn_list
    sorted_conn_list = get_word2vec_predicted_conn_list(Arg_vec)
    write_word2vec_predict_conns_to_file(sorted_conn_list, relation, "word2vec_predict_conns_2.txt")

    # 取 top_n 作为特征
    top_n = 10


    conn_list = [conn.replace("..", " ") for conn in Connectives_dict().sorted_conns_list]
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    return get_feature_by_feat_list(dict_conn, sorted_conn_list[:top_n])

def get_conn_vec_dict():
    dict_word2vec = Non_Explicit_dict().word2vec_dict

    conn_list = Connectives_dict().word2vec_conns_list

    conn_vec_dict = {}
    for conn in conn_list:
        conn_vec = [0.0] * 300
        conn_length = 0
        conn = conn.replace("..", " ")
        for item in conn.split(" "):
            if item in dict_word2vec:
                conn_vec = util.vec_plus_vec(conn_vec, dict_word2vec[item])
                conn_length += 1
        # 取平均
        if conn_length != 0:
            conn_vec = [v/conn_length for v in conn_vec]
        #
        conn_vec_dict[conn] = conn_vec

    return conn_vec_dict

conn_vec_dict = get_conn_vec_dict()
def get_word2vec_predicted_conn_list(Arg_vec):
    # get conn_vec_dict ["conn"] = [0.1, 0.2...]
    conn_score_dict = {}
    for conn in conn_vec_dict:
        conn_vec = conn_vec_dict[conn]
        score = util.get_cosine_similarity(conn_vec, Arg_vec)
        conn_score_dict[conn] = score

    # 按cosine similarity 降排
    conn_score_sorted_list = sorted(iter(conn_score_dict.items()), key=operator.itemgetter(1),reverse = True)

    # print conn_score_sorted_list
    return [conn for conn, score in conn_score_sorted_list]


# ID_sense|conn|conn|...
def write_word2vec_predict_conns_to_file(sorted_conns, relation, to_file):
    ID = relation["ID"]
    Sense = relation["Sense"][0]
    s = "|".join(sorted_conns)
    file = open(to_file, "a")
    file.write("%s_%s|%s\n" % (ID, Sense, s))
    file.close()


# 读文件，dict[ID] = [conn1, conn2,..]
dict_word2vec_predict_conn_1 = {}
fin = open(config.CWD + "data/word2vec_predict_conns_1.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0].split("_")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_word2vec_predict_conn_1[ID] = conn_list
fin.close()

def word2vec_predict_conn_1_from_file(relation, parse_dict):
    conn_list = Connectives_dict().word2vec_conns_list
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_word2vec_predict_conn_1[ID]
    # 取 top n
    top_n = 60

    return get_feature_by_feat_list(dict_conn, conn_list[:top_n])

def word2vec_predict_conn_1_from_file_by_top_n(relation, parse_dict, top_n):
    conn_list = Connectives_dict().word2vec_conns_list
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_word2vec_predict_conn_1[ID]
    # 取 top n
    # n = 60

    return get_feature_by_feat_list(dict_conn, conn_list[:top_n])

# 读文件，dict[ID] = [conn1, conn2,..]
dict_word2vec_predict_conn_2 = {}
fin = open(config.CWD + "data/word2vec_predict_conns_2.txt")
for line in fin.readlines():
    line = line.strip()
    ID = line.split("|")[0].split("_")[0]
    conn_list = [item.split(":")[0] for item in line.split("|")[1:]]
    dict_word2vec_predict_conn_2[ID] = conn_list
fin.close()

def word2vec_predict_conn_2_from_file(relation, parse_dict):
    conn_list = [conn.replace("..", " ") for conn in Connectives_dict().sorted_conns_list]
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_word2vec_predict_conn_2[ID]
    # 取 top n
    top_n = 60

    return get_feature_by_feat_list(dict_conn, conn_list[:top_n])

def word2vec_predict_conn_2_from_file_by_top_n(relation, parse_dict, top_n):
    conn_list = [conn.replace("..", " ") for conn in Connectives_dict().sorted_conns_list]
    dict_conn = dict(list(zip(conn_list, list(range(1, len(conn_list)+1)))))

    ID = str(relation["ID"])
    conn_list = dict_word2vec_predict_conn_2[ID]
    # 取 top n
    # n = 60

    return get_feature_by_feat_list(dict_conn, conn_list[:top_n])


def have_same_NNP(relation, parse_dict):
    Arg1_word_list = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg1_pos_list = dict_util.get_Arg_POS_List(relation, "Arg1", parse_dict)

    Arg2_word_list = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg2_pos_list = dict_util.get_Arg_POS_List(relation, "Arg2", parse_dict)

    flag = 0

    # 在 top n 中挑选
    top_n = 3
    Arg1_word_pos_list = list(zip(Arg1_word_list, Arg1_pos_list))[:top_n]
    Arg2_word_pos_list = list(zip(Arg2_word_list, Arg2_pos_list))[:top_n]

    # 专有名词
    Arg1_NNPS = [word for word, pos in Arg1_word_pos_list if "NNP" in pos and word != "Mr."]
    Arg2_NNPS = [word for word, pos in Arg2_word_pos_list if "NNP" in pos and word != "Mr."]

    if set(Arg1_NNPS) & set(Arg2_NNPS) != set([]):
        flag = 1

    if flag == 1:
        return get_feature_by_list([1])
    else:
        return get_feature_by_list([0])


def have_same_NNP_V2(relation, parse_dict):
    Arg1_word_list = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg1_pos_list = dict_util.get_Arg_POS_List(relation, "Arg1", parse_dict)

    Arg2_word_list = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg2_pos_list = dict_util.get_Arg_POS_List(relation, "Arg2", parse_dict)

    flag = 0

    #
    Arg1_word_pos_list = list(zip(Arg1_word_list, Arg1_pos_list))
    Arg2_word_pos_list = list(zip(Arg2_word_list, Arg2_pos_list))

    # 获取开头的连续的NNP
    Arg1_NNPS = []
    i = 0
    while i < len(Arg1_word_pos_list) and "NNP" in Arg1_word_pos_list[i][1]:
        Arg1_NNPS.append(Arg1_word_pos_list[i][0])
        i += 1

    Arg2_NNPS = []
    i = 0
    while i < len(Arg2_word_pos_list) and "NNP" in Arg2_word_pos_list[i][1]:
        Arg2_NNPS.append(Arg2_word_pos_list[i][0])
        i += 1

    if set(Arg1_NNPS) & set(Arg2_NNPS) != set([]):
        print("--" * 45)
        print(Arg1_word_pos_list)
        print(Arg2_word_pos_list)
        print(relation["Sense"][0])
        flag = 1

    if flag == 1:
        return get_feature_by_list([1])
    else:
        return get_feature_by_list([0])

def have_same_NN(relation, parse_dict):
    Arg1_word_list = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg1_pos_list = dict_util.get_Arg_POS_List(relation, "Arg1", parse_dict)

    Arg2_word_list = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg2_pos_list = dict_util.get_Arg_POS_List(relation, "Arg2", parse_dict)

    flag = 0

    # 在 top n 中挑选
    top_n = 5
    Arg1_word_pos_list = list(zip(Arg1_word_list, Arg1_pos_list))[:top_n]
    Arg2_word_pos_list = list(zip(Arg2_word_list, Arg2_pos_list))[:top_n]

    # 名词
    Arg1_NN = [word for word, pos in Arg1_word_pos_list if "NN" in pos and word != "Mr."]
    Arg2_NN = [word for word, pos in Arg2_word_pos_list if "NN" in pos and word != "Mr."]

    if set(Arg1_NN) & set(Arg2_NN) != set([]):
        flag = 1

    if flag == 1:
        return get_feature_by_list([1])
    else:
        return get_feature_by_list([0])

def have_NNP_PRP(relation, parse_dict):
    Arg1_word_list = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg1_pos_list = dict_util.get_Arg_POS_List(relation, "Arg1", parse_dict)

    Arg2_word_list = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg2_pos_list = dict_util.get_Arg_POS_List(relation, "Arg2", parse_dict)

    flag = 0

    # 在 top n 中挑选
    top_n = 5
    Arg1_word_pos_list = list(zip(Arg1_word_list, Arg1_pos_list))[:top_n]
    Arg2_word_pos_list = list(zip(Arg2_word_list, Arg2_pos_list))[:top_n]

    # NNP PRP
    Arg1_NNP = [word for word, pos in Arg1_word_pos_list if "NNP" in pos and word != "Mr."]
    Arg2_PRP = [word for word, pos in Arg2_word_pos_list if "PRP" in pos and word != "Mr."]

    if Arg1_NNP != [] and Arg2_PRP != []:
        flag = 1

    if flag == 1:
        return get_feature_by_list([1])
    else:
        return get_feature_by_list([0])

def have_all_case(relation, parse_dict):
    Arg1_word_list = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg1_pos_list = dict_util.get_Arg_POS_List(relation, "Arg1", parse_dict)

    Arg2_word_list = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg2_pos_list = dict_util.get_Arg_POS_List(relation, "Arg2", parse_dict)

    flag = 0

    # 在 top n 中挑选
    top_n = 5
    Arg1_word_pos_list = list(zip(Arg1_word_list, Arg1_pos_list))[:top_n]
    Arg2_word_pos_list = list(zip(Arg2_word_list, Arg2_pos_list))[:top_n]

    # 专有名词
    Arg1_NNPS = [word for word, pos in Arg1_word_pos_list if "NNP" in pos and word != "Mr."]
    Arg2_NNPS = [word for word, pos in Arg2_word_pos_list if "NNP" in pos and word != "Mr."]

    if set(Arg1_NNPS) & set(Arg2_NNPS) != set([]):
        flag = 1

    # 名词
    Arg1_NNP = [word for word, pos in Arg1_word_pos_list if "NNP" in pos and word != "Mr."]
    Arg2_PRP = [word for word, pos in Arg2_word_pos_list if "PRP" in pos and word != "Mr."]

    if Arg1_NNP != [] and Arg2_PRP != []:
        flag = 1

    # NNP PRP
    Arg1_NNP = [word for word, pos in Arg1_word_pos_list if "NNP" in pos and word != "Mr."]
    Arg2_PRP = [word for word, pos in Arg2_word_pos_list if "PRP" in pos and word != "Mr."]

    if Arg1_NNP != [] and Arg2_PRP != []:
        flag = 1


    if flag == 1:
        return get_feature_by_list([1])
    else:
        return get_feature_by_list([0])


# [0, 1, 0, 1]
def get_feature_by_list(list):
    feat_dict = {}
    for index, item in enumerate(list):
        if item != 0:
            feat_dict[index+1] = item
    return Feature("", len(list), feat_dict)


def get_feature_by_feat(dict, feat):
    feat_dict = {}
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_feat_list(dict, feat_list):
    feat_dict = {}
    for feat in feat_list:
        if feat in dict:
            feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

