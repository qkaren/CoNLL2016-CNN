import numpy as np
import config, util, os

def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = list(map(int, header.split()))
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in range(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            if word in vocab:
                word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)

    return word_vecs

def write_word_vec_to_file(word_vecs, to_file):
    f_out = open(to_file, "w")
    for word in word_vecs:
        f_out.write(word+":"+" ".join([str(f) for f in word_vecs[word] ])+"\n")
    f_out.close()


class WordEmbeddingDict(object):

    def __init__(self, word_embedding_file):
        lines = open(word_embedding_file).readlines()
        self.num_units = len(lines[1].strip().split(' ')) - 1
        self.vocab_size = len(lines)
        self.word_to_vector = {}
        for line in lines[1:]:
            word, vector = line.split(' ', 1)
            self.word_to_vector[word] = vector.strip()

    def __getitem__(self, key):
        vector = self.word_to_vector[key]
        if isinstance(vector, str):
            self.word_to_vector[key] = np.array([float(x) for x in vector.split(' ')])
        return self.word_to_vector[key]

    def __contains__(self, key):
        return key in self.word_to_vector

from gensim.models import Word2Vec
def get_word_vecs_by_gensim(vocab):
    model_path = '/Users/Hunter/Documents/conll2015/conll15st/data/GoogleNews-vectors-negative300.bin'
    model = Word2Vec.load_word2vec_format(model_path, binary=True)  # C binary format

    word_vecs = {}
    for word in vocab:
        if word in model:
            word_vecs[word] = model[word]
    return word_vecs



if __name__ == "__main__":
    # vocab = util.load_list_from_file(config.NON_EXPLICIT_DICT_ALL_WORDS)
    # word_vecs = get_word_vecs_by_gensim(vocab)
    # write_word_vec_to_file(word_vecs, config.NON_EXPLICIT_DICT_WORD2VEC)

    # word_embedding_dict = WordEmbeddingDict(os.path.expanduser(config.SKIPGRAM_WORD_EMBEDDING_FILE))

    # print word_embedding_dict["good"]
    pass