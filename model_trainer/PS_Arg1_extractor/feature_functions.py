#coding:utf-8
from ps_arg1_dict import Ps_arg1_dict
from feature import Feature
import model_trainer.PS_Arg1_extractor.ps_arg1_dict_util as dict_util
import util

def _all_features(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Ps_arg1_dict().dict_lowercase_verbs
    dict_lemma_verbs = Ps_arg1_dict().dict_lemma_verbs
    dict_curr_first = Ps_arg1_dict().dict_curr_first
    dict_curr_last = Ps_arg1_dict().dict_curr_last
    dict_prev_last = Ps_arg1_dict().dict_prev_last
    dict_next_first = Ps_arg1_dict().dict_next_first
    dict_prev_last_curr_first = Ps_arg1_dict().dict_prev_last_curr_first
    dict_curr_last_next_first = Ps_arg1_dict().dict_curr_last_next_first
    dict_curr_production_rule = Ps_arg1_dict().dict_curr_production_rule
    dict_position = {"left": 1, "middle": 2, "right": 3}

    ''' mine '''
    dict_con_str = Ps_arg1_dict().dict_con_str
    dict_con_lstr = Ps_arg1_dict().dict_con_lstr
    dict_con_cat = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }
    dict_conn_to_root_path = Ps_arg1_dict().dict_conn_to_root_path
    dict_conn_to_root_compressed_path = Ps_arg1_dict().dict_conn_to_root_compressed_path
    dict_conn_curr_position = Ps_arg1_dict().dict_conn_curr_position
    dict_is_clause_contain_comma_which = {"YES": 1, "NO": 2}

    # 特征
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)
    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)
    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)
    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)
    prev_last_curr_first = dict_util.get_prev_last_curr_first(arg_clauses, clause_index, parse_dict)
    curr_last_next_first = dict_util.get_curr_last_next_first(arg_clauses, clause_index, parse_dict)

    #当前clause的位置信息
    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)

    production_rule_list = dict_util.get_curr_production_rule(arg_clauses, clause_index, parse_dict)

    ''' mine '''
    con_str = dict_util.get_con_str(arg_clauses, clause_index, parse_dict)
    con_lstr = dict_util.get_con_lstr(arg_clauses, clause_index, parse_dict)
    con_cat = dict_util.get_con_cat(arg_clauses, clause_index, parse_dict)
    conn_to_root_path = dict_util.get_conn_to_root_path(arg_clauses, clause_index, parse_dict)
    conn_to_root_compressed_path = dict_util.get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict)
    conn_curr_position = dict_util.get_conn_curr_position(arg_clauses, clause_index, parse_dict)
    is_clause_contain_comma_which = dict_util.get_is_clause_contain_comma_which(arg_clauses, clause_index, parse_dict)


    features = []
    features.append(get_feature_by_feat_list(dict_lowercase_verbs, lowercase_verbs_list))
    features.append(get_feature_by_feat_list(dict_lemma_verbs, lemma_verbs_list))

    features.append(get_feature_by_feat(dict_curr_first, curr_first))
    features.append(get_feature_by_feat(dict_curr_last, curr_last))
    features.append(get_feature_by_feat(dict_prev_last, prev_last))
    features.append(get_feature_by_feat(dict_next_first, next_first))
    features.append(get_feature_by_feat(dict_prev_last_curr_first, prev_last_curr_first))
    features.append(get_feature_by_feat(dict_curr_last_next_first, curr_last_next_first))
    features.append(get_feature_by_feat(dict_position, position))

    ''' production rules '''
    features.append(get_feature_by_feat_list(dict_curr_production_rule, production_rule_list))

    ''' mine '''
    features.append(get_feature_by_feat(dict_con_str, con_str))
    features.append(get_feature_by_feat(dict_con_lstr, con_lstr))
    features.append(get_feature_by_feat(dict_con_cat, con_cat))
    features.append(get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path))
    features.append(get_feature_by_feat(dict_conn_to_root_compressed_path, conn_to_root_compressed_path))
    features.append(get_feature_by_feat(dict_conn_curr_position, conn_curr_position))

    # features.append(get_feature_by_feat(dict_is_clause_contain_comma_which, is_clause_contain_comma_which))

    return util.mergeFeatures(features)

def all_features(arg_clauses, clause_index, parse_dict):
    feature_function_list = [
        # lowercase_verbs,
        lemma_verbs,
        curr_first,
        curr_last,
        # prev_last,
        # next_first,
        prev_last_curr_first,
        # curr_last_next_first,
        # production_rule_list,
        # position,
        # # mine
        # con_str,
        con_lstr,
        con_cat,
        # conn_to_root_path,
        # conn_to_root_compressed_path,
        # conn_curr_position
    ]
    # feature_function_list = [
    #     lemma_verbs,
    #     curr_first,
    #     clause_first_conn_pos,
    #
    #     conn_connCtx,
    #     con_lstr,
    #     CParent_to_root_path_node_names
    # ]

    features = [feature_function(arg_clauses, clause_index, parse_dict) for feature_function in feature_function_list]
    #合并特征
    feature = util.mergeFeatures(features)
    return feature

