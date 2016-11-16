#coding:utf-8

from feature import Feature
from connective_dict import Connectives_dict
from syntax_tree import Syntax_tree
import util
import conn_dict_util as dict_util
from conn_head_mapper import ConnHeadMapper

def _all_features(parse_dict, DocID, sent_index, conn_indices):
    feature_function_list = [
        # '''Z.Lin'''
        CPOS,
        prev_C,
        prevPOS,
        prevPOS_CPOS,
        C_next,
        nextPOS,
        CPOS_nextPOS,
        CParent_to_root_path,
        compressed_CParent_to_root_path,

        # Pitler
        self_category,
        parent_category,
        left_sibling_category,
        right_sibling_category,
        is_right_sibling_contains_VP,
        # conn - syn
        conn_self_category,
        conn_parent_category,
        conn_left_sibling_category,
        conn_right_sibling_category,
        # syn - syn
        self_parent,
        self_right,
        self_left,
        parent_left,
        parent_right,
        left_right,

        # mine
        conn_lower_case,
        conn,
        CParent_to_root_path_node_names,
        conn_connCtx,
        conn_rightSiblingCtx,
        conn_parent_category_Ctx
    ]

    features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]
    #合并特征
    feature = util.mergeFeatures(features)
    return feature

def CPOS(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_cpos = Connectives_dict().cpos_dict
    # feature
    CPOS = dict_util.get_CPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_cpos, CPOS)

