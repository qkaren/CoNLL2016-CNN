#coding:utf-8
import util
import config
from . import NT_dict_util as dict_util
from pdtb_parse import PDTB_PARSE
from connective import Connective
from syntax_tree import Syntax_tree

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        # dict[(DocID, sent_index)] = [[1], [4,5]]
        self.one_SS_conns_not_parallel =self.pdtb_parse.pdtb.one_SS_conns_not_parallel
        self.one_SS_conns_parallel =self.pdtb_parse.pdtb.one_SS_conns_parallel

    def create_all_dict(self, threshold = 1):

        print("生成所有 argument extractor 所需字典...")

        dict_CON_Str = {}
        dict_CON_LStr = {}
        dict_NT_Ctx = {}
        dict_CON_NT_Path = {}
        dict_CON_NT_Path_iLsib = {}
        dict_NT_prev_curr_Path = {}

        dict_CON_POS = {}
        dict_C_Prev = {}
        dict_NT_Name = {}
        dict_NT_prev_curr_production_rule = {}

        ''' mine '''
        dict_NT_NTparent_Ctx = {}


        total = float(len(self.one_SS_conns_not_parallel))

        for curr_index, connective in enumerate(self.one_SS_conns_not_parallel):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

            constituents = dict_util.get_constituents_with_label(self.parse_dict, connective)
            constituents = sorted(constituents, key=lambda constituent: constituent.indices[0])   # sort by age
            #为每一个constituent抽取特征
            for i, constituent in enumerate(constituents):

                syntax_tree = constituent.syntax_tree
                if syntax_tree.tree == None:
                    continue

                connective = constituent.connective
                conn_indices = connective.token_indices
                DocID = connective.DocID
                sent_index = connective.sent_index
                conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

                CON_Str = dict_util.get_CON_Str(self.parse_dict, DocID, sent_index, conn_indices)
                CON_LStr = CON_Str.lower()

                CON_iLSib = dict_util.get_CON_iLSib(syntax_tree,conn_node)
                NT_Ctx = dict_util.get_NT_Ctx(constituent)
                CON_NT_Path = dict_util.get_CON_NT_Path(conn_node, constituent)
                if CON_iLSib > 1:
                    CON_NT_Path_iLsib = CON_NT_Path + ":>1"
                else:
                    CON_NT_Path_iLsib = CON_NT_Path + ":<=1"

                # # 两个相邻的 NT - NT 的PATH
                # NT_prev_curr_Path = dict_util.get_NT_prev_curr_Path(i, constituents)
                # # 两个相邻的 NT - NT 的 production rule
                # NT_prev_curr_production_rule = dict_util.get_NT_prev_curr_production_rule(i, constituents)

                CON_POS = dict_util.get_CON_POS(self.parse_dict, DocID, sent_index, conn_indices)

                prev = dict_util.get_prev1(self.parse_dict, DocID, sent_index, conn_indices)
                C_Prev = "%s|%s" % (CON_Str, prev)

                NT_Name = constituent.node.name

                ''' mine '''
                NT_NTparent_Ctx = dict_util.get_NT_NTparent_Ctx(constituent)


                # prev_last, curr_first, curr_last, next_first = dict_util.get_NT_prev_curr_next()

                util.set_dict_key_value(dict_CON_Str, CON_Str)
                util.set_dict_key_value(dict_CON_LStr, CON_LStr)
                util.set_dict_key_value(dict_NT_Ctx, NT_Ctx)
                util.set_dict_key_value(dict_CON_NT_Path, CON_NT_Path)
                util.set_dict_key_value(dict_CON_NT_Path_iLsib, CON_NT_Path_iLsib)

                # util.set_dict_key_value(dict_NT_prev_curr_Path, NT_prev_curr_Path)
                # util.set_dict_key_value(dict_NT_prev_curr_production_rule, NT_prev_curr_production_rule)

                util.set_dict_key_value(dict_CON_POS, CON_POS)
                util.set_dict_key_value(dict_C_Prev, C_Prev)
                util.set_dict_key_value(dict_NT_Name, NT_Name)

                ''' mine '''
                util.set_dict_key_value(dict_NT_NTparent_Ctx, NT_NTparent_Ctx)





         #删除频率小于threshold的键
        util.removeItemsInDict(dict_CON_Str, threshold)
        util.removeItemsInDict(dict_CON_LStr, threshold)
        util.removeItemsInDict(dict_NT_Ctx, threshold)
        util.removeItemsInDict(dict_CON_NT_Path, threshold)
        util.removeItemsInDict(dict_CON_NT_Path_iLsib, threshold)

        util.removeItemsInDict(dict_NT_prev_curr_Path, threshold)
        util.removeItemsInDict(dict_CON_POS, threshold)
        util.removeItemsInDict(dict_C_Prev, threshold)



        #字典keys写入文件

        util.write_dict_keys_to_file(dict_CON_Str, config.NT_DICT_CON_Str)
        util.write_dict_keys_to_file(dict_CON_LStr, config.NT_DICT_CON_LStr)
        util.write_dict_keys_to_file(dict_NT_Ctx, config.NT_DICT_NT_Ctx)
        util.write_dict_keys_to_file(dict_CON_NT_Path, config.NT_DICT_CON_NT_Path)
        util.write_dict_keys_to_file(dict_CON_NT_Path_iLsib, config.NT_DICT_CON_NT_Path_iLsib)

        util.write_dict_keys_to_file(dict_NT_prev_curr_Path, config.NT_DICT_PREV_CURR_PATH)
        util.write_dict_keys_to_file(dict_CON_POS, config.NT_DICT_CON_POS)
        util.write_dict_keys_to_file(dict_C_Prev, config.NT_DICT_C_PREV)
        util.write_dict_keys_to_file(dict_NT_Name, config.NT_DICT_NT_NAME)

        # util.write_dict_keys_to_file(dict_NT_prev_curr_production_rule, config.NT_DICT_NT_PREV_CURR_PRODUCTION_RULE)
        ''' mine '''
        util.write_dict_keys_to_file(dict_NT_NTparent_Ctx, config.NT_DICT_NT_NTPARENT_CTX)


    def create_conn_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))
        dict = {}
        total = float(len(self.one_SS_conns_not_parallel))

        for curr_index, connective in enumerate(self.one_SS_conns_not_parallel):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

            constituents = dict_util.get_constituents_with_label(self.parse_dict, connective)
            constituents = sorted(constituents, key=lambda constituent: constituent.indices[0])   # sort by age
            #为每一个constituent抽取特征
            for i, constituent in enumerate(constituents):

                connective = constituent.connective
                conn_indices = connective.token_indices
                DocID = connective.DocID
                sent_index = connective.sent_index

                result = dict_function(self.parse_dict, DocID, sent_index, conn_indices)

                if type(result) == list:
                    for item in result:
                        util.set_dict_key_value(dict, item)
                else:
                    util.set_dict_key_value(dict, result)
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    def create_NT_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))
        dict = {}
        total = float(len(self.one_SS_conns_not_parallel))

        for curr_index, connective in enumerate(self.one_SS_conns_not_parallel):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

            constituents = dict_util.get_constituents_with_label(self.parse_dict, connective)
            constituents = sorted(constituents, key=lambda constituent: constituent.indices[0])   # sort by age
            #为每一个constituent抽取特征
            for i, constituent in enumerate(constituents):

                result = dict_function(constituent)

                if type(result) == list:
                    for item in result:
                        util.set_dict_key_value(dict, item)
                else:
                    util.set_dict_key_value(dict, result)
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    Dict_creator(pdtb_parse).create_all_dict()

    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_CParent_to_root_path, config.NT_DICT_CPARENT_TO_ROOT_PATH)

    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_CParent_to_root_path_node_names, config.NT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)
    #
    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_conn_connCtx, config.NT_DICT_CONN_CONNCTX)

    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_conn_parent_categoryCtx, config.NT_DICT_CONN_PARENT_CATEGORYCTX)
    #
    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_conn_rightSiblingCtx, config.NT_DICT_CONN_RIGHTSIBLINGCTX)
    #
    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_self_category, config.NT_DICT_SELF_CATEGORY)

    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_parent_category, config.NT_DICT_PARENT_CATEGORY)
    #
    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_left_sibling_category, config.NT_DICT_LEFT_SIBLING_CATEGORY)
    #
    # Dict_creator(pdtb_parse).create_conn_dict(dict_util.get_right_sibling_category, config.NT_DICT_RIGHT_SIBLING_CATEGORY)

    Dict_creator(pdtb_parse).create_NT_dict(dict_util.get_NT_Linked_ctx, config.NT_DICT_NT_LINKED_CTX)

    Dict_creator(pdtb_parse).create_NT_dict(dict_util.get_NT_to_root_path, config.NT_DICT_NT_TO_ROOT_PATH)

    Dict_creator(pdtb_parse).create_NT_dict(dict_util.get_NT_parent_linked_ctx, config.NT_DICT_NT_PARENT_LINKED_CTX)


