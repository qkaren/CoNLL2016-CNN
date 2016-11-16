#coding:utf-8
import util
import config
from . import implicit_arg2_dict_util as dict_util
from pdtb_parse import PDTB_PARSE

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        self.implicit_relations = []
        for relation in pdtb_parse.pdtb.non_explicit_relations:
            if relation["Type"] == "Implicit":
                # 一个句子长度的Arg2，Arg2
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
                if len(set(Arg2_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:
                    self.implicit_relations.append(relation)

    def create_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))

        total = float(len(self.implicit_relations))

        dict = {}
        for curr_index, relation in enumerate(self.implicit_relations):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            # 只考虑arg2
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

        total = float(len(self.implicit_relations))

        dict_curr_first = {}
        dict_curr_last = {}
        dict_prev_last = {}
        dict_next_first = {}
        dict_prev_last_curr_first = {}
        dict_curr_last_next_first = {}

        for curr_index, relation in enumerate(self.implicit_relations):
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
        util.write_dict_keys_to_file(dict_curr_first, config.IMPLICIT_ARG2_DICT_CURR_FIRST)
        util.write_dict_keys_to_file(dict_curr_last, config.IMPLICIT_ARG2_DICT_CURR_LAST)
        util.write_dict_keys_to_file(dict_prev_last, config.IMPLICIT_ARG2_DICT_PREV_LAST)
        util.write_dict_keys_to_file(dict_next_first, config.IMPLICIT_ARG2_DICT_NEXT_FIRST)
        util.write_dict_keys_to_file(dict_prev_last_curr_first, config.IMPLICIT_ARG2_DICT_PREV_LAST_CURR_FIRST)
        util.write_dict_keys_to_file(dict_curr_last_next_first, config.IMPLICIT_ARG2_DICT_CURR_LAST_NEXT_FIRST)


if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_lowercased_verbs, config.IMPLICIT_ARG2_DICT_LOWERCASE_VERBS)
    #
    Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_lemma_verbs, config.IMPLICIT_ARG2_DICT_LEMMA_VERBS)

    Dict_creator(pdtb_parse).create_term_dict()
    #
    Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_production_rule, config.IMPLICIT_ARG2_DICT_CURR_PRODUCTION_RULE)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_prev_curr_production_rule, config.IMPLICIT_ARG2_DICT_PREV_CURR_PRODUCTION_RULE)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_prev_curr_CP_production_rule, config.IMPLICIT_ARG2_DICT_PREV_CURR_CP_PRODUCTION_RULE)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_next_CP_production_rule, config.IMPLICIT_ARG2_DICT_CURR_NEXT_CP_PRODUCTION_RULE)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_2prev_pos_lemma_verb, config.IMPLICIT_ARG2_DICT_2PREV_POS_LEMMA_VERB)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_curr_first_to_prev_last_path, config.IMPLICIT_ARG2_DICT_CURR_FIRST_TO_PREV_LAST_PATH)



    # pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    #
    # for curr_index, relation in enumerate(Dict_creator(pdtb_parse).implicit_relations):
    #     for arg_clauses in dict_util.get_arg_clauses_with_label(Dict_creator(pdtb_parse).parse_dict, relation):
    #         pass

