#coding:utf-8
from model_trainer.mallet_classifier import *
from model_trainer.Implicit_classifier.make_feature_file import non_explicit_make_feature_file, non_explicit_make_feature_file_train
from model_trainer.Implicit_classifier.feature_functions import *
from pdtb_parse import PDTB_PARSE
from model_trainer.Implicit_classifier import evaluation


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
        cm =evaluation.get_evaluation(self.dev_result_file_path)
        cm.print_out()
        # print ("\n" + "-"*80 + "\n")
        # evaluation.do_my_evaluation()

if __name__ == "__main__":

    feature_function_list = [
        word_pairs,
        production_rules, dependency_rules,
        firstlast_first3,
        polarity,
        modality,
        verbs,
        brown_cluster_pair,
        Inquirer,
        MPQA_polarity,
        prev_context_conn
    ]


    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    ''' train & dev feature output path '''
    train_feature_path = config.IMPLICIT_TRAIN_FEATURE_OUTPUT_PATH
    dev_feature_path = config.IMPLICIT_DEV_FEATURE_OUTPUT_PATH

    ''' classifier '''
    classifier = Mallet_classifier(NaiveBayes())

    ''' model path '''
    model_path = config.IMPLICIT_CLASSIFIER_MODEL

    ''' dev_result_file_path'''
    dev_result_file_path = config.IMPLICIT_DEV_OUTPUT_PATH

    '''---- trainer ---- '''
    trainer = Trainer(classifier, model_path, feature_function_list, train_feature_path, dev_feature_path, dev_result_file_path)
    #特征
    trainer.make_feature_file(train_pdtb_parse, dev_pdtb_parse)
    #训练
    trainer.train_mode()
    #测试
    trainer.test_model()
    #结果
    trainer.get_evaluation()


    pass