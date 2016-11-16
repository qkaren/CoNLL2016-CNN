#coding:utf-8
from model_trainer.mallet_classifier import *
import conn_make_feature_file
from model_trainer.connective_classifier.feature_functions import *
from pdtb_parse import PDTB_PARSE
import conn_eval
import numpy as np
from operator import itemgetter

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
        print ("make %s feature file ..." % ("train"))
        conn_make_feature_file.make_feature_file(train_pdtb_parse, self.feature_function_list, self.train_feature_path)
        print ("make %s feature file ..." % ("dev"))
        conn_make_feature_file.make_feature_file(dev_pdtb_parse, self.feature_function_list, self.dev_feature_path)

    def train_mode(self):
        classifier.train_model(self.train_feature_path, self.model_path)

    def test_model(self):
        classifier.test_model(self.dev_feature_path, self.dev_result_file_path, self.model_path)

    def get_evaluation(self):
        cm =conn_eval.get_evaluation(self.dev_result_file_path)
        cm.print_out()
        # p, r, marco_f1 = cm.get_prf_for_all()

        # return np.nan_to_num(marco_f1) * 100


if __name__ == "__main__":

    feature_function_list = [all_features]

    # feature_function_list = [
    #     # '''Z.Lin'''
    #     CPOS,
    #     prev_C,
    #     prevPOS,
    #     prevPOS_CPOS,
    #     C_next,
    #     nextPOS,
    #     CPOS_nextPOS,
    #     CParent_to_root_path,
    #     compressed_CParent_to_root_path,
    #
    #     # Pitler
    #     self_category,
    #     parent_category,
    #     left_sibling_category,
    #     right_sibling_category,
    #     is_right_sibling_contains_VP,
    #     # conn - syn
    #     conn_self_category,
    #     conn_parent_category,
    #     conn_left_sibling_category,
    #     conn_right_sibling_category,
    #     # syn - syn
    #     self_parent,
    #     self_right,
    #     self_left,
    #     parent_left,
    #     parent_right,
    #     left_right,
    #
    #     # mine
    #     conn_lower_case,
    #     conn,
    #     CParent_to_root_path_node_names,
    #     conn_connCtx,
    #     conn_rightSiblingCtx,
    #     conn_parent_category_Ctx
    # ]


    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse = PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    ''' train & dev feature output path '''
    train_feature_path = config.CONNECTIVE_TRAIN_FEATURE_OUTPUT_PATH
    dev_feature_path = config.CONNECTIVE_DEV_FEATURE_OUTPUT_PATH

    ''' classifier '''
    classifier = Mallet_classifier(MaxEnt())

    ''' model path '''
    model_path = config.CONNECTIVE_CLASSIFIER_MODEL

    ''' dev_result_file_path'''
    dev_result_file_path = config.CONNECTIVE_DEV_OUTPUT_PATH

    '''---- trainer ---- '''
    trainer = Trainer(classifier, model_path, feature_function_list, train_feature_path, dev_feature_path, dev_result_file_path)
    #特征
    trainer.make_feature_file(train_pdtb_parse, dev_pdtb_parse)
    #训练
    trainer.train_mode()
    # #测试
    trainer.test_model()
    #结果
    trainer.get_evaluation()


    # best_feature_list = []
    # dict_feat_functions_to_score = {}
    # curr_best_score = -1
    # curr_best_features = ""
    #
    # while len(best_feature_list) != len(feature_function_list):
    #     T = list(set(feature_function_list) - set(best_feature_list))
    #     score = [0] * len(T)
    #     for index, feat_func in enumerate(T):
    #
    #         train_feature_function_list = best_feature_list + [feat_func]
    #         trainer = Trainer(classifier, model_path, train_feature_function_list, train_feature_path, dev_feature_path, dev_result_file_path)
    #         #特征
    #         trainer.make_feature_file(train_pdtb_parse, dev_pdtb_parse)
    #         #训练
    #         trainer.train_mode()
    #         #测试
    #         trainer.test_model()
    #         #结果
    #         marco_f1 = trainer.get_evaluation()
    #         score[index] = marco_f1
    #
    #         if marco_f1 > curr_best_score:
    #             curr_best_score = marco_f1
    #             curr_best_features = " ".join([func.__name__ for func in train_feature_function_list])
    #
    #         print ("##" * 45)
    #         print ("Current Best : %.2f" % curr_best_score)
    #         print ("Current Best Features: %s" % curr_best_features)
    #         print ("##" * 45)
    #
    #         # 加入字典
    #         feat_func_name = " ".join([func.func_name for func in train_feature_function_list])
    #         dict_feat_functions_to_score[feat_func_name] = marco_f1
    #
    #
    #     # 将最好的放入 best_feature_list
    #     best_index = score.index(max(score))
    #     best_feature_list.append(T[best_index])
    #
    # #将各种特征的组合及对应的score写入文件, 按sore降排
    # fout = open("result.txt", "w")
    # for func_names, score in sorted(dict_feat_functions_to_score.iteritems(), key= itemgetter(1), reverse=True):
    #     fout.write("%s : %.2f\n" % (func_names, score))
    # fout.close()

    pass