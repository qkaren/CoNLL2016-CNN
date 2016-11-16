import sys
sys.path.append("./")
sys.path = ['/home/tao0920/libs/keras-fix'] + sys.path
import json
import numpy as np
from keras.utils import np_utils
from model_trainer.cnn_implicit_classifier import cnn_config
from model_trainer.cnn_implicit_classifier.trainer import build_model
from keras.preprocessing import sequence
import config

maxlen=120
def test_imp(instances):
    nb_filter, filter_length1, filter_length2, filter_length3 = 1024,3,3,3
    lr = 0.001
    activation = 'tanh'
    batch_size = 128
    rf = open(config.CNN_IMP_DICT,'r')
    vocab = json.load(rf)
    w2i_dic = vocab[0]
    p2i_dic = vocab[1]
    Arg1_word,Arg2_word,Arg1_pos,Arg2_pos = embedding_process(instances, w2i_dic, p2i_dic)
    print("Implicit cnn is building...")
    model = build_model(lr,activation, nb_filter, filter_length1, filter_length2, filter_length3,train=False)
    print("Implicit cnn finish building!")
    model.load_weights(config.CNN_IMP_MODEL)
    dev_output = model.predict({'arg1': Arg1_word, 'arg2': Arg2_word, 'pos1': Arg1_pos, 'pos2': Arg2_pos},
                                       batch_size=batch_size)['output']
    # print(dev_output)
    return dev_output

def test_nop(instances):
    nb_filter, filter_length1, filter_length2, filter_length3 = 512 ,4,8,12
    lr = 0.001
    activation = 'tanh'
    batch_size = 64
    rf = open(config.CNN_NOEXP_DICT,'r')
    vocab = json.load(rf)
    w2i_dic = vocab[0]
    p2i_dic = vocab[1]
    Arg1_word,Arg2_word,Arg1_pos,Arg2_pos = embedding_process(instances, w2i_dic, p2i_dic)
    print("Non_Explicit cnn is building...")
    model = build_model(lr,activation, nb_filter, filter_length1, filter_length2, filter_length3,word_dim=36821,train=False)
    print("Non_Explicit cnn finish building!")
    model.load_weights(config.CNN_NOEXP_MODEL)
    dev_output = model.predict({'arg1': Arg1_word, 'arg2': Arg2_word, 'pos1': Arg1_pos, 'pos2': Arg2_pos},
                                       batch_size=batch_size)['output']
    # print(dev_output)
    return dev_output

def embedding_process(instances, w2i_dic, p2i_dic):
        tmp = []
        for x in instances:
            arg1 = []
            arg2 = []
            pos1 = []
            pos2 = []
            sense = []
            for w in x[0]:
                if w in w2i_dic.keys():
                    arg1.append(w2i_dic[w])
                else:
                    arg1.append(0)
            for w in x[1]:
                if w in w2i_dic.keys():
                    arg2.append(w2i_dic[w])
                else:
                    arg2.append(0)
            for w in x[2]:
                if w in p2i_dic.keys():
                    pos1.append(p2i_dic[w])
                else:
                    pos1.append(0)
            for w in x[3]:
                if w in p2i_dic.keys():
                    pos2.append(p2i_dic[w])
                else:
                    pos2.append(0)
            tmp.append((arg1, arg2, pos1, pos2, sense))
        data = tmp
        X_1 = np.array([x[0] for x in data])
        X_2 = np.array([x[1] for x in data])
        X_pos_1 = np.array([x[2] for x in data])
        X_pos_2 = np.array([x[3] for x in data])
        X_1 = sequence.pad_sequences(X_1, maxlen=maxlen, padding='pre', truncating='pre')
        X_2 = sequence.pad_sequences(X_2, maxlen=maxlen, padding='post', truncating='post')
        X_pos_1 = sequence.pad_sequences(X_pos_1, maxlen=maxlen, padding='pre', truncating='pre')
        X_pos_2 = sequence.pad_sequences(X_pos_2, maxlen=maxlen, padding='post', truncating='post')
        print((X_1.shape, X_pos_1.shape))
        return (X_1, X_2, X_pos_1, X_pos_2)
