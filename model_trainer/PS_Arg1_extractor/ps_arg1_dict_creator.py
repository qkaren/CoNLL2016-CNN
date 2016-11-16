#coding:utf-8
import util
import config
from pdtb_parse import PDTB_PARSE
from connective import Connective
from syntax_tree import Syntax_tree
from clause import Arg_Clauses
from . import ps_arg1_dict_util as dict_util

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        self.IPS_relations = pdtb_parse.pdtb.IPS_relations


    def create_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))

        total = float(len(self.IPS_relations))

        dict = {}
        for curr_index, relation in enumerate(self.IPS_relations):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            for arg_clauses in dict_util.get_arg_clauses_with_label(self.parse_dict, relation):
                if arg_clauses == []: continue
                for clause_index in range(len(arg_clauses.clauses)):
                    result = dict_function(arg_clauses, clause_index, self.parse_dict)
                    if type(result) == list:
                        for item in result:
                            util.set_dict_key_value(dict, item)
                    else:
                        util.set_dict_key_value(dict, result)
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    def create_term_dict(self, threshold = 1):

        print("生成 %s 的字典..." % ("term"))

        total = float(len(self.IPS_relations))

        dict_curr_first = {}
        dict_curr_last = {}
        dict_prev_last = {}
        dict_next_first = {}
        dict_prev_last_curr_first = {}
        dict_curr_last_next_first = {}


        for curr_index, relation in enumerate(self.IPS_relations):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            for arg_clauses in dict_util.get_arg_clauses_with_label(self.parse_dict, relation):
                if arg_clauses == []: continue
                for clause_index in range(len(arg_clauses.clauses)):
                    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, self.parse_dict)
                    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, self.parse_dict)
                    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, self.parse_dict)
                    next_first = dict_util.get_next_first(arg_clauses, clause_index, self.parse_dict)

                    prev_last_curr_first = "%s_%s" % (prev_last, curr_first)
                    curr_last_next_first = "%s_%s" % (curr_last, next_first)

                    util.set_dict_key_value(dict_curr_first, curr_first)
                    util.set_dict_key_value(dict_curr_last, curr_last)
                    util.set_dict_key_value(dict_prev_last, prev_last)
                    util.set_dict_key_value(dict_next_first, next_first)
                    util.set_dict_key_value(dict_prev_last_curr_first, prev_last_curr_first)
                    util.set_dict_key_value(dict_curr_last_next_first, curr_last_next_first)


        #删除频率小于threshold的键
        # util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict_curr_first, config.PS_ARG1_DICT_CURR_FIRST)
        util.write_dict_keys_to_file(dict_curr_last, config.PS_ARG1_DICT_CURR_LAST)
        util.write_dict_keys_to_file(dict_prev_last, config.PS_ARG1_DICT_PREV_LAST)
        util.write_dict_keys_to_file(dict_next_first, config.PS_ARG1_DICT_NEXT_FIRST)
        util.write_dict_keys_to_file(dict_prev_last_curr_first, config.PS_ARG1_DICT_PREV_LAST_CURR_FIRST)
        util.write_dict_keys_to_file(dict_curr_last_next_first, config.PS_ARG1_DICT_CURR_LAST_NEXT_FIRST)


if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_lowercased_verbs, config.PS_ARG1_DICT_LOWERCASE_VERBS)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_lemma_verbs, config.PS_ARG1_DICT_LEMMA_VERBS)
    #
    # Dict_creator(pdtb_parse).create_term_dict()
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_production_rule, config.PS_ARG1_DICT_CURR_PRODUCTION_RULE)



    # Dict_creator(pdtb_parse).create_dict(dict_util.get_con_str, config.PS_ARG1_DICT_CONN_STR)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_con_lstr, config.PS_ARG1_DICT_CONN_LSTR)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_to_root_path, config.PS_ARG1_DICT_CONN_TO_ROOT_PATH)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_to_root_compressed_path, config.PS_ARG1_DICT_CONN_TO_ROOT_COMPRESSED_PATH)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_curr_position, config.PS_ARG1_DICT_CONN_CURR_POSITION)





    ''' --- 下面的未加 －－－'''
    # # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_position_distance, config.PS_ARG1_DICT_CONN_POSITION_DISTANCE)
    #
    # # Dict_creator(pdtb_parse).create_dict(dict_util.get_prev_curr_CP_production_rule, config.PS_ARG1_DICT_PREV_CURR_CP_PRODUCTION_RULE, 5)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_to_root_path, config.PS_ARG1_DICT_CONN_TO_ROOT_PATH)
    #
    # # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_to_root_compressed_path, config.PS_ARG1_DICT_CONN_TO_ROOT_COMPRESSED_PATH)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_position, config.PS_ARG1_DICT_CONN_POSITION)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_is_adjacent_to_conn, config.PS_ARG1_DICT_CONN_IS_ADJACENT_TO_CONN)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_first_curr_first_lemma_verb, config.PS_ARG1_DICT_CURR_FIRST_CURR_FIRST_LEMMA_VERB)


    # Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_first_prev_last_parse_path, config.PS_ARG1_DICT_CURR_FIRST_PREV_LAST_PARSE_PATH)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_curr_first, config.PS_ARG1_DICT_CONN_CURR_FIRST)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_CParent_to_root_path_node_names, config.PS_ARG1_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_CPOS, config.PS_ARG1_DICT_CPOS)
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_connCtx, config.PS_ARG1_DICT_CONN_CONNCTX)
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_parent_category_Ctx, config.PS_ARG1_DICT_CONN_PARENT_CATEGORY_CTX)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_clause_first_conn_pos, config.PS_ARG1_DICT_CLAUSE_FIRST_CONN_POS)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_clause_main_verb_conn, config.PS_ARG1_DICT_CLAUSE_MAIN_VERB_CONN)






