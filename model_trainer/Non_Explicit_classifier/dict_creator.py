#coding:utf-8
import util
import config
from . import non_exp_dict_util as dict_util
from pdtb_parse import PDTB_PARSE
from connective import Connective
from syntax_tree import Syntax_tree

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        # dict[(DocID, sent_index)] = [[1], [4,5]]
        self.non_explicit_relations = pdtb_parse.pdtb.non_explicit_relations

    def create_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))
        dict = {}
        total = float(len(self.non_explicit_relations))
        for curr_index, relation in enumerate(self.non_explicit_relations):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            result = dict_function(relation, self.parse_dict)
            if type(result) == list:
                for item in result:
                    util.set_dict_key_value(dict, item)
            else:
                util.set_dict_key_value(dict, result)
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    def create_context_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))
        dict = {}
        total = float(len(self.non_explicit_relations))
        for curr_index, relation in enumerate(self.non_explicit_relations):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            result = dict_function(relation, self.parse_dict, pdtb_parse.pdtb.implicit_context_dict)
            if type(result) == list:
                for item in result:
                    util.set_dict_key_value(dict, item)
            else:
                util.set_dict_key_value(dict, result)
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    def create_fisrtlast_first3(self, threshold = 1):
        dict_Arg1_first = {}
        dict_Arg1_last = {}
        dict_Arg2_first = {}
        dict_Arg2_last = {}
        dict_Arg1_first_Arg2_first = {}
        dict_Arg1_last_Arg2_last = {}
        dict_Arg1_first3 = {}
        dict_Arg2_first3 = {}


        for relation in self.non_explicit_relations:
            Arg1_first, Arg1_last, Arg2_first, Arg2_last,\
            Arg1_first_Arg2_first, Arg1_last_Arg2_last,\
            Arg1_first3, Arg2_first3 \
                 = dict_util.get_firstlast_first3(relation, self.parse_dict)

            util.set_dict_key_value(dict_Arg1_first, Arg1_first)
            util.set_dict_key_value(dict_Arg1_last, Arg1_last)
            util.set_dict_key_value(dict_Arg2_first, Arg2_first)
            util.set_dict_key_value(dict_Arg2_last, Arg2_last)
            util.set_dict_key_value(dict_Arg1_first_Arg2_first, Arg1_first_Arg2_first)
            util.set_dict_key_value(dict_Arg1_last_Arg2_last, Arg1_last_Arg2_last)
            util.set_dict_key_value(dict_Arg1_first3, Arg1_first3)
            util.set_dict_key_value(dict_Arg2_first3, Arg2_first3)


        #删除频率小于threshold的键
        util.removeItemsInDict(dict_Arg1_first, threshold)
        util.removeItemsInDict(dict_Arg1_last, threshold)
        util.removeItemsInDict(dict_Arg2_first, threshold)
        util.removeItemsInDict(dict_Arg2_last, threshold)
        util.removeItemsInDict(dict_Arg1_first_Arg2_first, threshold)
        util.removeItemsInDict(dict_Arg1_last_Arg2_last, threshold)
        util.removeItemsInDict(dict_Arg1_first3, threshold)
        util.removeItemsInDict(dict_Arg2_first3, threshold)


        #字典keys写入文件
        util.write_dict_keys_to_file(dict_Arg1_first, config.NON_EXPLICIT_DICT_Arg1_first)
        util.write_dict_keys_to_file(dict_Arg1_last, config.NON_EXPLICIT_DICT_Arg1_last)
        util.write_dict_keys_to_file(dict_Arg2_first, config.NON_EXPLICIT_DICT_Arg2_first)
        util.write_dict_keys_to_file(dict_Arg2_last, config.NON_EXPLICIT_DICT_Arg2_last)
        util.write_dict_keys_to_file(dict_Arg1_first_Arg2_first, config.NON_EXPLICIT_DICT_Arg1_first_Arg2_first)
        util.write_dict_keys_to_file(dict_Arg1_last_Arg2_last, config.NON_EXPLICIT_DICT_Arg1_last_Arg2_last)
        util.write_dict_keys_to_file(dict_Arg1_first3, config.NON_EXPLICIT_DICT_Arg1_first3)
        util.write_dict_keys_to_file(dict_Arg2_first3, config.NON_EXPLICIT_DICT_Arg2_first3)






if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # # word pairs
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_word_pairs, config.NON_EXPLICIT_DICT_WORD_PAIRS, 6)

    # production_rules
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_production_rules, config.NON_EXPLICIT_DICT_PRODUCTION_RULES, 6)

    # #get_dependency_rules
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_dependency_rules, config.NON_EXPLICIT_DICT_DEPENDENCY_RULES, 5)
    #
    # #
    # Dict_creator(pdtb_parse).create_fisrtlast_first3(1)
    #
    # # get_brown_cluster_pairs
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_brown_cluster_pairs, config.NON_EXPLICIT_DICT_BROWN_CLUSTER_PAIRS, 6)

    # get_lemma_words
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_lower_case_lemma_words, config.NON_EXPLICIT_DICT_LOWER_CASE_LEMMA_WORDS, 1)

    # get_main_verb_pair
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_main_verb_pair, config.NON_EXPLICIT_DICT_MAIN_VERB_PAIR, 1)

    # cp production rule
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_cp_production_rules, config.NON_EXPLICIT_DICT_CP_PRODUCTION_RULES, 4)

    # get_all_words
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_all_words, config.NON_EXPLICIT_DICT_ALL_WORDS, 1)

    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_word2vec_cluster_pairs, config.NON_EXPLICIT_DICT_WORD2VEC_CLUSTER_PAIRS, 5)

    # arg tense paire
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg1_arg2_tense_pair, config.NON_EXPLICIT_DICT_ARG_TENSE_PAIR, 1)
    #
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg1_tense, config.NON_EXPLICIT_DICT_ARG1_TENSE, 1)
    #
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg2_tense, config.NON_EXPLICIT_DICT_ARG2_TENSE, 1)

    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg_first3_conn_pair,config.NON_EXPLICIT_DICT_ARG_FIRST3_CONN_PAIR, 1)
    #
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg1_first3_conn, config.NON_EXPLICIT_DICT_ARG1_FIRST3_CONN, 1)
    #
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg2_first3_conn, config.NON_EXPLICIT_DICT_ARG2_FIRST3_CONN, 1)

    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_verb_pair, config.NON_EXPLICIT_DICT_VERB_PAIR, 1)

    # brown_cluster
    # Dict_creator(pdtb_parse).create_dict(
    #     dict_util.get_arg_brown_cluster, config.NON_EXPLICIT_DICT_ARG_BROWN_CLUSTER, 6)

    Dict_creator(pdtb_parse).create_context_dict(
        dict_util.get_prev_context_conn, config.NON_EXPLICIT_DICT_PREV_CONTEXT_CONN, 1)

    # Dict_creator(pdtb_parse).create_context_dict(
    #     dict_util.get_prev_context_conn_sense, config.NON_EXPLICIT_DICT_PREV_CONTEXT_CONN_SENSE, 1)
    #
    Dict_creator(pdtb_parse).create_context_dict(
        dict_util.get_next_context_conn, config.NON_EXPLICIT_DICT_NEXT_CONTEXT_CONN, 1)

    Dict_creator(pdtb_parse).create_context_dict(
        dict_util.get_prev_next_context_conn, config.NON_EXPLICIT_DICT_PREV_NEXT_CONTEXT_CONN, 1)


