import  json
import codecs

threshold_vocab = 2
ndims = 300
pos_ndims = 50
maxlen = 80
trian_file_path = "../../data/conll16st-en-01-12-16-train/"
dev_file_path = "../../data/conll16st-en-01-12-16-dev/"
parses_file_name = "parses.json"
relations_file_name = "relations.json"
train_parses = trian_file_path + parses_file_name
dev_parses = trian_file_path + parses_file_name
train_relations = trian_file_path + relations_file_name
dev_relations = trian_file_path + relations_file_name
dev = "dev.json"
vocab = set()
pos_vocab = set()
w2i_dic = {}
p2i_dic = {}
# w2v_file = "../../../../GoogleNews-vectors-negative300.bin"
# wv = Word2Vec.load_word2vec_format(w2v_file, binary=True)

def data_process(relations_file,parses_file):
    rf = open(relations_file)
    pf = open(parses_file)
    relations = [json.loads(x) for x in rf]
    parse_dict = json.load(codecs.open(parses_file, encoding='utf8'))
    relation = []
    flag= 0
    for r in relations:
        docid = r['DocID']
        type = r['Type']
        sense = r['Sense']
        if type == 'Explicit':
            continue
        ''' arg_offset_list = [sentence_index] from TokenList in relations '''
        arg1_sent = set()
        arg2_sent = set()
        arg1_word = []
        arg2_word = []
        arg1_pos = []
        arg2_pos = []
        for t in r['Arg1']['TokenList']:
            arg1_sent.add(t[3])
        for i in arg1_sent:
            arg1_word += [w[0] for w in parse_dict[docid]["sentences"][i]["words"]]
            arg1_pos += [w[1]["PartOfSpeech"] for w in parse_dict[docid]["sentences"][i]["words"]]
            print(i,arg1_word,arg1_pos)
        for t in r['Arg2']['TokenList']:
            arg2_sent.add(t[3])
        for i in arg2_sent:
            arg2_word += [w[0] for w in parse_dict[docid]["sentences"][i]["words"]]
            arg2_pos += [w[1]["PartOfSpeech"] for w in parse_dict[docid]["sentences"][i]["words"]]
        relation.append((arg1_word,arg2_word,arg1_pos,arg2_pos,sense,docid))
        print(relation)
    return relation

data_process(dev_relations,dev_parses)