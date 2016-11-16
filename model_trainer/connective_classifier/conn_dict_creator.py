#coding:utf-8
import config, util
from pdtb import PDTB
from pdtb_parse import PDTB_PARSE
from syntax_tree import Syntax_tree
# from .conn_head_mapper import ConnHeadMapper
import conn_dict_util as dict_util
class ConnectiveDict:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.disc_conns_dict = self.pdtb_parse.disc_conns_dict
        self.non_disc_conns_dict = self.pdtb_parse.non_disc_conns_dict
        self.parse_dict = pdtb_parse.parse_dict

    #生成c 的POS字典。
    #读取 pdtb-parses 的文件，获取c 的 pos tag
    def create_CPOS_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                pos_tag_list = []
                for conn_index in conn_indices:
                    pos_tag_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                pos_tag = "_".join(pos_tag_list)

                if pos_tag not in dict:
                    dict[pos_tag] = 0
                dict[pos_tag] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                pos_tag_list = []
                for conn_index in conn_indices:
                    pos_tag_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                pos_tag = "_".join(pos_tag_list)
                if pos_tag not in dict:
                    dict[pos_tag] = 0
                dict[pos_tag] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict,dict_path)

    # prev + C
    def create_prev_C_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                prev_C = "%s|%s" % (prev, conn_name)
                if prev_C not in dict:
                    dict[prev_C] = 0
                dict[prev_C] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                prev_C = "%s|%s" % (prev, conn_name)
                if prev_C not in dict:
                    dict[prev_C] = 0
                dict[prev_C] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # prevPOS
    def create_prevPOS_dict(self, dict_path, threshold = 1):
        dict = {}

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]
                if prev_pos not in dict:
                    dict[prev_pos] = 0
                dict[prev_pos] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]
                if prev_pos not in dict:
                    dict[prev_pos] = 0
                dict[prev_pos] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict,dict_path)

    # prePOS + CPOS
    def create_prePOS_CPOS_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]

                pos_tag_list = []
                for conn_index in conn_indices:
                    pos_tag_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                pos_tag = "_".join(pos_tag_list)
                prePOS_CPOS = "%s|%s" % (prev_pos, pos_tag)
                if prePOS_CPOS not in dict:
                    dict[prePOS_CPOS] = 0
                dict[prePOS_CPOS] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]

                pos_tag_list = []
                for conn_index in conn_indices:
                    pos_tag_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                pos_tag = "_".join(pos_tag_list)
                prePOS_CPOS = "%s|%s" % (prev_pos, pos_tag)
                if prePOS_CPOS not in dict:
                    dict[prePOS_CPOS] = 0
                dict[prePOS_CPOS] += 1
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict,dict_path)


    #  C + next
    def create_C_next_dict(self, dict_path, threshold = 1):
        dict = {}
        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                #获取连接词到名称
                conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                C_next = "%s|%s" % (conn_name, next)
                if C_next not in dict:
                    dict[C_next] = 0
                dict[C_next] += 1

        #非语篇连接词
        for (DocID, sent_index) in list(self.non_disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                #获取连接词到名称
                conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                C_next = "%s|%s" % (conn_name, next)
                if C_next not in dict:
                    dict[C_next] = 0
                dict[C_next] += 1
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # next pos
    def create_nextPOS_dict(self, dict_path, threshold = 1):
        dict = {}
        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                # 连接词的后面一个词的pos
                ''' next pos '''
                if next == "NONE":
                    nextPOS = "NONE"
                else:
                    nextPOS = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]
                if nextPOS not in dict:
                    dict[nextPOS] = 0
                dict[nextPOS] += 1

        #非语篇连接词
        for (DocID, sent_index) in list(self.non_disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                # 连接词的后面一个词的pos
                ''' next pos '''
                if next == "NONE":
                    nextPOS = "NONE"
                else:
                    nextPOS = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]
                if nextPOS not in dict:
                    dict[nextPOS] = 0
                dict[nextPOS] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # C POS + next POS
    def create_CPOS_nextPOS_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:

                CPOS_list = []
                for conn_index in conn_indices:
                    CPOS_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                CPOS = "_".join(CPOS_list)

                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                # 连接词的后面一个词的pos
                ''' next pos '''
                if next == "NONE":
                    nextPOS = "NONE"
                else:
                    nextPOS = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]

                CPOS_nextPOS = "%s|%s" % (CPOS, nextPOS)
                if CPOS_nextPOS not in dict:
                    dict[CPOS_nextPOS] = 0
                dict[CPOS_nextPOS] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句子长度，该doc的总句子数
            sent_count = len(self.parse_dict[DocID]["sentences"])
            sent_length = len(self.parse_dict[DocID]["sentences"][sent_index]["words"])

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:

                CPOS_list = []
                for conn_index in conn_indices:
                    CPOS_list.append(self.parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
                CPOS = "_".join(CPOS_list)

                flag = 0
                next_index = conn_indices[-1] + 1
                next_sent_index = sent_index
                if next_index >= sent_length:
                    next_sent_index += 1
                    next_index = 0
                    if next_sent_index >= sent_count:
                        flag = 1
                # 连接词的后面一个词
                if flag == 1:
                    next = "NONE"
                else:
                    next = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

                # 连接词的后面一个词的pos
                ''' next pos '''
                if next == "NONE":
                    nextPOS = "NONE"
                else:
                    nextPOS = self.parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]

                CPOS_nextPOS = "%s|%s" % (CPOS, nextPOS)
                if CPOS_nextPOS not in dict:
                    dict[CPOS_nextPOS] = 0
                dict[CPOS_nextPOS] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # path of c's parent to root
    def create_CParent_to_root_path_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up
                        path += syntax_tree.get_node_path_to_root(conn_parent_node) + "&"
                    if path[-1] == "&":
                        path = path[:-1]

                if path not in dict:
                    dict[path] = 0
                dict[path] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up
                        path += syntax_tree.get_node_path_to_root(conn_parent_node) + "&"
                    if path[-1] == "&":
                        path = path[:-1]

                if path not in dict:
                    dict[path] = 0
                dict[path] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # compressed path of c's parent to root
    def create_compressed_CParent_to_root_path_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    compressed_path = "NONE_TREE"
                else:
                    compressed_path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up

                        path = syntax_tree.get_node_path_to_root(conn_parent_node)

                        compressed_path += util.get_compressed_path(path) + "&"
                if compressed_path[-1] == "&":
                    compressed_path = compressed_path[:-1]

                if compressed_path not in dict:
                    dict[compressed_path] = 0
                dict[compressed_path] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    compressed_path = "NONE_TREE"
                else:
                    compressed_path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up

                        path = syntax_tree.get_node_path_to_root(conn_parent_node)

                        compressed_path += util.get_compressed_path(path) + "&"
                if compressed_path[-1] == "&":
                    compressed_path = compressed_path[:-1]

                if compressed_path not in dict:
                    dict[compressed_path] = 0
                dict[compressed_path] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # Pitler :self_category
    def create_self_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:

                if syntax_tree.tree == None:
                    self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

                if self_category not in dict:
                    dict[self_category] = 0
                dict[self_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

                if self_category not in dict:
                    dict[self_category] = 0
                dict[self_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # Pitler :parent_category
    def create_parent_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                if parent_category not in dict:
                    dict[parent_category] = 0
                dict[parent_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                if parent_category not in dict:
                    dict[parent_category] = 0
                dict[parent_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    # Pitler : left_sibling_category
    def create_left_sibling_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    left_sibling_category = "NONE_TREE"
                else:
                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                if left_sibling_category not in dict:
                    dict[left_sibling_category] = 0
                dict[left_sibling_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    left_sibling_category = "NONE_TREE"
                else:
                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                if left_sibling_category not in dict:
                    dict[left_sibling_category] = 0
                dict[left_sibling_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    # Pitler : right_sibling_category
    def create_right_sibling_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                     right_sibling_category = "NONE_TREE"
                else:
                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name


                if right_sibling_category not in dict:
                    dict[right_sibling_category] = 0
                dict[right_sibling_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                     right_sibling_category = "NONE_TREE"
                else:
                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name


                if right_sibling_category not in dict:
                    dict[right_sibling_category] = 0
                dict[right_sibling_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    ''' conn syn interaction '''
    def create_conn_self_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name
                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_self_category = "%s|%s" % (conn_name, self_category)

                if conn_self_category not in dict:
                    dict[conn_self_category] = 0
                dict[conn_self_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name
                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_self_category = "%s|%s" % (conn_name, self_category)

                if conn_self_category not in dict:
                    dict[conn_self_category] = 0
                dict[conn_self_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    def create_conn_parent_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_parent_category = "%s|%s" % (conn_name, parent_category)

                if conn_parent_category not in dict:
                    dict[conn_parent_category] = 0
                dict[conn_parent_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_parent_category = "%s|%s" % (conn_name, parent_category)

                if conn_parent_category not in dict:
                    dict[conn_parent_category] = 0
                dict[conn_parent_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    def create_conn_left_sibling_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_left_sibling_category = "NONE_TREE"
                else:

                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)

                if conn_left_sibling_category not in dict:
                    dict[conn_left_sibling_category] = 0
                dict[conn_left_sibling_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_left_sibling_category = "NONE_TREE"
                else:

                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)

                if conn_left_sibling_category not in dict:
                    dict[conn_left_sibling_category] = 0
                dict[conn_left_sibling_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)


    def create_conn_right_sibling_category_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_right_sibling_category = "NONE_TREE"
                else:

                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

                if conn_right_sibling_category not in dict:
                    dict[conn_right_sibling_category] = 0
                dict[conn_right_sibling_category] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    conn_right_sibling_category = "NONE_TREE"
                else:

                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name

                    #获取连接词到名称
                    conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                                  for word_token in conn_indices ])

                    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

                if conn_right_sibling_category not in dict:
                    dict[conn_right_sibling_category] = 0
                dict[conn_right_sibling_category] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #self_parent
    #self_right
    #self_left
    #parent_left
    #parent_right
    #left_right
    def create_all_syn_syn_category_dict(self, threshold = 1):
        self_parent_dict = {}
        self_right_dict = {}
        self_left_dict = {}
        parent_left_dict = {}
        parent_right_dict = {}
        left_right_dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)


            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

                if syntax_tree.tree == None:
                    parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                if syntax_tree.tree == None:
                    left_sibling_category = "NONE_TREE"
                else:
                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                if syntax_tree.tree == None:
                    right_sibling_category = "NONE_TREE"
                else:
                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name

                self_parent = "%s|%s" % (self_category, parent_category)
                self_right = "%s|%s" % (self_category, right_sibling_category)
                self_left = "%s|%s" % (self_category, left_sibling_category)
                parent_left = "%s|%s" % (parent_category, left_sibling_category)
                parent_right = "%s|%s" % (parent_category, right_sibling_category)
                left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

                if self_parent not in self_parent_dict:
                    self_parent_dict[self_parent] = 0
                self_parent_dict[self_parent] += 1

                if self_right not in self_right_dict:
                    self_right_dict[self_right] = 0
                self_right_dict[self_right] += 1

                if self_left not in self_left_dict:
                    self_left_dict[self_left] = 0
                self_left_dict[self_left] += 1

                if parent_left not in parent_left_dict:
                    parent_left_dict[parent_left] = 0
                parent_left_dict[parent_left] += 1

                if parent_right not in parent_right_dict:
                    parent_right_dict[parent_right] = 0
                parent_right_dict[parent_right] += 1

                if left_right not in left_right_dict:
                    left_right_dict[left_right] = 0
                left_right_dict[left_right] += 1


        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    self_category = "NONE_TREE"
                else:
                    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

                if syntax_tree.tree == None:
                    parent_category = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    if parent_category_node == None:
                        parent_category = "ROOT"
                    else:
                        parent_category = parent_category_node.name

                if syntax_tree.tree == None:
                    left_sibling_category = "NONE_TREE"
                else:
                    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    if left_sibling_category_node == None:
                        left_sibling_category = "NONE"
                    else:
                        left_sibling_category = left_sibling_category_node.name

                if syntax_tree.tree == None:
                    right_sibling_category = "NONE_TREE"
                else:
                    right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    if right_sibling_category_node == None:
                        right_sibling_category = "NONE"
                    else:
                        right_sibling_category = right_sibling_category_node.name

                self_parent = "%s|%s" % (self_category, parent_category)
                self_right = "%s|%s" % (self_category, right_sibling_category)
                self_left = "%s|%s" % (self_category, left_sibling_category)
                parent_left = "%s|%s" % (parent_category, left_sibling_category)
                parent_right = "%s|%s" % (parent_category, right_sibling_category)
                left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

                if self_parent not in self_parent_dict:
                    self_parent_dict[self_parent] = 0
                self_parent_dict[self_parent] += 1

                if self_right not in self_right_dict:
                    self_right_dict[self_right] = 0
                self_right_dict[self_right] += 1

                if self_left not in self_left_dict:
                    self_left_dict[self_left] = 0
                self_left_dict[self_left] += 1

                if parent_left not in parent_left_dict:
                    parent_left_dict[parent_left] = 0
                parent_left_dict[parent_left] += 1

                if parent_right not in parent_right_dict:
                    parent_right_dict[parent_right] = 0
                parent_right_dict[parent_right] += 1

                if left_right not in left_right_dict:
                    left_right_dict[left_right] = 0
                left_right_dict[left_right] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(self_parent_dict, threshold)
        util.removeItemsInDict(self_right_dict, threshold)
        util.removeItemsInDict(self_left_dict, threshold)
        util.removeItemsInDict(parent_left_dict, threshold)
        util.removeItemsInDict(parent_right_dict, threshold)
        util.removeItemsInDict(left_right_dict, threshold)
        #字典keys写入文件


        self_parent_path = config.CONNECTIVE_DICT_SELF_PARENT_CATEGORY_PATH
        self_right_path = config.CONNECTIVE_DICT_SELF_RIGHT_CATEGORY_PATH
        self_left_path = config.CONNECTIVE_DICT_SELF_LEFT_CATEGORY_PATH
        parent_left_path = config.CONNECTIVE_DICT_PARENT_LEFT_CATEGORY_PATH
        parent_right_path = config.CONNECTIVE_DICT_PARENT_RIGHT_CATEGORY_PATH
        left_right_path = config.CONNECTIVE_DICT_LEFT_RIGHT_CATEGORY_PATH


        util.write_dict_keys_to_file(self_parent_dict, self_parent_path)
        util.write_dict_keys_to_file(self_right_dict, self_right_path)
        util.write_dict_keys_to_file(self_left_dict, self_left_path)
        util.write_dict_keys_to_file(parent_left_dict, parent_left_path)
        util.write_dict_keys_to_file(parent_right_dict, parent_right_path)
        util.write_dict_keys_to_file(left_right_dict, left_right_path)



    # prev + C
    def create_lower_case_C_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                lower_case_C = conn_name.lower()

                if "if the" == lower_case_C:
                    print("disc conn")
                    print((DocID, sent_index))

                if lower_case_C not in dict:
                    dict[lower_case_C] = 0
                dict[lower_case_C] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])

                lower_case_C = conn_name.lower()

                if "if the" == lower_case_C:
                    print("non-disc conn")
                    print((DocID, sent_index))

                if lower_case_C not in dict:
                    dict[lower_case_C] = 0
                dict[lower_case_C] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  C
    def create_C_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if conn_name not in dict:
                    dict[conn_name] = 0
                dict[conn_name] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if conn_name not in dict:
                    dict[conn_name] = 0
                dict[conn_name] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    # prePOS + C
    def create_prePOS_C_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]

                #获取连接词到名称
                conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])


                prePOS_C = "%s|%s" % (prev_pos, conn_name.lower())
                if prePOS_C not in dict:
                    dict[prePOS_C] = 0
                dict[prePOS_C] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                flag = 0
                prev_index = conn_indices[0] - 1
                pre_sent_index = sent_index
                if prev_index < 0:
                    pre_sent_index -= 1
                    prev_index = -1
                    if pre_sent_index < 0:
                        flag = 1
                # 连接词的前面一个词
                if flag == 1:
                    prev = "NONE"
                else:
                    prev = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
                if prev == "NONE":
                    prev_pos = "NONE"
                else:
                    prev_pos = self.parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]

                #获取连接词到名称
                conn_name = " ".join([self.parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])


                prePOS_C = "%s|%s" % (prev_pos, conn_name.lower())
                if prePOS_C not in dict:
                    dict[prePOS_C] = 0
                dict[prePOS_C] += 1
        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict,dict_path)

    # path of c's parent to root path 的所有node的names
    def create_self_category_to_root_path_dict(self,dict_path, threshold = 1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
                    path = syntax_tree.get_node_path_to_root(conn_node)

                if path not in dict:
                    dict[path] = 0
                dict[path] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
                    path = syntax_tree.get_node_path_to_root(conn_node)

                if path not in dict:
                    dict[path] = 0
                dict[path] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #   c's parent to root  node names
    def create_CParent_to_root_path_node_names_dict(self, dict_path, threshold=1):
        dict = {}

        # dict[(DocID, sent_index)] = [[1], [4,5]]

        #语篇连接词
        for DocID, sent_index in list(self.disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up
                        path += syntax_tree.get_node_path_to_root(conn_parent_node) + "-->"
                    if path[-3:] == "-->":
                        path = path[:-3]

                for t in path.split("-->"):
                    if t not in dict:
                        dict[t] = 0
                    dict[t] += 1
        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    path = "NONE_TREE"
                else:
                    path = ""
                    for conn_index in conn_indices:
                        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
                        conn_parent_node = conn_node.up
                        path += syntax_tree.get_node_path_to_root(conn_parent_node) + "-->"
                    if path[-3:] == "-->":
                        path = path[:-3]

                for t in path.split("-->"):
                    if t not in dict:
                        dict[t] = 0
                    dict[t] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其上下文
    def create_conn_connCtx_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    connCtx = "NONE_TREE"
                else:
                    conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
                    connCtx = dict_util.get_node_Ctx(conn_node, syntax_tree)

                conn_connCtx = "%s|%s" % (conn_name, connCtx)

                if conn_connCtx not in dict:
                    dict[conn_connCtx] = 0
                dict[conn_connCtx] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    connCtx = "NONE_TREE"
                else:
                    conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
                    connCtx = dict_util.get_node_Ctx(conn_node, syntax_tree)


                conn_connCtx = "%s|%s" % (conn_name, connCtx)

                if conn_connCtx not in dict:
                    dict[conn_connCtx] = 0
                dict[conn_connCtx] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其 right sibling 的上下文
    def create_conn_rightSiblingCtx_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    rightSiblingCtx = "NONE_TREE"
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

                conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

                if conn_rightSiblingCtx not in dict:
                    dict[conn_rightSiblingCtx] = 0
                dict[conn_rightSiblingCtx] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    rightSiblingCtx = "NONE_TREE"
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

                conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

                if conn_rightSiblingCtx not in dict:
                    dict[conn_rightSiblingCtx] = 0
                dict[conn_rightSiblingCtx] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其 left sibling 的上下文
    def create_conn_leftSiblingCtx_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    leftSiblingCtx = "NONE_TREE"
                else:
                    leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

                conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

                if conn_leftSiblingCtx not in dict:
                    dict[conn_leftSiblingCtx] = 0
                dict[conn_leftSiblingCtx] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    leftSiblingCtx = "NONE_TREE"
                else:
                    leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

                conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

                if conn_leftSiblingCtx not in dict:
                    dict[conn_leftSiblingCtx] = 0
                dict[conn_leftSiblingCtx] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其 left right sibling 的上下文
    def create_conn_left_right_SiblingCtx_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    leftSiblingCtx = "NONE_TREE"
                else:
                    leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

                if syntax_tree.tree == None:
                    rightSiblingCtx = "NONE_TREE"
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

                conn_left_right_SiblingCtx = "%s|%s|%s" % (conn_name, leftSiblingCtx, rightSiblingCtx)

                if conn_left_right_SiblingCtx not in dict:
                    dict[conn_left_right_SiblingCtx] = 0
                dict[conn_left_right_SiblingCtx] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    leftSiblingCtx = "NONE_TREE"
                else:
                    leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
                    leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

                if syntax_tree.tree == None:
                    rightSiblingCtx = "NONE_TREE"
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

                conn_left_right_SiblingCtx = "%s|%s|%s" % (conn_name, leftSiblingCtx, rightSiblingCtx)

                if conn_left_right_SiblingCtx not in dict:
                    dict[conn_left_right_SiblingCtx] = 0
                dict[conn_left_right_SiblingCtx] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其 parent_category 的上下文
    def create_conn_parent_category_Ctx_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    parent_categoryCtx = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    parent_categoryCtx = dict_util.get_node_linked_Ctx(parent_category_node, syntax_tree)

                conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

                if conn_parent_categoryCtx not in dict:
                    dict[conn_parent_categoryCtx] = 0
                dict[conn_parent_categoryCtx] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                #获取连接词到名称
                conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                              for word_token in conn_indices ])
                if syntax_tree.tree == None:
                    parent_categoryCtx = "NONE_TREE"
                else:
                    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
                    parent_categoryCtx = dict_util.get_node_linked_Ctx(parent_category_node, syntax_tree)

                conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

                if conn_parent_categoryCtx not in dict:
                    dict[conn_parent_categoryCtx] = 0
                dict[conn_parent_categoryCtx] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

    #  连接词，加其 right sibling 的上下文
    def create_rightSibling_production_rules_dict(self, dict_path, threshold = 1):
        dict = {}
        parse_dict = self.parse_dict

        #语篇连接词
        for (DocID, sent_index) in list(self.disc_conns_dict.keys()):
             #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.disc_conns_dict[(DocID, sent_index)]:

                if syntax_tree.tree == None:
                    rightSibling_production_rules = ["NONE_TREE"]
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSibling_production_rules = dict_util.get_node_production_rules(rightSibling_node, syntax_tree)

                for rule in rightSibling_production_rules:
                    if rule not in dict:
                        dict[rule] = 0
                    dict[rule] += 1

        #非语篇连接词
        for DocID, sent_index in list(self.non_disc_conns_dict.keys()):
            #获取该句话的语法树
            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            for conn_indices in self.non_disc_conns_dict[(DocID, sent_index)]:
                if syntax_tree.tree == None:
                    rightSibling_production_rules = ["NONE_TREE"]
                else:
                    rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
                    rightSibling_production_rules = dict_util.get_node_production_rules(rightSibling_node, syntax_tree)

                for rule in rightSibling_production_rules:
                    if rule not in dict:
                        dict[rule] = 0
                    dict[rule] += 1

        #删除频率小于threshold的键
        util.removeItemsInDict(dict, threshold)
        #字典keys写入文件
        util.write_dict_keys_to_file(dict, dict_path)

#排序后的连接词
def create_sorted_exp_conns():
    ExpConnFile = open(config.ExpConn_PATH)
    conn_list = [line.strip() for line in ExpConnFile.readlines()]

    sortedConn = []
    #1. if..then 这种类型的
    for conn in conn_list:
        if ".." in conn and conn not in sortedConn:
            sortedConn.append(conn)
    #2. 根据连接词字数降序排列
    for conn in sorted(conn_list, cmp=lambda y, x: len(x.split(" ")) - len(y.split(" "))):
        if conn not in sortedConn:
            sortedConn.append(conn)

    fout = open(config.SORTED_ExpConn_PATH, "w")
    fout.write("\n".join(sortedConn))
    fout.close()





if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # ''' 所有连接词特征所需的dict '''

    # print "cpos dict ..."
    # ConnectiveDict(pdtb_parse).create_CPOS_dict(config.CONNECTIVE_DICT_CPOS_PATH)
    #
    # print "pre + C dict ..."
    # ConnectiveDict(pdtb_parse).create_prev_C_dict(config.CONNECTIVE_DICT_PREV_C_PATH)
    #
    # print "prevPOS dic..."
    # ConnectiveDict(pdtb_parse).create_prevPOS_dict(config.CONNECTIVE_DICT_PREVPOS_PATH)
    #
    # # prePOS + CPOS
    # print "prePOS + CPOS"
    # ConnectiveDict(pdtb_parse).create_prePOS_CPOS_dict(config.CONNECTIVE_DICT_PREVPOS_CPOS_PATH)
    #
    # # C +next
    print("C +next dict...")
    ConnectiveDict(pdtb_parse).create_C_next_dict(config.CONNECTIVE_DICT_C_NEXT_PATH)
    #
    # # next POS
    # print "next pos dict..."
    # ConnectiveDict(pdtb_parse).create_nextPOS_dict(config.CONNECTIVE_DICT_NEXTPOS_PATH)
    #
    # # C POS + next POS
    # print "C POS + next POS dict..."
    # ConnectiveDict(pdtb_parse).create_CPOS_nextPOS_dict(config.CONNECTIVE_DICT_CPOS_NEXTPOS_PATH)
    #
    # # path of c's parent to root
    # print "path of c's parent to root dict"
    # ConnectiveDict(pdtb_parse).create_CParent_to_root_path_dict(config.CONNECTIVE_DICT_CPARENT_TO_ROOT_PATH)
    #
    # print "compressed path of c's parent to root dict"
    # ConnectiveDict(pdtb_parse).create_compressed_CParent_to_root_path_dict(config.CONNECTIVE_DICT_COMPRESSED_CPARENT_TO_ROOT_PATH)
    #
    # print "create_self_category_dict"
    # ConnectiveDict(pdtb_parse).create_self_category_dict(config.CONNECTIVE_DICT_SELF_CATEGORY_PATH)
    #
    # print "create_parent_category_dict..."
    # ConnectiveDict(pdtb_parse).create_parent_category_dict(config.CONNECTIVE_DICT_PARENT_CATEGORY_PATH)
    #
    # print "create_left_sibling_category_dict..."
    # ConnectiveDict(pdtb_parse).create_left_sibling_category_dict(config.CONNECTIVE_DICT_LEFT_SIBLING_CATEGORY_PATH)
    #
    # print "create_right_sibling_category_dict..."
    # ConnectiveDict(pdtb_parse).create_right_sibling_category_dict(config.CONNECTIVE_DICT_RIGHT_SIBLING_CATEGORY_PATH)
    #
    # print "create_conn_self_category_dict..."
    # ConnectiveDict(pdtb_parse).create_conn_self_category_dict(config.CONNECTIVE_DICT_CONN_SELF_CATEGORY_PATH)
    #
    # print "create_conn_parent_category_dict..."
    # ConnectiveDict(pdtb_parse).create_conn_parent_category_dict(config.CONNECTIVE_DICT_CONN_PARENT_CATEGORY_PATH)
    #
    # print "create_conn_left_sibling_category_dict..."
    # ConnectiveDict(pdtb_parse).create_conn_left_sibling_category_dict(config.CONNECTIVE_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH)
    #
    # print "create_conn_right_sibling_category_dict..."
    # ConnectiveDict(pdtb_parse).create_conn_right_sibling_category_dict(config.CONNECTIVE_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH)
    #
    # print "create_all_syn_syn_category_dict..."
    # ConnectiveDict(pdtb_parse).create_all_syn_syn_category_dict()
    #
    # # ''' mine '''
    # print "conn_lower_case dict ..."
    # ConnectiveDict(pdtb_parse).create_lower_case_C_dict(config.CONNECTIVE_DICT_CONN_LOWER_CASE)

    # print "conn_ dict ..."
    # ConnectiveDict(pdtb_parse).create_C_dict(config.CONNECTIVE_DICT_CONN)

    # print "prev POS + C"
    # ConnectiveDict(pdtb_parse).create_prePOS_C_dict(config.CONNECTIVE_DICT_PREVPOS_C)

    # print "create_CParent_to_root_path_node_names_dict"
    # ConnectiveDict(pdtb_parse).create_conn_connCtx_dict(config.CONNECTIVE_DICT_CONN_CONNCTX)

    # print "create_conn_rightSiblingCtx_dict"
    # ConnectiveDict(pdtb_parse).create_conn_rightSiblingCtx_dict(config.CONNECTIVE_DICT_CONN_RIGHTSIBLINGCTX)

    # print "create_conn_leftSiblingCtx_dict"
    # ConnectiveDict(pdtb_parse).create_conn_leftSiblingCtx_dict(config.CONNECTIVE_DICT_CONN_LEFTSIBLINGCTX)

    # print "create_conn_parent_category_Ctx_dict"
    # ConnectiveDict(pdtb_parse).create_conn_parent_category_Ctx_dict(config.CONNECTIVE_DICT_CONN_PARENT_CATEGORY_CTX)

    # print "create_rightSibling_production_rules_dict"
    # ConnectiveDict(pdtb_parse).create_rightSibling_production_rules_dict(config.CONNECTIVE_DICT_CONN_RIGHTSIBLING_PRODUCTION_RULES)




