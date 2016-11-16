from keras.models import Graph
from keras.layers.core import Dense, Activation, Flatten,Dropout,Reshape
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.preprocessing import sequence
from keras.layers.embeddings import Embedding
from keras.optimizers import Adagrad


def build_model(lr, activation, nb_filter, filter_length1, filter_length2, filter_length3,
          WE=None, pos_WE=None, word_dim=35397, pos_dim=45,ndims = 300,pos_ndims=100,pool_length = 120,maxlen = 120,train=True,):

    model = Graph()
    model.add_input(name='arg1', input_shape=(maxlen,), dtype=int)
    model.add_input(name='arg2', input_shape=(maxlen,), dtype=int)
    model.add_input(name='pos1', input_shape=(maxlen,), dtype=int)
    model.add_input(name='pos2', input_shape=(maxlen,), dtype=int)

    # our vocab indices into embedding_dims dimensions
    if (WE is not None):
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, weights=[WE], output_dim=ndims, mask_zero=True),
            name='embedding1', input='arg1')
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, weights=[WE], output_dim=ndims, mask_zero=True),
            name='embedding2', input='arg2')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen, weights=[pos_WE], output_dim=pos_ndims, mask_zero=True),
            name='embedding3', input='pos1')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen, weights=[pos_WE], output_dim=pos_ndims, mask_zero=True),
            name='embedding4', input='pos2')
    else:
        model.add_node(
        Embedding(input_dim=word_dim + 1, input_length=maxlen, output_dim=ndims, mask_zero=True),
        name='embedding1', input='arg1')
        model.add_node(
            Embedding(input_dim=word_dim + 1, input_length=maxlen, output_dim=ndims, mask_zero=True),
            name='embedding2', input='arg2')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen, output_dim=pos_ndims, mask_zero=True),
            name='embedding3', input='pos1')
        model.add_node(
            Embedding(input_dim=pos_dim + 1, input_length=maxlen,  output_dim=pos_ndims, mask_zero=True),
            name='embedding4', input='pos2')
    model.add_node(Dropout(0.25), merge_mode='concat', concat_axis=2, name='arg_1', inputs=['embedding1', 'embedding3'])
    model.add_node(Dropout(0.25), merge_mode='concat', concat_axis=2, name='arg_2', inputs=['embedding2', 'embedding4'])

    model.add_shared_node(Convolution1D(nb_filter=nb_filter,
                                        filter_length=filter_length1,
                                        border_mode='same',
                                        activation=activation,
                                        subsample_length=1), inputs=['arg_1', 'arg_2'], name='cnn1',
                          merge_mode='concat')

    model.add_shared_node(Convolution1D(nb_filter=nb_filter,
                                        filter_length=filter_length2,
                                        border_mode='same',
                                        activation=activation,
                                        subsample_length=1), inputs=['arg_1', 'arg_2'], name='cnn2',
                          merge_mode='concat')

    model.add_shared_node(Convolution1D(nb_filter=nb_filter,
                                        filter_length=filter_length3,
                                        border_mode='same',
                                        activation=activation,
                                        subsample_length=1), inputs=['arg_1', 'arg_2'], name='cnn3',
                          merge_mode='concat')
    # we use standard max pooling (halving the output of the previous layer):

    model.add_node(MaxPooling1D(pool_length=pool_length), name='mpooling1', input='cnn1')
    model.add_node(MaxPooling1D(pool_length=pool_length), name='mpooling2', input='cnn2')
    model.add_node(MaxPooling1D(pool_length=pool_length), name='mpooling3', input='cnn3')
    model.add_node(Flatten(), name='f1', input='mpooling1')
    model.add_node(Flatten(), name='f2', input='mpooling2')
    model.add_node(Flatten(), name='f3', input='mpooling3')

    model.add_node(Dense(20),name='final', inputs=['f1','f2','f3'],merge_mode='concat')
    model.add_node(Activation('softmax'),name='lastDim',input='final')
    model.add_output(name='output', input = 'lastDim')

    ada = Adagrad(lr=lr, epsilon=1e-06)
    model.compile(optimizer=ada, loss={'output':'categorical_crossentropy'})
    model.summary()
    # if train:
    #     json_string = model.to_json()
    #     open('1-2-5_1024_weights.h5', 'w').write(json_string)
    return model
