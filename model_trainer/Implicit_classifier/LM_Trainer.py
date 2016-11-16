#coding:utf-8
import sys
sys.path.append("/home/jianxiang/SDP/conll15st")
from model_trainer.mallet_classifier import *
from .feature_functions import *
from pdtb_parse import PDTB_PARSE
from . import evaluation
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file



def non_explicit_make_feature_file_train(pdtb_parse, feature_function_list, top_n, to_file):
    print("为 non_explicit 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

        features = []
        for feature_function in feature_function_list:
            feature = feature_function(relation, parse_dict, top_n)
            features.append(feature)

        #合并特征
        feature = mergeFeatures(features)
        #特征target
        if len(relation["Sense"]) == 1:
            sense = relation["Sense"][0]#暂时取第一个
            target = config.Sense_To_Label[sense]
            #example
            example = Example(target, feature)
            example.comment = "%s" % (relation["ID"])

            example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))

def non_explicit_make_feature_file(pdtb_parse, feature_function_list, top_n, to_file):
    print("为 non_explicit 抽取特征.\n" + "-"*120)
    print(" %s " % (" || ".join([f.__name__ for f in feature_function_list])))
    print("-" * 120)

    parse_dict = pdtb_parse.parse_dict

    relations = pdtb_parse.pdtb.non_explicit_relations

    example_list = []

    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        print("process: %.2f%%.\r" % ((curr_index + 1)/total*100), end=' ')

        features = []
        for feature_function in feature_function_list:
            feature = feature_function(relation, parse_dict, top_n)
            features.append(feature)

        #合并特征
        feature = mergeFeatures(features)
        #特征target
        sense = relation["Sense"][0]#暂时取第一个
        target = config.Sense_To_Label[sense]
        #example
        example = Example(target, feature)
        example.comment = "%s" % (relation["ID"])

        example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print("non_explicit特征已经写入文件：%s ." % (to_file))


class Trainer:
    def __init__(self, classifier, model_path, feature_function_list,
                 train_feature_path ,dev_feature_path, dev_result_file_path):
        self.classifier = classifier
        self.model_path = model_path
        self.feature_function_list = feature_function_list
        self.train_feature_path = train_feature_path
        self.dev_feature_path = dev_feature_path
        self.dev_result_file_path = dev_result_file_path

    def make_feature_file(self, train_pdtb_parse, dev_pdtb_parse):
        print("make %s feature file ..." % ("train"))
        non_explicit_make_feature_file_train(train_pdtb_parse, self.feature_function_list, self.train_feature_path)
        print("make %s feature file ..." % ("dev"))
        non_explicit_make_feature_file(dev_pdtb_parse, self.feature_function_list, self.dev_feature_path)

    def train_mode(self):
        print(self.train_feature_path, self.model_path)
        classifier.train_model(self.train_feature_path, self.model_path)

    def test_model(self):
        classifier.test_model(self.dev_feature_path, self.dev_result_file_path, self.model_path)

    def get_evaluation(self):
        pass
        F1 =evaluation.get_evaluation_LM(self.dev_result_file_path)

        return F1

if __name__ == "__main__":

    feature_function_list = [
        # LM_impl_conn_2_from_file_by_top_n,
        LM_exp_conn1_from_file_by_top_n
    ]

    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    ''' train & dev feature output path '''
    train_feature_path = config.NON_EXPLICIT_TRAIN_FEATURE_OUTPUT_PATH
    dev_feature_path = config.NON_EXPLICIT_DEV_FEATURE_OUTPUT_PATH

    ''' classifier '''
    classifier = Mallet_classifier(NaiveBayes())

    ''' model path '''
    model_path = config.NON_EXPLICIT_CLASSIFIER_MODEL

    ''' dev_result_file_path'''
    dev_result_file_path = config.NON_EXPLICIT_DEV_OUTPUT_PATH

    '''---- trainer ---- '''
    trainer = Trainer(classifier, model_path, feature_function_list, train_feature_path, dev_feature_path, dev_result_file_path)
    #特征

    curr_best_n = -1
    curr_best_f1 = -1

    #存入字典
    dict_top_n_f1 = {}

    top_n_list = list(range(1,200))

    for top_n in top_n_list:
        print("make %s feature file ..." % ("train"))
        non_explicit_make_feature_file_train(train_pdtb_parse, feature_function_list, top_n, train_feature_path)
        print("make %s feature file ..." % ("dev"))
        non_explicit_make_feature_file(dev_pdtb_parse, feature_function_list, top_n, dev_feature_path)

        #训练
        trainer.train_mode()
        #测试
        trainer.test_model()
        #结果
        F1 = trainer.get_evaluation()

        dict_top_n_f1[top_n] = F1

        if F1 >= curr_best_f1:
            curr_best_f1 = F1
            curr_best_n = top_n

        print("--" * 45)
        print("N : %d ; F1 %.2f" % (top_n, F1 * 100))
        print("--" * 45)

        print("##" * 45)
        print("curr best N : %s " % curr_best_n)
        print("curr best F1 : %.2f " % (curr_best_f1 * 100))

    # 降序, 放文件
    list_top_n_f1 = sorted(iter(dict_top_n_f1.items()), key=operator.itemgetter(1), reverse=True)
    #
    f_out = open("LM_exp_conn_1_result.txt","w")
    for top_n, f1 in list_top_n_f1:
        f_out.write("%d : %.2f\n" % (top_n, f1 * 100))
    f_out.close()


    pass