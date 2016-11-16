#coding:utf-8
import util
import config
from . import exp_dict_util as dict_util
from pdtb_parse import PDTB_PARSE
from connective import Connective
from syntax_tree import Syntax_tree

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        self.conns_list = self.pdtb_parse.pdtb.conns_list

    def create_all_dict(self, threshold = 1):

        print("生成所有 explicit classifier 所需字典...")

        dict_CString = {}
        dict_CPOS = {}
        dict_C_Prev = {}
        dict_CLString = {}
        #pitler
        '''Pitler'''
        dict_self_category = {}
        dict_parent_category = {}
        dict_left_sibling_category = {}
        dict_right_sibling_category = {}
        ''' conn_syn '''
        dict_conn_self_category = {}
        dict_conn_parent_category = {}
        dict_conn_left_sibling_category = {}
        dict_conn_right_sibling_category = {}
        ''' syn-syn '''
        self_parent_dict = {}
        self_right_dict = {}
        self_left_dict = {}
        parent_left_dict = {}
        parent_right_dict = {}
        left_right_dict = {}



        for connective in self.conns_list:
            #获取该句话的语法树
            DocID = connective.DocID
            sent_index = connective.sent_index
            conn_indices = connective.token_indices

            #特征值
            CString = dict_util.get_C_String(self.parse_dict, DocID, sent_index, conn_indices)
            CPOS = dict_util.get_CPOS(self.parse_dict, DocID, sent_index, conn_indices)
            prev = dict_util.get_prev1(self.parse_dict, DocID, sent_index, conn_indices)
            C_Prev = "%s|%s" % (CString, prev)

            CLString = CString.lower()

            #语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)
            #pitler
            self_category = dict_util.get_self_category(syntax_tree, conn_indices)
            parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
            left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)
            right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)
            #conn - syn
            conn_name = CLString
            conn_self_category = "%s|%s" % (conn_name, self_category)
            conn_parent_category = "%s|%s" % (conn_name, parent_category)
            conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)
            conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

            # syn - syn
            self_parent = "%s|%s" % (self_category, parent_category)
            self_right = "%s|%s" % (self_category, right_sibling_category)
            self_left = "%s|%s" % (self_category, left_sibling_category)
            parent_left = "%s|%s" % (parent_category, left_sibling_category)
            parent_right = "%s|%s" % (parent_category, right_sibling_category)
            left_right = "%s|%s" % (left_sibling_category, right_sibling_category)



            #写入字典
            util.set_dict_key_value(dict_CString, CString)
            util.set_dict_key_value(dict_CPOS, CPOS)
            util.set_dict_key_value(dict_C_Prev, C_Prev)
            util.set_dict_key_value(dict_CLString, CLString)

            #pitler
            util.set_dict_key_value(dict_self_category, self_category)
            util.set_dict_key_value(dict_parent_category, parent_category)
            util.set_dict_key_value(dict_left_sibling_category, left_sibling_category)
            util.set_dict_key_value(dict_right_sibling_category, right_sibling_category)
            #syn-conn
            util.set_dict_key_value(dict_conn_self_category, conn_self_category)
            util.set_dict_key_value(dict_conn_parent_category, conn_parent_category)
            util.set_dict_key_value(dict_conn_left_sibling_category, conn_left_sibling_category)
            util.set_dict_key_value(dict_conn_right_sibling_category, conn_right_sibling_category)
            #syn - syn
            util.set_dict_key_value(self_parent_dict, self_parent)
            util.set_dict_key_value(self_right_dict, self_right)
            util.set_dict_key_value(self_left_dict, self_left)
            util.set_dict_key_value(parent_left_dict, parent_left)
            util.set_dict_key_value(parent_right_dict, parent_right)
            util.set_dict_key_value(left_right_dict, left_right)




         #删除频率小于threshold的键
        util.removeItemsInDict(dict_CString, threshold)
        util.removeItemsInDict(dict_CPOS, threshold)
        util.removeItemsInDict(dict_C_Prev, threshold)
        util.removeItemsInDict(dict_CLString, threshold)
        #pitler
        util.removeItemsInDict(dict_self_category, threshold)
        util.removeItemsInDict(dict_parent_category, threshold)
        util.removeItemsInDict(dict_left_sibling_category, threshold)
        util.removeItemsInDict(dict_right_sibling_category, threshold)
        #syn-conn
        util.removeItemsInDict(dict_conn_self_category, threshold)
        util.removeItemsInDict(dict_conn_parent_category, threshold)
        util.removeItemsInDict(dict_conn_left_sibling_category, threshold)
        util.removeItemsInDict(dict_conn_right_sibling_category, threshold)




        #字典keys写入文件


        util.write_dict_keys_to_file(dict_CString, config.EXPLICIT_DICT_CSTRING)
        util.write_dict_keys_to_file(dict_CPOS, config.EXPLICIT_DICT_CPOS)
        util.write_dict_keys_to_file(dict_C_Prev, config.EXPLICIT_DICT_C_PREV)
        util.write_dict_keys_to_file(dict_CLString, config.EXPLICIT_DICT_CLSTRING)



        util.write_dict_keys_to_file(dict_self_category, config.EXPLICIT_DICT_SELF_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_parent_category, config.EXPLICIT_DICT_PARENT_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_left_sibling_category, config.EXPLICIT_DICT_LEFT_SIBLING_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_right_sibling_category, config.EXPLICIT_DICT_RIGHT_SIBLING_CATEGORY_PATH)

        util.write_dict_keys_to_file(dict_conn_self_category, config.EXPLICIT_DICT_CONN_SELF_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_conn_parent_category, config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_conn_left_sibling_category, config.EXPLICIT_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH)
        util.write_dict_keys_to_file(dict_conn_right_sibling_category, config.EXPLICIT_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH)


        util.write_dict_keys_to_file(self_parent_dict, config.EXPLICIT_DICT_SELF_PARENT_CATEGORY_PATH)
        util.write_dict_keys_to_file(self_right_dict, config.EXPLICIT_DICT_SELF_RIGHT_CATEGORY_PATH)
        util.write_dict_keys_to_file(self_left_dict, config.EXPLICIT_DICT_SELF_LEFT_CATEGORY_PATH)
        util.write_dict_keys_to_file(parent_left_dict, config.EXPLICIT_DICT_PARENT_LEFT_CATEGORY_PATH)
        util.write_dict_keys_to_file(parent_right_dict, config.EXPLICIT_DICT_PARENT_RIGHT_CATEGORY_PATH)
        util.write_dict_keys_to_file(left_right_dict, config.EXPLICIT_DICT_LEFT_RIGHT_CATEGORY_PATH)


    def create_dict(self, dict_function, dict_path, threshold = 1):

        print("生成 %s 的字典..." % (dict_function.__name__.replace("get_", "")))
        dict = {}
        total = float(len(self.conns_list))
        for curr_index, connective in enumerate(self.conns_list):
            print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')
            #获取该句话的语法树
            DocID = connective.DocID
            sent_index = connective.sent_index
            conn_indices = connective.token_indices

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


