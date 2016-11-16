#coding:utf-8
from model_trainer.mallet_classifier import *
from make_feature_file import comp_contrast_make_feature_file, comp_contrast_make_feature_file_train
from model_trainer.Non_Explicit_classifier.feature_functions import *
from pdtb_parse import PDTB_PARSE
import evaluation
import numpy as np


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
        comp_contrast_make_feature_file_train(train_pdtb_parse, self.feature_function_list, self.train_feature_path)
        print("make %s feature file ..." % ("dev"))
        comp_contrast_make_feature_file(dev_pdtb_parse, self.feature_function_list, self.dev_feature_path)

    def train_mode(self):
        print(self.train_feature_path, self.model_path)
        classifier.train_model(self.train_feature_path, self.model_path)

    def test_model(self):
        classifier.test_model(self.dev_feature_path, self.dev_result_file_path, self.model_path)

    def get_evaluation(self):
        pass
        cm =evaluation.get_evaluation(self.dev_result_file_path)
        cm.print_out()

        evaluation.write_result_to_file(cm, self.feature_function_list, "EntRel_1_f1_Maxent_result.txt")

        # p, r, f1 = cm.get_average_prf()
        # return np.nan_to_num(f1)

        # 1 的f1 排序
        p, r, f1 = cm.get_prf("1")
        return np.nan_to_num(f1)

        # print "\n" + "-"*80 + "\n"
        # evaluation.do_my_evaluation()

if __name__ == "__main__":




    feature_function_list = [
        # word_pairs,
        production_rules, dependency_rules,
        firstlast_first3,
        # polarity,
        modality,
        verbs,
        brown_cluster_pair,
        Inquirer,
        MPQA_polarity,
        #
        # # arg_tense_pair,
        # # arg1_tense,
        # # arg2_tense,
        # #
        # arg_first3_conn_pair,
        # arg1_first3_conn,
        # arg2_first3_conn,

        verb_pair

        # MPQA_polarity_score,
        # MPQA_polarity_no_strong_weak,
        # main_verb_pair
        # money_date_percent,
        # Arg_word2vec
        # cp_production_rules
        # word2vec_cluster_pair,
    ]

    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    ''' train & dev feature output path '''
    train_feature_path = config.COMP_CONTRAST_TRAIN_FEATURE_OUTPUT_PATH
    dev_feature_path = config.COMP_CONTRAST_DEV_FEATURE_OUTPUT_PATH


    ''' classifier '''
    classifier = Mallet_classifier(MaxEnt())

    ''' model path '''
    model_path = config.COMP_CONTRAST_CLASSIFIER_MODEL

    ''' dev_result_file_path'''
    dev_result_file_path = config.COMP_CONTRAST_DEV_OUTPUT_PATH

    '''---- trainer ---- '''
    best_feature_list = []

    while len(best_feature_list) != len(feature_function_list):
        T = list(set(feature_function_list) - set(best_feature_list))
        score = [0] * len(T)
        for index, feat_func in enumerate(T):

            train_feature_function_list = best_feature_list + [feat_func]
            trainer = Trainer(classifier, model_path, train_feature_function_list, train_feature_path, dev_feature_path, dev_result_file_path)
            #特征
            trainer.make_feature_file(train_pdtb_parse, dev_pdtb_parse)
            #训练
            trainer.train_mode()
            #测试
            trainer.test_model()
            #结果
            f1 = trainer.get_evaluation()
            score[index] = f1

        # 将最好的放入 best_feature_list
        best_index = score.index(max(score))
        best_feature_list.append(T[best_index])


    pass