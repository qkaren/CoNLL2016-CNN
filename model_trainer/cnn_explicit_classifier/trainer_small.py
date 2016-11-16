import codecs
import sys
sys.path.append("./")
import json
import numpy as np
import exp_config
from keras.models import Graph
from keras.layers.core import Dense, Activation, Flatten,Dropout,Reshape
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.preprocessing import sequence
from keras.layers.embeddings import Embedding
from keras.optimizers import Adagrad
from gensim.models import Word2Vec
from keras.utils import np_utils
from keras.callbacks import Callback,EarlyStopping
from conn_head_mapper import ConnHeadMapper

def pretainning():
    threshold_vocab = 0
    ndims = 50
    pos_ndims = 50
    conn_ndims = 50
    maxlen = 120
    trian_file_path = "../../data/conll16st-en-01-12-16-train/"
    dev_file_path = "../../data/conll16st-en-01-12-16-dev/"
    parses_file_name = "parses.json"
    relations_file_name = "relations.json"
    train_parses = trian_file_path + parses_file_name
    dev_parses = dev_file_path + parses_file_name
    train_relations = trian_file_path + relations_file_name
    dev_relations = dev_file_path + relations_file_name
    vocab = set()
    pos_vocab = set()
    conn_vocab = set()
    w2i_dic = {}
    p2i_dic = {}
    c2i_dic = {}
    w2v_file = "../../../../GoogleNews-vectors-negative300.bin"
    # wv = Word2Vec.load_word2vec_format(w2v_file, binary=True)

    def data_process(relations_file,parses_file):
        rf = open(relations_file)
        pf = open(parses_file)
        relations = [json.loads(x) for x in rf]
        parse_dict = json.load(codecs.open(parses_file, encoding='utf8'))
        relation = []
        for r in relations:
            type = r['Type']
            sense = r['Sense']
            if type == 'Explicit':
                docid = r['DocID']
                # deal with connective
                connective_raw = r['Connective']['RawText']
                connective_mapping = ConnHeadMapper.DEFAULT_MAPPING[connective_raw]
                try:
                    connective_index = connective_raw.lower().split().index(connective_mapping.lower().split()[0])
                except:
                    # print("!! warning:",connective_raw,"||",connective_mapping)
                    connective_index = 0
                conn_vocab.add(connective_mapping)
                conn_index = [[x[3],x[4]] for x in r['Connective']['TokenList']]
                ''' arg_offset_list = [sentence_index,wordinsentence_index] from TokenList in relations '''
                arg1_tokenlist = [[t[3],t[4]] for t in r['Arg1']['TokenList']]
                arg2_tokenlist = [[t[3],t[4]] for t in r['Arg2']['TokenList']] + conn_index
                arg2_tokenlist.sort(key=lambda x:x[1])
                arg1_word = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][0] for sent_index,word_index in arg1_tokenlist]
                arg1_pos = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"] for sent_index,word_index in arg1_tokenlist]
                arg2_word = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][0] for sent_index,word_index in arg2_tokenlist]
                arg2_pos = [parse_dict[docid]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"] for sent_index,word_index in arg2_tokenlist]
                arg2_dis = [x[1]-conn_index[connective_index][1] for x in arg2_tokenlist]
                ''' add 0/1 to each word'''
                arg2_if_conn = []
                for s,w in arg2_tokenlist:
                    if [s,w] in conn_index:
                        arg2_if_conn.append(1)
                    else:
                        arg2_if_conn.append(0)
                relation.append((arg1_word,arg2_word,arg1_pos,arg2_pos,sense,connective_mapping,arg2_if_conn,arg2_dis,docid))
        fw = open("conn_vocab.txt",'w')
        tmp_list = sorted(list(conn_vocab))
        str = json.dumps(tmp_list)
        fw.write(str)
        fw.close()
        return relation

    def vocab_process():
        count = {}
        relation = data_process(train_relations,train_parses)
        for x in relation:
            for w in x[0]+x[1]:
                if w in count.keys():
                    count[w] += 1
                else:
                    count[w] = 1
        for x in relation:
            for w in x[0]+x[1]:
                if w in count.keys():
                    if count[w] > threshold_vocab:
                        vocab.add(w)
            for p in x[2]+x[3]:
                pos_vocab.add(p)


    def WE_process():
        vocab_process()
        idx = 1  # o for unknown
        for w in vocab:
            w2i_dic[w] = idx
            idx += 1
        WE = np.zeros((len(vocab) + 1, ndims), dtype='float32')
        pos_WE = np.zeros((len(pos_vocab) + 1, pos_ndims), dtype='float32')
        conn_WE = np.zeros((len(conn_vocab) + 1, conn_ndims), dtype='float32')
        pre_trained = set()
        # pre_trained = WE = np.zeros((len(vocab) + 1, ndims), dtype='float32')
        WE[0, :] = np.array(np.random.uniform(-0.5 / ndims, 0.5 / ndims, (ndims,)), dtype='float32')
        pos_WE[0, :] = np.array(np.random.uniform(-0.5 / pos_ndims, 0.5 / pos_ndims, (pos_ndims,)), dtype='float32')
        conn_WE[0, :] = np.array(np.random.uniform(-0.5 / conn_ndims, 0.5 / conn_ndims, (conn_ndims,)), dtype='float32')
        for x in vocab:
            if x in pre_trained:
                WE[w2i_dic[x], :] = None
                # pass
            else:
                WE[w2i_dic[x], :] = np.array(np.random.uniform(-0.5 / ndims, 0.5 / ndims, (ndims,)),
                                             dtype='float32')  # hyperparameter
        for i, y in enumerate(pos_vocab,start=1):
            p2i_dic[y] = i
            pos_WE[i, :] = np.array(np.random.uniform(-0.5 / pos_ndims, 0.5 / pos_ndims, (pos_ndims,)), dtype='float32')

        for i, y in enumerate(conn_vocab,start=1):
            c2i_dic[y] = i
            conn_WE[i, :] = np.array(np.random.uniform(-0.5 / conn_ndims, 0.5 / conn_ndims, (conn_ndims,)), dtype='float32')
        dict_str = json.dumps([w2i_dic,p2i_dic,c2i_dic])

        f = open("all_vocab_dict.txt",'w')
        f.write(dict_str)
        f.close()
        return WE, pos_WE, conn_WE

    def embedding_process(train_relations,train_parses):
        data = data_process(train_relations,train_parses)
        tmp = []
        dist_map =20
        for x in data:
            arg1 = []
            arg2 = []
            pos1 = []
            pos2 = []
            conn = []
            sense1 = []
            sense2 = []
            dist = []
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
            for distance in x[7]:
                if distance >= dist_map:
                    dist.append(dist_map*2)
                elif distance <= -dist_map:
                    dist.append(0)
                else:
                    dist.append(distance+dist_map)
            if x[5] in c2i_dic.keys():
                conn.append(c2i_dic[x[5]])
            else:
                conn.append(0)
            if_conn = x[6]
            if len(x[4])>1:
                sense1.append(exp_config.Sense_To_Label[x[4][0]])
                tmp.append((arg1, arg2, pos1, pos2, sense1, conn, dist,if_conn))
                sense2.append(exp_config.Sense_To_Label[x[4][1]])
                tmp.append((arg1, arg2, pos1, pos2, sense2, conn, dist,if_conn))
            else:
                sense1.append(exp_config.Sense_To_Label[x[4][0]])
                tmp.append((arg1, arg2, pos1, pos2, sense1, conn, dist,if_conn))

        data = tmp
        X_1 = np.array([x[0] for x in data])
        X_2 = np.array([x[1] for x in data])
        X_pos_1 = np.array([x[2] for x in data])
        X_pos_2 = np.array([x[3] for x in data])
        X_conn = np.array([x[5] for x in data])
        X_dist = np.array([x[6] for x in data])
        X_if_conn = np.array([x[7] for x in data])
        y_s = np_utils.to_categorical(np.array([x[4] for x in data]))
        X_1 = sequence.pad_sequences(X_1, maxlen=maxlen, padding='pre', truncating='pre')
        X_2 = sequence.pad_sequences(X_2, maxlen=maxlen, padding='post', truncating='post')
        X_pos_1 = sequence.pad_sequences(X_pos_1, maxlen=maxlen, padding='pre', truncating='pre')
        X_pos_2 = sequence.pad_sequences(X_pos_2, maxlen=maxlen, padding='post', truncating='post')
        X_conn = sequence.pad_sequences(X_conn, maxlen=1, padding='post', truncating='post')
        X_dist = sequence.pad_sequences(X_dist, maxlen=maxlen, padding='post', truncating='post')
        X_if_conn = sequence.pad_sequences(X_if_conn, maxlen=maxlen, padding='post', truncating='post')
        print(train_relations,train_parses, (X_1.shape, X_pos_1.shape, y_s.shape, X_conn.shape,X_if_conn.shape,X_dist.shape))
        return (X_1, X_2, X_pos_1, X_pos_2, X_conn, X_dist, X_if_conn,y_s)

    WE, pos_WE,conn_WE = WE_process()
    X_train_1, X_train_2, X_train_pos_1, X_train_pos_2,X_train_conn,X_train_dist,X_train_ifconn, y_train = embedding_process(train_relations,train_parses)
    X_dev_1, X_dev_2, X_dev_pos_1, X_dev_pos_2,X_dev_conn,X_dev_dist,X_dev_ifconn, y_dev = embedding_process(dev_relations,dev_parses)
    print("the lens of vocab, pos_vocab and conn_vocab: ",len(vocab),len(pos_vocab),len(conn_vocab))
    return (WE, pos_WE, conn_WE,len(vocab), len(pos_vocab),len(conn_vocab),len(X_train_dist),
            X_train_1, X_train_2, X_train_pos_1, X_train_pos_2, X_train_conn,X_train_dist, X_train_ifconn,y_train,
            X_dev_1, X_dev_2, X_dev_pos_1, X_dev_pos_2, X_dev_conn,X_dev_dist, X_dev_ifconn,y_dev)

def build_model(lr, activation, nb_filter, filter_length1, filter_length2, filter_length3,
                WE=None, pos_WE=None, conn_WE=None,word_dim=35397, pos_dim=45,conn_dim=100,dist_dim=100,
                ifconn_dim=2,ndims = 300,pos_ndims = 100,conn_ndims=100,dist_ndims=100,
                ifconn_ndims=30,pool_length = 120,maxlen = 120,train = True):

    model = Graph()
    model.add_input(name='arg1', input_shape=(maxlen,), dtype=int)
    model.add_input(name='arg2', input_shape=(maxlen,), dtype=int)
    model.add_input(name='pos1', input_shape=(maxlen,), dtype=int)
    model.add_input(name='pos2', input_shape=(maxlen,), dtype=int)
    model.add_input(name='conn', input_shape=(1,), dtype=int)
    model.add_input(name='dist', input_shape=(maxlen,), dtype=int)
    model.add_input(name='ifconn', input_shape=(maxlen,), dtype=int)

    # our vocab indices into embedding_dims dimensions
    if (WE is not None):
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, weights=[WE], output_dim=ndims),
            name='emb_arg1', input='arg1')
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, weights=[WE], output_dim=ndims),
            name='emb_arg2', input='arg2')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen, weights=[pos_WE], output_dim=pos_ndims),
            name='emb_pos1', input='pos1')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen, weights=[pos_WE], output_dim=pos_ndims),
            name='emb_pos2', input='pos2')
        model.add_node(
            Embedding(input_dim=conn_dim + 1, input_length=1, weights=[conn_WE], output_dim=conn_ndims),
            name='emb_conn', input='conn')
        model.add_node(
            Embedding(input_dim=dist_dim + 1, input_length=maxlen, output_dim=dist_ndims),
            name='emb_dist', input='dist')
        model.add_node(
            Embedding(input_dim=ifconn_dim + 1, input_length=maxlen, output_dim=ifconn_ndims),
            name='emb_ifconn', input='ifconn')
    else:
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, output_dim=ndims),
            name='emb_arg1', input='arg1')
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, output_dim=ndims),
            name='emb_arg2', input='arg2')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen ,output_dim=pos_ndims),
            name='emb_pos1', input='pos1')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen,output_dim=pos_ndims),
            name='emb_pos2', input='pos2')
        model.add_node(
            Embedding(input_dim=conn_dim + 1, input_length=1, output_dim=conn_ndims),
            name='emb_conn', input='conn')
        model.add_node(
            Embedding(input_dim=dist_dim + 1, input_length=maxlen, output_dim=dist_ndims),
            name='emb_dist', input='dist')
        model.add_node(
            Embedding(input_dim=ifconn_dim + 1, input_length=maxlen, output_dim=ifconn_ndims),
            name='emb_ifconn', input='ifconn')

    model.add_node(Dropout(0.25), merge_mode='concat', concat_axis=2, name='arg_1', inputs=['emb_arg1', 'emb_pos1'])
    model.add_node(Dropout(0.25), merge_mode='concat', concat_axis=2, name='arg_2', inputs=['emb_arg2', 'emb_pos2','emb_dist','emb_ifconn'])

    def TMP_add_cnn(input_name,output_name,f_length):
        model.add_node(Convolution1D(nb_filter=nb_filter, filter_length=f_length, border_mode='same',
                                        activation=activation, subsample_length=1), input=input_name, name=output_name)

    TMP_add_cnn('arg_1', 'cnn1_arg1', filter_length1)
    TMP_add_cnn('arg_1', 'cnn2_arg1', filter_length2)
    TMP_add_cnn('arg_1', 'cnn3_arg1', filter_length3)
    TMP_add_cnn('arg_2', 'cnn1_arg2', filter_length1)
    TMP_add_cnn('arg_2', 'cnn2_arg2', filter_length2)
    TMP_add_cnn('arg_2', 'cnn3_arg2', filter_length3)

    # we use standard max pooling (halving the output of the previous layer):
    model.add_node(MaxPooling1D(pool_length=pool_length), name='mpooling',
                   inputs=['cnn1_arg1','cnn2_arg1','cnn3_arg1','cnn1_arg2','cnn2_arg2','cnn3_arg2'])
    model.add_node(Flatten(), name='f1', input='mpooling')

    model.add_node(Flatten(), name='connf', input='emb_conn')
    model.add_node(Dense(19),name='final', inputs=['f1','connf'],merge_mode='concat')
    model.add_node(Activation('softmax'),name='lastDim',input='final')
    model.add_output(name='output', input = 'lastDim')

    ada = Adagrad(lr=lr, epsilon=1e-06)
    model.compile(optimizer=ada, loss={'output':'categorical_crossentropy'})
    model.summary()
    if train:
        json_string = model.to_json()
        open('exp_architecture.json', 'w').write(json_string)
    return model

