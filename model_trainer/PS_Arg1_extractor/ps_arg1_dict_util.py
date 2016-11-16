#coding:utf-8
import copy
from syntax_tree import Syntax_tree
from clause import Arg_Clauses
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import util
from connective_dict import Connectives_dict
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper

def get_arg_clauses_with_label(parse_dict, relation):
    return [_arg_clauses_with_label(parse_dict, relation, "Arg1")]

def _arg_clauses_with_label(parse_dict, relation, Arg):
    DocID = relation["DocID"]
    Arg_sent_indices = sorted([item[3] for item in relation[Arg]["TokenList"]])
    if len(set(Arg_sent_indices)) != 1:
        return []
    relation_ID = relation["ID"]
    sent_index = Arg_sent_indices[0]
    Arg_list = sorted([item[4] for item in relation[Arg]["TokenList"]])

    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

    # sent_indices = sorted(list(set(range(0, sent_length)) - set(conn_token_indices)))
    sent_tokens = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, sent_length)]

    #按标点符号和连接词分
    punctuation = "...,:;?!~--"
    _clause_indices_list = []#[[(1,"I")..], ..]
    temp = []
    for index, word in sent_tokens:
        if word not in punctuation:
            temp.append((index, word))
        else:
            if temp != []:
                _clause_indices_list.append(temp)
                temp = []
    clause_indices_list = []
    for clause_indices in _clause_indices_list:
        temp = util.list_strip_punctuation(clause_indices)
        if temp != []:
            clause_indices_list.append([item[0] for item in temp])

    # 继续细化，根据语法树， 第一个SBAR
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        return []

    clause_list = []
    for clause_indices in clause_indices_list:
        clause_tree = _get_subtree(syntax_tree, clause_indices)
        # 层次遍历，
        flag = 0
        for node in clause_tree.tree.traverse(strategy="levelorder"):
            if node.name == "SBAR":
                temp1 = [node.index for node in node.get_leaves()]
                temp2 = sorted(list(set(clause_indices) - set(temp1)))

                if temp2 == []:
                    clause_list.append(temp1)
                else:
                    if temp1[0] < temp2 [0]:
                        clause_list.append(temp1)
                        clause_list.append(temp2)
                    else:
                        clause_list.append(temp2)
                        clause_list.append(temp1)


                flag = 1
                break
        if flag == 0:
            clause_list.append(clause_indices)

    # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)])
    # print clause_list
    # print Arg_list

    clauses = []# [([1,2,3],yes), ([4, 5],no), ]
    for clause_indices in clause_list:
        label = "no"
        if set(clause_indices) & set(Arg_list) == set([]):#是attribution
            label = "yes"
        clauses.append((clause_indices, label))

    gc = Arg_Clauses(relation_ID, Arg, DocID, sent_index, clauses)

    conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
    #需要将获取语篇连接词的头
    raw_connective = relation["Connective"]["RawText"]
    chm = ConnHeadMapper()
    conn_head, indices = chm.map_raw_connective(raw_connective)
    conn_head_indices = [conn_token_indices[index] for index in indices]

    gc.conn_indices = conn_head_indices
    gc.conn_head_name = conn_head
    return gc

def _get_subtree(syntax_tree, clause_indices):
    copy_tree = copy.deepcopy(syntax_tree)
    #给每个叶子节点，赋予feature ，即对应原来树的index

    for index, leaf in enumerate(copy_tree.tree.get_leaves()):
        leaf.add_feature("index",index)

    clause_nodes = []
    for index in clause_indices:
        node = copy_tree.get_leaf_node_by_token_index(index)
        clause_nodes.append(node)

    for node in copy_tree.tree.traverse(strategy="levelorder"):
        node_leaves = node.get_leaves()
        if set(node_leaves) & set(clause_nodes) == set([]):
            node.detach()
    return copy_tree

def get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)

    verbs = []
    for index in curr_clause[0]:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            verbs.append(word.lower())

    return verbs


def get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)

    lmtzr = WordNetLemmatizer()

    verbs = []
    for index in curr_clause[0]:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            word = lmtzr.lemmatize(word, "v")
            verbs.append(word)

    return verbs


