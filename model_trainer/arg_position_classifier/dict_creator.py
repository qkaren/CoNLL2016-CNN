#coding:utf-8
import util
import config
from . import arg_position_dict_util as dict_util
from pdtb_parse import PDTB_PARSE

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        # dict[(DocID, sent_index)] = [[1], [4,5]]
        self.SS_conns_dict = pdtb_parse.pdtb.SS_conns_dict
        self.PS_conns_dict = pdtb_parse.pdtb.PS_conns_dict


    def create_all_dict(self, threshold = 1):
        print("生成所有 argument position 所需字典...")

        dict_CString = {}
        dict_CPOS = {}
        dict_prev1 = {}
        dict_prev1POS = {}
        dict_prev1_C = {}
        dict_prev1POS_CPOS = {}
        dict_prev2 = {}
        dict_prev2POS = {}
        dict_prev2_C = {}
        dict_prev2POS_CPOS = {}

        dict_next1 = {}
        dict_next1POS = {}
        dict_next1_C = {}
        dict_next1POS_CPOS = {}
        dict_next2 = {}
        dict_next2POS = {}
        dict_next2_C = {}
        dict_next2POS_CPOS = {}

        ''' Prasad '''
        dict_conn_to_root_path = {}


        position_dict_list = [self.SS_conns_dict, self.PS_conns_dict]

        for position_dict in position_dict_list:
            for DocID, sent_index in list(position_dict.keys()):
                for conn_indices in position_dict[(DocID, sent_index)]:

                    C_String = dict_util.get_C_String(self.parse_dict, DocID, sent_index, conn_indices)
                    CPOS = dict_util.get_CPOS(self.parse_dict, DocID, sent_index, conn_indices)
                    prev1 = dict_util.get_prev1(self.parse_dict, DocID, sent_index, conn_indices)
                    prev1POS = dict_util.get_prev1POS(self.parse_dict, DocID, sent_index, conn_indices)
                    prev2 = dict_util.get_prev2(self.parse_dict, DocID, sent_index, conn_indices)
                    prev2POS = dict_util.get_prev2POS(self.parse_dict, DocID, sent_index, conn_indices)

                    prev1_C = "%s|%s" % (prev1, C_String)
                    prev1POS_CPOS = "%s|%s" % (prev1POS, CPOS)

                    prev2_C = "%s|%s" % (prev2, C_String)
                    prev2POS_CPOS = "%s|%s" % (prev2POS, CPOS)

                    next1, next1POS = dict_util.get_next1_next1POS(self.parse_dict, DocID, sent_index, conn_indices)
                    next2, next2POS = dict_util.get_next2_next2POS(self.parse_dict, DocID, sent_index, conn_indices)

                    next1_C = "%s|%s" % (C_String, next1)
                    next1POS_CPOS = "%s|%s" % (CPOS, next1POS)

                    next2_C = "%s|%s" % (C_String, next2)
                    next2POS_CPOS = "%s|%s" % (CPOS, next2POS)

                    conn_to_root_path = dict_util.get_conn_to_root_path(self.parse_dict, DocID, sent_index, conn_indices)

                    util.set_dict_key_value(dict_CString, C_String)
                    util.set_dict_key_value(dict_CPOS, CPOS)
                    util.set_dict_key_value(dict_prev1, prev1)
                    util.set_dict_key_value(dict_prev1POS, prev1POS )
                    util.set_dict_key_value(dict_prev1_C, prev1_C)
                    util.set_dict_key_value(dict_prev1POS_CPOS, prev1POS_CPOS)
                    util.set_dict_key_value(dict_prev2, prev2)
                    util.set_dict_key_value(dict_prev2POS, prev2POS)
                    util.set_dict_key_value(dict_prev2_C, prev2_C)
                    util.set_dict_key_value(dict_prev2POS_CPOS, prev2POS_CPOS)

                    util.set_dict_key_value(dict_next1, next1)
                    util.set_dict_key_value(dict_next1POS, next1POS )
                    util.set_dict_key_value(dict_next1_C, next1_C)
                    util.set_dict_key_value(dict_next1POS_CPOS, next1POS_CPOS)
                    util.set_dict_key_value(dict_next2, next2)
                    util.set_dict_key_value(dict_next2POS, next2POS)
                    util.set_dict_key_value(dict_next2_C, next2_C)
                    util.set_dict_key_value(dict_next2POS_CPOS, next2POS_CPOS)

                    util.set_dict_key_value(dict_conn_to_root_path, conn_to_root_path)

        #删除频率小于threshold的键
        util.removeItemsInDict(dict_CString, threshold)
        util.removeItemsInDict(dict_CPOS, threshold)
        util.removeItemsInDict(dict_prev1, threshold)
        util.removeItemsInDict(dict_prev1POS, threshold)
        util.removeItemsInDict(dict_prev1_C, threshold)
        util.removeItemsInDict(dict_prev1POS_CPOS, threshold)
        util.removeItemsInDict(dict_prev2, threshold)
        util.removeItemsInDict(dict_prev2POS, threshold)
        util.removeItemsInDict(dict_prev2_C, threshold)
        util.removeItemsInDict(dict_prev2POS_CPOS, threshold)

        util.removeItemsInDict(dict_next1, threshold)
        util.removeItemsInDict(dict_next1POS, threshold)
        util.removeItemsInDict(dict_next1_C, threshold)
        util.removeItemsInDict(dict_next1POS_CPOS, threshold)
        util.removeItemsInDict(dict_next2, threshold)
        util.removeItemsInDict(dict_next2POS, threshold)
        util.removeItemsInDict(dict_next2_C, threshold)
        util.removeItemsInDict(dict_next2POS_CPOS, threshold)
        util.removeItemsInDict(dict_conn_to_root_path, threshold)



        #字典keys写入文件

        util.write_dict_keys_to_file(dict_CString,config.ARG_POSITION_DICT_CSTRING)
        util.write_dict_keys_to_file(dict_CPOS,config.ARG_POSITION_DICT_CPOS)
        util.write_dict_keys_to_file(dict_prev1,config.ARG_POSITION_DICT_PREV1)
        util.write_dict_keys_to_file(dict_prev1POS,config.ARG_POSITION_DICT_PREV1POS)
        util.write_dict_keys_to_file(dict_prev1_C,config.ARG_POSITION_DICT_PREV1_C)
        util.write_dict_keys_to_file(dict_prev1POS_CPOS,config.ARG_POSITION_DICT_PREV1POS_CPOS)
        util.write_dict_keys_to_file(dict_prev2,config.ARG_POSITION_DICT_PREV2)
        util.write_dict_keys_to_file(dict_prev2POS,config.ARG_POSITION_DICT_PREV2POS)
        util.write_dict_keys_to_file(dict_prev2_C,config.ARG_POSITION_DICT_PREV2_C)
        util.write_dict_keys_to_file(dict_prev2POS_CPOS,config.ARG_POSITION_DICT_PREV2POS_CPOS)

        util.write_dict_keys_to_file(dict_next1,config.ARG_POSITION_DICT_NEXT1)
        util.write_dict_keys_to_file(dict_next1POS,config.ARG_POSITION_DICT_NEXT1POS)
        util.write_dict_keys_to_file(dict_next1_C,config.ARG_POSITION_DICT_NEXT1_C)
        util.write_dict_keys_to_file(dict_next1POS_CPOS,config.ARG_POSITION_DICT_NEXT1POS_CPOS)
        util.write_dict_keys_to_file(dict_next2,config.ARG_POSITION_DICT_NEXT2)
        util.write_dict_keys_to_file(dict_next2POS,config.ARG_POSITION_DICT_NEXT2POS)
        util.write_dict_keys_to_file(dict_next2_C,config.ARG_POSITION_DICT_NEXT2_C)
        util.write_dict_keys_to_file(dict_next2POS_CPOS,config.ARG_POSITION_DICT_NEXT2POS_CPOS)

        util.write_dict_keys_to_file(dict_conn_to_root_path, config.ARG_POSITION_DICT_CONN_TO_ROOT_PATH)



if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    Dict_creator(pdtb_parse).create_all_dict()

