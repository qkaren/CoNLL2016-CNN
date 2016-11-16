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



data_process(dev_relations,dev_parses)