def fit_model(batch_size,lr, activation, nb_filter, filter_length1, filter_length2, filter_length3,
              WE, pos_WE, conn_WE,word_dim, pos_dim,conn_dim,dist_dim,
              X_train_1, X_train_2, X_train_pos_1, X_train_pos_2, X_train_conn,X_train_dist, X_train_ifconn, y_train,
              X_dev_1, X_dev_2, X_dev_pos_1, X_dev_pos_2, X_dev_conn,X_dev_dist, X_dev_ifconn,y_dev,train=True):
    nb_epoch = 80
    # callback each epoch:
    def onehot2num(y):
        y_num=[]
        y_sense=[]
        for x in y:
            index=22
            for i in range(len(x)):
                if x[i]==1:
                    index=i
                    continue
            if index==22:
                print (x)
            sense = exp_config.Label_To_Sense[index]
            y_num.append(index)
            y_sense.append(sense)
        return y_num,y_sense

    def TMP_equal_array(x,y):
        #print("x:",x,"||y:",y)
        if len(x) != len(y):
            return False
        for i in range(len(x)):
            if x[i] != y[i]:
                return False
        return True

    def TMP_to_one(x):
        index = np.argmax(x)
        # print(x,index)
        ret = [0. for i in range(len(x))]
        ret[index] = 1.
        return ret

    class scorer(Callback):
        dev_best_acc = 0
        dev_epoch_th = 0
        def on_epoch_end(self, epoch, logs={}):
            dev_output = model.predict({'arg1': X_dev_1, 'arg2': X_dev_2, 'pos1': X_dev_pos_1, 'pos2': X_dev_pos_2,
                'conn':X_dev_conn,'dist':X_dev_dist,'ifconn':X_dev_ifconn},
                                       batch_size=batch_size)['output']
            acc_dev = (len([1 for i in range(len(y_dev)) if (TMP_equal_array(TMP_to_one(dev_output[i]),y_dev[i]))])) / len(y_dev)
            sys.stdout.flush()
            print()
            print('Dev accuracy is:', round(acc_dev, 4), " at ", epoch)
            if acc_dev > scorer.dev_best_acc:
                scorer.dev_best_acc = np.round(acc_dev, 4)
                scorer.dev_epoch_th = epoch + 1
                print("saving the best model-----the best dev is: ",scorer.dev_best_acc)
                model.save_weights('explicit_cnn_weights.h5' ,overwrite=True)
            if epoch % 3 == 0:
                print('the best dev is explicit_cnn_weights.h5:',nb_filter, filter_length1, filter_length2, filter_length3, 'epoch', scorer.dev_epoch_th, 'dev_best_acc:', scorer.dev_best_acc)
            print()
            sys.stdout.flush()
        def on_train_end(self, logs={}):
            print('the final best dev is:', 'dev_epoch', nb_filter, filter_length1, filter_length2, filter_length3,scorer.dev_epoch_th, 'dev_best_acc:', scorer.dev_best_acc)
    scorer = scorer()
    stop = EarlyStopping(patience=10, verbose=1)
    print('Train...')
    model = build_model(lr, activation, nb_filter, filter_length1, filter_length2, filter_length3,
              WE, pos_WE, conn_WE,word_dim, pos_dim,conn_dim,dist_dim,ifconn_dim=2,
              ndims = 50,pos_ndims = 50,conn_ndims=50,dist_ndims=10,ifconn_ndims=10,
                        pool_length = 120,maxlen = 120,train=True)
    model.fit({'arg1': X_train_1, 'arg2': X_train_2, 'pos1': X_train_pos_1, 'pos2': X_train_pos_2,
               'conn':X_train_conn,'dist':X_train_dist,'ifconn':X_train_ifconn,'output': y_train},
              callbacks = [scorer, stop],batch_size = batch_size, shuffle = True,nb_epoch = nb_epoch,
              validation_data = ({'arg1': X_dev_1, 'arg2': X_dev_2, 'pos1': X_dev_pos_1, 'pos2': X_dev_pos_2,
                'conn':X_dev_conn,'dist':X_dev_dist,'ifconn':X_dev_ifconn,'output': y_dev}),show_accuracy=True)

    dev_best_acc = scorer.dev_best_acc
    dev_epoch_th = scorer.dev_epoch_th
    return (dev_epoch_th, dev_best_acc)