if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    # Dict_creator(pdtb_parse).create_all_dict()

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_to_root_path, config.EXPLICIT_DICT_CONN_TO_ROOT_PATH)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_next, config.EXPLICIT_DICT_CONN_NEXT)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_connCtx, config.EXPLICIT_DICT_CONN_CONNCTX)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_rightSiblingCtx, config.EXPLICIT_DICT_CONN_RIGHTSIBLINGCTX)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_parent_category_Ctx, config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_CTX)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_CParent_to_root_path_node_names, config.EXPLICIT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_parent_category_not_linked_Ctx, config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_NOT_LINKED_CTX)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_conn_prev_conn, config.EXPLICIT_DICT_CONN_PREV_CONN)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_prev_conn, config.EXPLICIT_DICT_PREV_CONN)

    Dict_creator(pdtb_parse).create_dict(dict_util.get_as_prev_conn, config.EXPLICIT_DICT_AS_PREV_CONN)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_as_prev_connPOS, config.EXPLICIT_DICT_AS_PREV_CONNPOS)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_when_prev_conn, config.EXPLICIT_DICT_WHEN_PREV_CONN)
    #
    # Dict_creator(pdtb_parse).create_dict(dict_util.get_when_prev_connPOS, config.EXPLICIT_DICT_WHEN_PREV_CONNPOS)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_as_before_after_tense, config.EXPLICIT_DICT_AS_BEFORE_AFTER_TENSE)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_when_before_after_tense, config.EXPLICIT_DICT_WHEN_BEFORE_AFTER_TENSE)

    # Dict_creator(pdtb_parse).create_dict(dict_util.get_when_after_lemma_verbs, config.EXPLICIT_DICT_WHEN_AFTER_LEMMA_VERBS)