def prev_C(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    prev_C_dict = Connectives_dict().prev_C_dict
    # feature
    prev_C = dict_util.get_prev_C(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(prev_C_dict, prev_C)

def prevPOS(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    prevPOS_dict = Connectives_dict().prevPOS_dict
    # feature
    prevPOS = dict_util.get_prevPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(prevPOS_dict, prevPOS)

def prevPOS_CPOS(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    prevPOS_CPOS_dict = Connectives_dict().prevPOS_CPOS_dict
    # feature
    prevPOS_CPOS = dict_util.get_prePOS_CPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(prevPOS_CPOS_dict, prevPOS_CPOS)

def C_next(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    C_next_dict = Connectives_dict().C_next_dict
    # feature
    C_next = dict_util.get_C_next(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(C_next_dict, C_next)

def nextPOS(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    nextPOS_dict = Connectives_dict().nextPOS_dict
    # feature
    nextPOS = dict_util.get_nextPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(nextPOS_dict, nextPOS)

def CPOS_nextPOS(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    CPOS_nextPOS_dict = Connectives_dict().CPOS_nextPOS_dict
    # feature
    CPOS_nextPOS = dict_util.get_CPOS_nextPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(CPOS_nextPOS_dict, CPOS_nextPOS)

def CParent_to_root_path(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    CParent_to_root_path_dict = Connectives_dict().CParent_to_root_path_dict
    # feature
    CParent_to_root_path = dict_util.get_CParent_to_root_path(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(CParent_to_root_path_dict, CParent_to_root_path)

def compressed_CParent_to_root_path(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    compressed_CParent_to_root_path_dict = Connectives_dict().compressed_CParent_to_root_path_dict
    # feature
    compressed_CParent_to_root_path = dict_util.get_compressed_cparent_to_root_path(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(compressed_CParent_to_root_path_dict, compressed_CParent_to_root_path)

def self_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    self_category_dict = Connectives_dict().self_category_dict
    # feature
    self_category = dict_util.get_self_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(self_category_dict, self_category)

def parent_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    parent_category_dict = Connectives_dict().parent_category_dict
    # feature
    parent_category = dict_util.get_parent_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(parent_category_dict, parent_category)

def left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    left_sibling_category_dict = Connectives_dict().left_sibling_category_dict
    # feature
    left_sibling_category = dict_util.get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(left_sibling_category_dict, left_sibling_category)

def right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    right_sibling_category_dict = Connectives_dict().right_sibling_category_dict
    # feature
    right_sibling_category = dict_util.get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(right_sibling_category_dict, right_sibling_category)

def conn_self_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    conn_self_category_dict = Connectives_dict().conn_self_category_dict
    # feature
    conn_self_category = dict_util.get_conn_self_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(conn_self_category_dict, conn_self_category)

def conn_parent_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    conn_parent_category_dict = Connectives_dict().conn_parent_category_dict
    # feature
    conn_parent_category = dict_util.get_conn_parent_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(conn_parent_category_dict, conn_parent_category)

def conn_left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    conn_left_sibling_category_dict = Connectives_dict().conn_left_sibling_category_dict
    # feature
    conn_left_sibling_category = dict_util.get_conn_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(conn_left_sibling_category_dict, conn_left_sibling_category)

def conn_right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    conn_right_sibling_category_dict = Connectives_dict().conn_right_sibling_category_dict
    # feature
    conn_right_sibling_category = dict_util.get_conn_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(conn_right_sibling_category_dict, conn_right_sibling_category)

def self_parent(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    self_parent_dict = Connectives_dict().self_parent_dict
    # feature
    self_parent = dict_util.get_self_parent(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(self_parent_dict, self_parent)

def self_right(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    self_right_dict = Connectives_dict().self_right_dict
    # feature
    self_right = dict_util.get_self_right(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(self_right_dict, self_right)

def self_left(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    self_left_dict = Connectives_dict().self_left_dict
    # feature
    self_left = dict_util.get_self_left(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(self_left_dict, self_left)

def parent_left(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    parent_left_dict = Connectives_dict().parent_left_dict
    # feature
    parent_left = dict_util.get_parent_left(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(parent_left_dict, parent_left)

def parent_right(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    parent_right_dict = Connectives_dict().parent_right_dict
    # feature
    parent_right = dict_util.get_parent_right(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(parent_right_dict, parent_right)

def left_right(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    left_right_dict = Connectives_dict().left_right_dict
    # feature
    left_right = dict_util.get_left_right(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(left_right_dict, left_right)

def conn_lower_case(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_conn_lower_case = Connectives_dict().dict_conn_lower_case
    # feature
    conn_lower_case = dict_util.get_conn_lower_case(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_lower_case, conn_lower_case)

def conn(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_conn = Connectives_dict().dict_conn
    # feature
    conn = dict_util.get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn, conn)


def CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_CParent_to_root_path_node_names = Connectives_dict().dict_CParent_to_root_path_node_names
    # feature
    CParent_to_root_path_node_names = dict_util.get_CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat_list(dict_CParent_to_root_path_node_names, CParent_to_root_path_node_names)

def conn_connCtx(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_conn_connCtx = Connectives_dict().dict_conn_connCtx
    # feature
    conn_connCtx = dict_util.get_conn_connCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_connCtx, conn_connCtx)

def conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_conn_rightSiblingCtx = Connectives_dict().dict_conn_rightSiblingCtx
    # feature
    conn_rightSiblingCtx = dict_util.get_conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_rightSiblingCtx, conn_rightSiblingCtx)

def conn_parent_category_Ctx (parse_dict, DocID, sent_index, conn_indices):
    #load dict
    dict_conn_parent_category_Ctx = Connectives_dict().dict_conn_parent_category_Ctx
    # feature
    conn_parent_category_Ctx  = dict_util.get_conn_parent_categoryCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_parent_category_Ctx, conn_parent_category_Ctx)


def is_right_sibling_contains_VP(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree != None:
        right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)

    feat_dict_is_right_sibling_contains_VP = {}
    if syntax_tree.tree != None and right_sibling_category_node != None:
        T = right_sibling_category_node.get_descendants()
        T.append(right_sibling_category_node)
        for node in T:
            if node.name == "VP" or node.name == "S":
                feat_dict_is_right_sibling_contains_VP[1] = 1
                break

    return Feature("", 1, feat_dict_is_right_sibling_contains_VP)

def syn_syn_category_feature(parse_dict, DocID, sent_index, conn_indices):
    #feature dict
    feat_dict_self_parent = {}
    feat_dict_self_right = {}
    feat_dict_self_left = {}
    feat_dict_parent_left = {}
    feat_dict_parent_right = {}
    feat_dict_left_right = {}

    #load dict
    self_parent_dict = Connectives_dict().get_self_parent_dict()
    self_right_dict = Connectives_dict().get_self_right_dict()
    self_left_dict = Connectives_dict().get_self_left_dict()
    parent_left_dict = Connectives_dict().get_parent_left_dict()
    parent_right_dict = Connectives_dict().get_parent_right_dict()
    left_right_dict = Connectives_dict().get_left_right_dict()

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        length = len(self_parent_dict) + len(self_right_dict) + len(self_left_dict) \
                + len(parent_left_dict) + len(parent_right_dict) +len(left_right_dict)
        return Feature("NONE",length, {})


    self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name
    parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
    if parent_category_node == None:
        parent_category = "ROOT"
    else:
        parent_category = parent_category_node.name

    left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
    if left_sibling_category_node == None:
        left_sibling_category = "NONE"
    else:
        left_sibling_category = left_sibling_category_node.name

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

    features = []
    features.append(get_feature(feat_dict_self_parent, self_parent_dict, self_parent))
    features.append(get_feature(feat_dict_self_right,self_right_dict, self_right ))
    features.append(get_feature(feat_dict_self_left, self_left_dict, self_left))
    features.append(get_feature(feat_dict_parent_left, parent_left_dict, parent_left))
    features.append(get_feature(feat_dict_parent_right, parent_right_dict, parent_right))
    features.append(get_feature(feat_dict_left_right,left_right_dict, left_right))


    return util.mergeFeatures(features)


def all_features(parse_dict, DocID, sent_index, conn_indices):
    # feat dict
    '''Z.Lin'''
    feat_dict_CPOS_dict = {}
    feat_dict_prev_C_dict = {}
    feat_dict_prevPOS_dict = {}
    feat_dict_prevPOS_CPOS_dict = {}
    feat_dict_C_next_dict = {}
    feat_dict_nextPOS_dict = {}
    feat_dict_CPOS_nextPOS_dict = {}
    feat_dict_CParent_to_root_path_dict = {}
    feat_dict_compressed_CParent_to_root_path_dict = {}

    '''Pitler'''
    feat_dict_self_category_dict = {}
    feat_dict_parent_category_dict = {}
    feat_dict_left_sibling_category_dict = {}
    feat_dict_right_sibling_category_dict = {}
    ''' conn_syn '''
    feat_dict_conn_self_category_dict = {}
    feat_dict_conn_parent_category_dict = {}
    feat_dict_conn_left_sibling_category_dict = {}
    feat_dict_conn_right_sibling_category_dict = {}
    ''' syn_syn '''
    feat_dict_self_parent = {}
    feat_dict_self_right = {}
    feat_dict_self_left = {}
    feat_dict_parent_left = {}
    feat_dict_parent_right = {}
    feat_dict_left_right = {}

    #dict
    '''Z.Lin'''
    CPOS_dict = Connectives_dict().cpos_dict
    prev_C_dict = Connectives_dict().prev_C_dict
    prevPOS_dict = Connectives_dict().prevPOS_dict
    prevPOS_CPOS_dict = Connectives_dict().prevPOS_CPOS_dict
    C_next_dict = Connectives_dict().C_next_dict
    nextPOS_dict = Connectives_dict().nextPOS_dict
    CPOS_nextPOS_dict = Connectives_dict().CPOS_nextPOS_dict
    CParent_to_root_path_dict = Connectives_dict().CParent_to_root_path_dict
    compressed_CParent_to_root_path_dict = Connectives_dict().compressed_CParent_to_root_path_dict

    '''Pitler'''
    self_category_dict = Connectives_dict().self_category_dict
    parent_category_dict = Connectives_dict().parent_category_dict
    left_sibling_category_dict = Connectives_dict().left_sibling_category_dict
    right_sibling_category_dict = Connectives_dict().right_sibling_category_dict
    ''' conn_syn '''
    conn_self_category_dict = Connectives_dict().conn_self_category_dict
    conn_parent_category_dict = Connectives_dict().conn_parent_category_dict
    conn_left_sibling_category_dict = Connectives_dict().conn_left_sibling_category_dict
    conn_right_sibling_category_dict = Connectives_dict().conn_right_sibling_category_dict
    ''' syn_syn '''
    self_parent_dict = Connectives_dict().self_parent_dict
    self_right_dict = Connectives_dict().self_right_dict
    self_left_dict = Connectives_dict().self_left_dict
    parent_left_dict = Connectives_dict().parent_left_dict
    parent_right_dict = Connectives_dict().parent_right_dict
    left_right_dict = Connectives_dict().left_right_dict

    ''' mine '''
    dict_conn_lower_case = Connectives_dict().dict_conn_lower_case
    dict_conn = Connectives_dict().dict_conn
    # dict_prevPOS_C = Connectives_dict().dict_prevPOS_C
    # dict_self_category_to_root_path = Connectives_dict().dict_self_category_to_root_path
    dict_CParent_to_root_path_node_names = Connectives_dict().dict_CParent_to_root_path_node_names
    dict_conn_connCtx = Connectives_dict().dict_conn_connCtx
    dict_conn_rightSiblingCtx = Connectives_dict().dict_conn_rightSiblingCtx
    # dict_conn_leftSiblingCtx = Connectives_dict().dict_conn_leftSiblingCtx
    # dict_conn_left_right_SiblingCtx = Connectives_dict().dict_conn_left_right_SiblingCtx
    dict_conn_parent_category_Ctx = Connectives_dict().dict_conn_parent_category_Ctx
    dict_rightSibling_production_rules = Connectives_dict().dict_rightSibling_production_rules

    ''' c pos '''
    pos_tag_list = []
    for conn_index in conn_indices:
        pos_tag_list.append(parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
    CPOS = "_".join(pos_tag_list)

    ''' prev '''
    flag = 0
    prev_index = conn_indices[0] - 1
    prev_sent_index = sent_index
    if prev_index < 0:
        prev_index = -1
        prev_sent_index -= 1
        if prev_sent_index < 0:
            flag = 1
    # 连接词的前面一个词
    if flag == 1 :
        prev = "NONE"
    else:
        prev = parse_dict[DocID]["sentences"][prev_sent_index]["words"][prev_index][0]

    ''' conn_name '''
    #获取连接词到名称
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])

    '''prevPOS'''
    if prev == "NONE":
        prevPOS = "NONE"
    else:
        prevPOS = parse_dict[DocID]["sentences"][prev_sent_index]["words"][prev_index][1]["PartOfSpeech"]

    '''next'''
    #获取该句子长度，该doc的总句子数
    sent_count = len(parse_dict[DocID]["sentences"])
    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

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
        next = parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

    ''' next pos '''
    if next == "NONE":
        nextPOS = "NONE"
    else:
        nextPOS = parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]


    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)


    ''' c parent to root '''
    if syntax_tree.tree == None:
        cparent_to_root_path = "NONE_TREE"
    else:
        cparent_to_root_path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up
            cparent_to_root_path += syntax_tree.get_node_path_to_root(conn_parent_node) + "&"
        if cparent_to_root_path[-1] == "&":
            cparent_to_root_path = cparent_to_root_path[:-1]

    ''' compressed c parent to root '''
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

    ''' Pitler '''
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


    prev_C = "%s|%s" % (prev, conn_name)
    prePOS_CPOS = "%s|%s" % (prevPOS, CPOS)
    C_next = "%s|%s" % (conn_name, next)
    CPOS_nextPOS = "%s|%s" % (CPOS, nextPOS)

    conn_self_category = "%s|%s" % (conn_name, self_category)
    conn_parent_category = "%s|%s" % (conn_name, parent_category)
    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)
    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

    self_parent = "%s|%s" % (self_category, parent_category)
    self_right = "%s|%s" % (self_category, right_sibling_category)
    self_left = "%s|%s" % (self_category, left_sibling_category)
    parent_left = "%s|%s" % (parent_category, left_sibling_category)
    parent_right = "%s|%s" % (parent_category, right_sibling_category)
    left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

    '''--- mine ---'''
    conn_lower_case = conn_name.lower()
    # prevPOS_C = "%s|%s" % (prevPOS, conn_name.lower())
    if syntax_tree.tree == None:
        _path = "NONE_TREE"
    else:
        _path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up
            _path += syntax_tree.get_node_path_to_root(conn_parent_node) + "-->"
        if _path[-3:] == "-->":
            _path = _path[:-3]

    # conn + connCtx
    if syntax_tree.tree == None:
        connCtx = "NONE_TREE"
    else:
        conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
        connCtx = dict_util.get_node_Ctx(conn_node, syntax_tree)

    conn_connCtx = "%s|%s" % (conn_name, connCtx)

    # conn + right sibling ctx
    if syntax_tree.tree == None:
        rightSiblingCtx = "NONE_TREE"
    else:
        rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

    conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

    # conn _ left sibling ctx
    if syntax_tree.tree == None:
        leftSiblingCtx = "NONE_TREE"
    else:
        leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

    conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

    # conn left right sibling ctx
    conn_left_right_SiblingCtx = "%s|%s|%s" % (conn_name, leftSiblingCtx, rightSiblingCtx)

    # conn parent category ctx
    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = dict_util.get_node_linked_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    #dict_conn_rightSibling_production_rules
    # if syntax_tree.tree == None:
    #     rightSibling_production_rules = ["NONE_TREE"]
    # else:
    #     rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
    #     rightSibling_production_rules = dict_util.get_node_production_rules(rightSibling_node, syntax_tree)


    features = []
    '''Z.Lin'''
    features.append(get_feature(feat_dict_CPOS_dict, CPOS_dict, CPOS))
    features.append(get_feature(feat_dict_prev_C_dict, prev_C_dict, prev_C))
    features.append(get_feature(feat_dict_prevPOS_dict, prevPOS_dict, prevPOS))
    features.append(get_feature(feat_dict_prevPOS_CPOS_dict, prevPOS_CPOS_dict, prePOS_CPOS ))
    features.append(get_feature(feat_dict_C_next_dict, C_next_dict, C_next))
    features.append(get_feature(feat_dict_nextPOS_dict, nextPOS_dict, nextPOS))
    features.append(get_feature(feat_dict_CPOS_nextPOS_dict, CPOS_nextPOS_dict, CPOS_nextPOS))
    features.append(get_feature(feat_dict_CParent_to_root_path_dict,CParent_to_root_path_dict, cparent_to_root_path ))
    features.append(get_feature(feat_dict_compressed_CParent_to_root_path_dict, compressed_CParent_to_root_path_dict, compressed_path))

    ''' pitler '''
    features.append(get_feature(feat_dict_self_category_dict, self_category_dict, self_category))
    features.append(get_feature(feat_dict_parent_category_dict, parent_category_dict, parent_category))
    features.append(get_feature(feat_dict_left_sibling_category_dict, left_sibling_category_dict, left_sibling_category))
    features.append(get_feature(feat_dict_right_sibling_category_dict, right_sibling_category_dict, right_sibling_category))

    feat_dict_is_right_sibling_contains_VP = {}
    if syntax_tree.tree != None and right_sibling_category_node != None:
        T = right_sibling_category_node.get_descendants()
        T.append(right_sibling_category_node)
        for node in T:
            if node.name == "VP" or node.name == "S":
                feat_dict_is_right_sibling_contains_VP[1] = 1
                break
    features.append(Feature("", 1, feat_dict_is_right_sibling_contains_VP))

    ''' conn-syn '''
    features.append(get_feature(feat_dict_conn_self_category_dict, conn_self_category_dict, conn_self_category))
    features.append(get_feature(feat_dict_conn_parent_category_dict, conn_parent_category_dict, conn_parent_category))
    features.append(get_feature(feat_dict_conn_left_sibling_category_dict, conn_left_sibling_category_dict, conn_left_sibling_category))
    features.append(get_feature(feat_dict_conn_right_sibling_category_dict, conn_right_sibling_category_dict, conn_right_sibling_category))

    ''' syn-syn '''

    features.append(get_feature(feat_dict_self_parent, self_parent_dict, self_parent))
    features.append(get_feature(feat_dict_self_right,self_right_dict, self_right ))
    features.append(get_feature(feat_dict_self_left, self_left_dict, self_left))
    features.append(get_feature(feat_dict_parent_left, parent_left_dict, parent_left))
    features.append(get_feature(feat_dict_parent_right, parent_right_dict, parent_right))
    features.append(get_feature(feat_dict_left_right,left_right_dict, left_right))

    ''' mine '''
    features.append(get_feature_by_feat(dict_conn_lower_case, conn_lower_case))
    features.append(get_feature_by_feat(dict_conn, conn_name))
    # features.append(get_feature_by_feat(dict_prevPOS_C, prevPOS_C))
    # features.append(get_feature_by_feat(dict_self_category_to_root_path, self_category_to_root_path))

    features.append(get_feature_by_feat_list(dict_CParent_to_root_path_node_names, _path.split("-->")))
    # features.append(get_feature_by_feat(dict_conn_connCtx, conn_connCtx))
    features.append(get_feature_by_feat(dict_conn_rightSiblingCtx, conn_rightSiblingCtx))
    # features.append(get_feature_by_feat(dict_conn_leftSiblingCtx, conn_leftSiblingCtx))
    # features.append(get_feature_by_feat(dict_conn_left_right_SiblingCtx, conn_left_right_SiblingCtx))
    features.append(get_feature_by_feat(dict_conn_parent_category_Ctx, conn_parent_categoryCtx))
    # features.append(get_feature_by_feat_list(dict_rightSibling_production_rules, rightSibling_production_rules))


    # connective category
    features.append(CON_Cat(parse_dict, DocID, sent_index, conn_indices))



    return util.mergeFeatures(features)


def CON_Cat(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_category = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }
    # 特征
    conn_category = Connectives_dict().conn_category
    conn_name = dict_util.get_conn_name(parse_dict, DocID, sent_index, conn_indices).lower()
    CON_Cat = conn_category[conn_name]

    return get_feature_by_feat(dict_category, CON_Cat)

def get_feature(feat_dict, dict, feat):
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

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