def lowercase_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Ps_arg1_dict().dict_lowercase_verbs
    # 特征
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lowercase_verbs, lowercase_verbs_list)

def lemma_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lemma_verbs = Ps_arg1_dict().dict_lemma_verbs
    # 特征
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lemma_verbs, lemma_verbs_list)

def curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first = Ps_arg1_dict().dict_curr_first
    # 特征
    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first, curr_first)

def curr_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last = Ps_arg1_dict().dict_curr_last

    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last, curr_last)


def prev_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last = Ps_arg1_dict().dict_prev_last

    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last, prev_last)

def next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_next_first = Ps_arg1_dict().dict_next_first

    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_next_first, next_first)

def prev_last_curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last_curr_first = Ps_arg1_dict().dict_prev_last_curr_first

    prev_last_curr_first = dict_util.get_prev_last_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last_curr_first, prev_last_curr_first)


def curr_last_next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last_next_first = Ps_arg1_dict().dict_curr_last_next_first

    curr_last_next_first = dict_util.get_curr_last_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last_next_first, curr_last_next_first)

def production_rule_list(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_production_rule = Ps_arg1_dict().dict_curr_production_rule

    production_rule_list = dict_util.get_curr_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_curr_production_rule, production_rule_list)

def position(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_position = {"left": 1, "middle": 2, "right": 3}

    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_position, position)


def con_str(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_str = Ps_arg1_dict().dict_con_str

    con_str = dict_util.get_con_str(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_str, con_str)

def con_lstr(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_lstr = Ps_arg1_dict().dict_con_lstr

    con_lstr = dict_util.get_con_lstr(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_lstr, con_lstr)

def con_cat(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_cat = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }

    con_cat = dict_util.get_con_cat(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_cat, con_cat)

def conn_to_root_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_to_root_path = Ps_arg1_dict().dict_conn_to_root_path

    conn_to_root_path = dict_util.get_conn_to_root_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path)

def conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_to_root_compressed_path = Ps_arg1_dict().dict_conn_to_root_compressed_path

    conn_to_root_compressed_path = dict_util.get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_to_root_compressed_path, conn_to_root_compressed_path)

def conn_curr_position(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_curr_position = Ps_arg1_dict().dict_conn_curr_position

    conn_curr_position = dict_util.get_conn_curr_position(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_curr_position, conn_curr_position)


def curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first_prev_last_parse_path = Ps_arg1_dict().dict_curr_first_prev_last_parse_path
    # feature
    curr_first_prev_last_parse_path = dict_util.get_curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first_prev_last_parse_path, curr_first_prev_last_parse_path)

def CParent_to_root_path_node_names(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_CParent_to_root_path_node_names = Ps_arg1_dict().dict_CParent_to_root_path_node_names
    # feature
    CParent_to_root_path_node_names = dict_util.get_CParent_to_root_path_node_names(arg_clauses, clause_index, parse_dict)
    return get_feature_by_feat_list(dict_CParent_to_root_path_node_names, CParent_to_root_path_node_names)

def CPOS(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_CPOS = Ps_arg1_dict().dict_CPOS
    # feature
    CPOS = dict_util.get_CPOS(arg_clauses, clause_index, parse_dict)
    return get_feature_by_feat(dict_CPOS, CPOS)

def conn_connCtx(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_connCtx = Ps_arg1_dict().dict_conn_connCtx
    # feature
    conn_connCtx = dict_util.get_conn_connCtx(arg_clauses, clause_index, parse_dict)
    return get_feature_by_feat(dict_conn_connCtx, conn_connCtx)

def conn_parent_category_Ctx(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_parent_category_Ctx = Ps_arg1_dict().dict_conn_parent_category_Ctx
    # feature
    conn_parent_category_Ctx = dict_util.get_conn_parent_category_Ctx(arg_clauses, clause_index, parse_dict)
    return get_feature_by_feat(dict_conn_parent_category_Ctx, conn_parent_category_Ctx)



def conn_curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_curr_first = Ps_arg1_dict().dict_conn_curr_first
    # feature
    conn_curr_first = dict_util.get_conn_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_curr_first, conn_curr_first)

def clause_first_conn_pos(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_clause_first_conn_pos = Ps_arg1_dict().dict_clause_first_conn_pos
    # feature
    clause_first_conn_pos = dict_util.get_clause_first_conn_pos(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_clause_first_conn_pos, clause_first_conn_pos)

def clause_main_verb_conn(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_clause_main_verb_conn = Ps_arg1_dict().dict_clause_main_verb_conn
    # feature
    clause_main_verb_conn = dict_util.get_clause_main_verb_conn(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_clause_main_verb_conn, clause_main_verb_conn)


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