def get_curr_first(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    curr_first_index = curr_clause[0][0]
    curr_first = parse_dict[DocID]["sentences"][sent_index]["words"][curr_first_index][0]

    return curr_first

def get_curr_last(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    curr_last_index = curr_clause[0][-1]
    curr_last = parse_dict[DocID]["sentences"][sent_index]["words"][curr_last_index][0]

    return curr_last

def get_prev_last(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    prev_last_index = curr_clause[0][0] - 1
    if prev_last_index < 0:
        return "NONE"
    punctuation = "...,:;``''?--!~"
    prev_last_word = parse_dict[DocID]["sentences"][sent_index]["words"][prev_last_index][0]
    if prev_last_word not in punctuation:#不是标点
        return prev_last_word
    else:#当前是标点，返回从他与他前面的标点 如 ”，
        temp = []
        index = prev_last_index
        while index >= 0:
            word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
            if word in punctuation:
                temp.append(word)
                index -= 1
            else:
                break
        return " ".join(temp)


def get_next_first(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    next_first_index = curr_clause[0][-1] + 1

    if next_first_index >= len(parse_dict[DocID]["sentences"][sent_index]["words"]):
        return "NONE"

    punctuation = "...,:;``''?--!~"
    next_first_word = parse_dict[DocID]["sentences"][sent_index]["words"][next_first_index][0]
    if next_first_word not in punctuation:
        return next_first_word
    else:
        temp = []
        index = next_first_index
        while index < len(parse_dict[DocID]["sentences"][sent_index]["words"]):
            word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
            if word in punctuation:
                temp.append(word)
                index += 1
            else:
                break
        return " ".join(temp)

def get_prev_last_curr_first(arg_clauses, clause_index, parse_dict):
    prev_last = get_prev_last(arg_clauses, clause_index, parse_dict)
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    prev_last_curr_first = "%s_%s" % (prev_last, curr_first)

    return prev_last_curr_first

def get_curr_last_next_first(arg_clauses, clause_index, parse_dict):
    curr_last = get_curr_last(arg_clauses, clause_index, parse_dict)
    next_first = get_next_first(arg_clauses, clause_index, parse_dict)
    curr_last_next_first = "%s_%s" % (curr_last, next_first)

    return curr_last_next_first


def get_curr_production_rule(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    subtrees = []
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree != None:
        clause_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in curr_clause_indices])
        #进行层次遍历
        no_need = []
        for node in syntax_tree.tree.traverse(strategy="levelorder"):
            if node not in no_need:
                if set(node.get_leaves()) <= clause_leaves:
                    subtrees.append(node)
                    no_need.extend(node.get_descendants())

    #3. 对每个子树产生production rule
    production_rule = []
    for tree in subtrees:
        #层次遍历
        for node in tree.traverse(strategy="levelorder"):
            if not node.is_leaf():
                rule = node.name + "-->" + " ".join([child.name for child in node.get_children()])
                production_rule.append(rule)

    return production_rule


def get_curr_position(arg_clauses, clause_index, parse_dict):
    length = len(arg_clauses.clauses)
    if length == 1:
        return "middle"
    elif length < 5:
        if clause_index == 0:
            return "left"
        elif clause_index == length - 1:
            return "right"
        else:
            return "middle"
    else:
        if clause_index <= 1:
            return "left"
        elif clause_index >= length - 2:
            return "right"
        else:
            return "middle"


def get_is_curr_NNP_prev_PRP_or_NNP(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NONE"
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    prev_clause_indices = arg_clauses.clauses[clause_index-1][0]

    curr_poses = set([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
                    for index in curr_clause_indices])

    prev_poses = set([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
                    for index in prev_clause_indices])

    if set(["WHNP", "NNP"]) & curr_poses and set(["NNP", "PRP"]) & prev_poses != set([]):
        return "yes"
    else:
        return "no"


# curr 与 prev 合成的子树的 production rules
def get_prev_curr_production_rule(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    if clause_index > 0:
        prev_clause_index = clause_index - 1
        curr_clause_indices = arg_clauses.clauses[prev_clause_index][0] + curr_clause_indices

    subtrees = []
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree != None:
        clause_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in curr_clause_indices])
        #进行层次遍历
        no_need = []
        for node in syntax_tree.tree.traverse(strategy="levelorder"):
            if node not in no_need:
                if set(node.get_leaves()) <= clause_leaves:
                    subtrees.append(node)
                    no_need.extend(node.get_descendants())

    #3. 对每个子树产生production rule
    production_rule = []
    for tree in subtrees:
        #层次遍历
        for node in tree.traverse(strategy="levelorder"):
            if not node.is_leaf():
                rule = node.name + "-->" + " ".join([child.name for child in node.get_children()])
                production_rule.append(rule)

    return production_rule


# curr 与 prev 子树 cross_production 的 production rules
def get_prev_curr_CP_production_rule(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return ["%s|%s" % ("NULL", rule) for rule in get_curr_production_rule(arg_clauses, clause_index, parse_dict)]

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    prev_production_rule = get_curr_production_rule(arg_clauses, clause_index - 1, parse_dict)

    CP_production_rule = []
    for curr_rule in curr_production_rule:
        for prev_rule in prev_production_rule:
            CP_production_rule.append("%s|%s" % (prev_rule, curr_rule))

    return CP_production_rule

# curr 与 prev 子树 cross_production 的 production rules
def get_curr_next_CP_production_rule(arg_clauses, clause_index, parse_dict):
    if clause_index == len(arg_clauses.clauses) - 1:
        return ["%s|%s" % (rule, "NULL") for rule in get_curr_production_rule(arg_clauses, clause_index, parse_dict)]

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    next_production_rule = get_curr_production_rule(arg_clauses, clause_index + 1, parse_dict)

    CP_production_rule = []
    for curr_rule in curr_production_rule:
        for next_rule in next_production_rule:
            CP_production_rule.append("%s|%s" % (curr_rule, next_rule))

    return CP_production_rule

# prev: NP->NNP, curr: WHNP->WP
def get_is_NNP_WP(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NONE"

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    prev_production_rule = get_curr_production_rule(arg_clauses, clause_index - 1, parse_dict)

    flag = 0
    for rule in curr_production_rule:
        part1, part2 = rule.split("-->")
        if "WHNP" in part1 and "WP" in part2:
            flag = 1
            break
    if flag == 1:
        for rule in prev_production_rule:
            part1, part2 = rule.split("-->")
            if "NP" in part1 and "NNP" in part2:
                return "yes"
        return "no"
    else:
        return "no"

#lemma verb ＋ prev 2 pos
def get_2prev_pos_lemma_verb(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    lmtzr = WordNetLemmatizer()

    first_verb = ""
    first_verb_index = 0
    for index in curr_clause_indices:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            word = lmtzr.lemmatize(word)
            first_verb = (word, index)
            break
        first_verb_index += 1
    if first_verb == "":
        return "NULL|NULL|NULL"
    if first_verb_index == 0:
        return "%s|%s|%s" % ("NULL", "NULL", first_verb[0])
    if first_verb_index == 1:
        prev1_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 1][1]["PartOfSpeech"]
        return "%s|%s|%s" % ("NULL", prev1_pos, first_verb[0])

    prev1_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 1][1]["PartOfSpeech"]
    prev2_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 2][1]["PartOfSpeech"]
    return "%s|%s|%s" % (prev2_pos, prev1_pos, first_verb[0])

# 当前第一个词的pos到前一个clause的最后一个词的pos的路径
def get_curr_first_to_prev_last_path(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NULL"

    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        return "NOTREE"

    curr_first_index = arg_clauses.clauses[clause_index][0][0]
    prev_last_index = arg_clauses.clauses[clause_index - 1][0][-1]

    curr_first_node = syntax_tree.get_leaf_node_by_token_index(curr_first_index).up
    prev_last_node = syntax_tree.get_leaf_node_by_token_index(prev_last_index).up

    path = syntax_tree.get_node_to_node_path(curr_first_node, prev_last_node)

    return path

# con str
def get_con_str(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name

# con str
def get_con_lstr(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name.lower()

# conn cate
def get_con_cat(arg_clauses, clause_index, parse_dict):
    conn_category = Connectives_dict().conn_category
    return conn_category[arg_clauses.conn_head_name]

def get_clause_conn_position(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices#[5]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    if conn_indices[0] > curr_clause_indices[-1]:
        return "left"
    else:
        return "right"

#clause 与conn 的相隔的clause个数
def get_clause_conn_distance(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices#[5]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    if conn_indices[-1] < curr_clause_indices[0]:
        s = conn_indices[-1]
        e = curr_clause_indices[0]
    else:
        s = curr_clause_indices[-1]
        e = conn_indices[0]
    count = 0
    for clause_indices, _ in arg_clauses.clauses:
        if clause_indices[0] > s and clause_indices[-1] < e:
            count += 1
    return count

def get_conn_position_distance(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)
    position = get_clause_conn_position(arg_clauses, clause_index, parse_dict)
    distance = get_clause_conn_distance(arg_clauses, clause_index, parse_dict)

    return "%s_%s_%d" % (conn, position, distance)

# conn cate
def get_conn_to_root_path(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    #获取该句话的语法树
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        path = "NONE_TREE"
    else:
        path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            t = syntax_tree.get_node_path_to_root(conn_node)
            path += t + "&"
        if path[-1] == "&":
            path = path[:-1]

    return path

def get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    #获取该句话的语法树
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

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
    return compressed_path

def get_conn_position(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)
    position = get_clause_conn_position(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, position)

def get_conn_curr_position(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)

    curr_position = get_curr_position(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, curr_position)

# 当前clause是否有 , which
def get_is_clause_contain_comma_which(arg_clauses, clause_index, parse_dict):
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    # curr_first 的前面一个词
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    prev_last_index = curr_clause[0][0] - 1
    if prev_last_index < 0:
        return "NO"
    prev_last_word = parse_dict[DocID]["sentences"][sent_index]["words"][prev_last_index][0]

    prev_last_curr_first = "%s %s" % (prev_last_word, curr_first)

    if prev_last_curr_first == ", which":
        # print 1
        return "YES"
    else:
        # print 0
        return "NO"

def get_curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    if clause_index - 1 < 0:
        return "NONE"

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    curr_first_index = arg_clauses.clauses[clause_index][0][0]
    prev_last_index = arg_clauses.clauses[clause_index - 1][0][-1]

    curr_first_node = syntax_tree.get_leaf_node_by_token_index(curr_first_index)
    prev_last_node = syntax_tree.get_leaf_node_by_token_index(prev_last_index)

    path = syntax_tree.get_node_to_node_path(curr_first_node, prev_last_node)

    if path.find("<") != -1:
        path_1 = path[:path.find("<")]
        path_2 = path[path.find("<"):]
        return util.get_compressed_path_tag(path_1, ">") + util.get_compressed_path_tag(path_2, "<")
    else:
        return util.get_compressed_path_tag(path, ">")


def get_CParent_to_root_path_node_names(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_indices = arg_clauses.conn_indices

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

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

    return path.split("-->")

def get_CPOS(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_indices = arg_clauses.conn_indices

    pos_tag_list = []
    for conn_index in conn_indices:
        pos_tag_list.append(parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
    CPOS = "_".join(pos_tag_list)

    return CPOS

def get_conn_connCtx(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_indices = arg_clauses.conn_indices

    conn_name = get_con_str(arg_clauses, clause_index, parse_dict)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    # conn + connCtx
    if syntax_tree.tree == None:
        connCtx = "NONE_TREE"
    else:
        conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
        connCtx = get_node_Ctx(conn_node, syntax_tree)

    conn_connCtx = "%s|%s" % (conn_name, connCtx)

    return conn_connCtx

def get_conn_parent_category_Ctx(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1 # 这里的sent_index指的是Arg1的，conn的sent_index 在下一句
    conn_indices = arg_clauses.conn_indices

    conn_name = get_con_str(arg_clauses, clause_index, parse_dict)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = get_node_linked_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    return conn_parent_categoryCtx

def get_conn_curr_first(arg_clauses, clause_index, parse_dict):
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    conn = get_con_lstr(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, curr_first)

#与之相连的上下文
def get_node_linked_Ctx(node, syntax_tree):
    if node == None:
        return "None"
    Ctx = []
    #self
    Ctx.append(node.name)
    #parent
    if node.up == None:
        Ctx.append("NULL")
    else:
        Ctx.append(node.up.name)
    #children
    for child in node.get_children():
        Ctx.append(child.name)

    return "-".join(Ctx)

def get_node_Ctx(node, syntax_tree):
    if node == None:
        return "None"
    Ctx = []
    #self
    Ctx.append(node.name)
    #parent
    if node.up == None:
        Ctx.append("NULL")
    else:
        Ctx.append(node.up.name)
    #left
    left_siblings = syntax_tree.get_left_siblings(node)
    if left_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(left_siblings[-1].name)
    #right
    right_siblings = syntax_tree.get_right_siblings(node)
    if right_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(right_siblings[0].name)

    nodeCtx = "-".join(Ctx)
    return nodeCtx

def get_clause_first_conn_pos(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    clause_words = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in curr_clause_indices]
    clause_POS = [parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"] for index in curr_clause_indices]

    conn_names, indices = _check_connective_names(clause_words)

    # Arg2 中的 disc conn
    con_lstr = get_con_lstr(arg_clauses, clause_index, parse_dict)

    if conn_names != []:
        pos = " ".join([clause_POS[index] for index in indices[0]])
        conn = conn_names[0]
        return "%s_%s" % (con_lstr, conn)
    else:
        return "%s_NULL" % (con_lstr)

def get_clause_main_verb_conn(arg_clauses, clause_index, parse_dict):
    con_lstr = get_con_lstr(arg_clauses, clause_index, parse_dict)
    lemma_verbs = get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    if lemma_verbs == []:
        return "%s_%s" % (con_lstr, "NULL")
    else:
        return "%s_%s" % (con_lstr, lemma_verbs[0])

def get_clause_modality_conn(arg_clauses, clause_index, parse_dict):
    con_lstr = get_con_lstr(arg_clauses, clause_index, parse_dict)


''' 识别sentence中的连接词, 返回识别出来的连接词的name # ["but", "in particular"] '''
def _check_connective_names(sent_tokens):
    sent_tokens = [word.lower() for word in sent_tokens ]
    indices = []
    conn_names = []
    tagged = set([])#已经标记列表
    sortedConn = Connectives_dict().sorted_conns_list
    for conn in sortedConn:
        #判断连接词是否在句子中出现
        if '..' in conn:#对于这种类型的在sentence中只识别一次
            c1, c2 = conn.split('..')
            c1_indice = util.getSpanIndecesInSent(c1.split(), sent_tokens)#[[7]]
            c2_indice = util.getSpanIndecesInSent(c2.split(), sent_tokens)#[[10]]
            if c1_indice!= [] and c2_indice != []:#词在句子中
                if c1_indice[0][0] < c2_indice[0][0]:#c1,c2 的先后顺序也不能错
                    #识别到该连接词
                    temp = set([t for t in (c1_indice[0]+c2_indice[0]) ])
                    #判断连接词是否已经被识别过了，如 已经识别了 for example 就不用去识别for 了
                    if tagged & temp == set([]):#没有被识别过，加入indices，加入tagged
                        indices.append(c1_indice[0]+c2_indice[0])# [[7], [10]]
                        conn_names.append(conn)
                        tagged = tagged.union(temp)
        else:
            c_indice = util.getSpanIndecesInSent(conn.split(), sent_tokens)#[[2,6],[1,3],...]
            if c_indice !=[]:
                #检查c_indice中每一项，如果该项在tagged中存在，剔除该项
                tt = []
                for item in c_indice:
                    if set(item) & tagged == set([]):
                        tt.append(item)
                c_indice = tt

                if c_indice != []:
                    indices.extend([item for item in c_indice])#[([2,6], 'for instance'), ....]
                    tagged = tagged.union(set([r for t in c_indice for r in t]))
                    conn_names.append(conn)
    return conn_names , indices
if __name__ == "__main__":
    from pdtb_parse import PDTB_PARSE
    import config
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    IPS_relations = pdtb_parse.pdtb.IPS_relations
    parse_dict = pdtb_parse.parse_dict

    for curr_index, relation in enumerate(IPS_relations):
        for arg_clauses in get_arg_clauses_with_label(parse_dict, relation):
            pass