if __name__ == '__main__':
    WE, pos_WE, conn_WE,word_dim, pos_dim,conn_dim,dist_dim,\
    X_train_1, X_train_2, X_train_pos_1, X_train_pos_2, X_train_conn,X_train_dist, X_train_ifconn,y_train,\
    X_dev_1, X_dev_2, X_dev_pos_1, X_dev_pos_2, X_dev_conn,X_dev_dist, X_dev_ifconn,y_dev = pretainning()
    activation = "tanh"
    batch_size = 128
    lr = 0.01
    final = []
    nb_filter_list = [128,256]
    filter_list = [(2,2,2),(2,5,10),(3,10,15),(2,4,8)]
    for nb_filter in nb_filter_list:
        for filter_length1, filter_length2, filter_length3 in filter_list:
            '''  train '''
            dev_epoch_th, dev_best_acc = \
            fit_model(batch_size,lr, activation, nb_filter, filter_length1, filter_length2, filter_length3,
                  WE, pos_WE, conn_WE,word_dim, pos_dim,conn_dim,dist_dim,
                  X_train_1, X_train_2, X_train_pos_1, X_train_pos_2, X_train_conn,X_train_dist, X_train_ifconn, y_train,
                  X_dev_1, X_dev_2, X_dev_pos_1, X_dev_pos_2, X_dev_conn,X_dev_dist, X_dev_ifconn,y_dev,train=True)
            print('the final results is : ',dev_epoch_th,nb_filter, filter_length1, filter_length2, filter_length3,dev_best_acc)
            final.append((filter_length1, filter_length2, filter_length3,dev_best_acc))
            print(final)
            if dev_best_acc>0.454:
                break