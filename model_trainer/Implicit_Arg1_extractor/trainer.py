#coding:utf-8
from model_trainer.mallet_classifier import *
from model_trainer.Implicit_Arg1_extractor.make_feature_file import implicit_arg1_make_feature_file
from model_trainer.Implicit_Arg1_extractor.feature_functions import *
from pdtb_parse import PDTB_PARSE
from model_trainer.Implicit_Arg1_extractor import evaluation
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
        print("make %s feature file ..." % ("train"))
        implicit_arg1_make_feature_file(train_pdtb_parse, self.feature_function_list, self.train_feature_path)
        print("make %s feature file ..." % ("dev"))
        implicit_arg1_make_feature_file(dev_pdtb_parse, self.feature_function_list, self.dev_feature_path)


    def train_mode(self):
        classifier.train_model(self.train_feature_path, self.model_path)

    def test_model(self):
        classifier.test_model(self.dev_feature_path, self.dev_result_file_path, self.model_path)

    def get_evaluation(self):
        cm =evaluation.get_evaluation(self.dev_result_file_path)
        cm.print_out()
        Arg1_Acc = evaluation.get_Arg1_Acc(self.dev_feature_path, self.dev_result_file_path)
        print("Arg1_Acc: %.2f" % Arg1_Acc)
        return Arg1_Acc

if __name__ == "__main__":


    # feature_function_list = [all_features]

    # feature_function_list = [
    #     # lowercase_verbs,
    #     # lemma_verbs,
    #     # curr_first,
    #     curr_last,
    #     prev_last,
    #     # next_first,
    #     # prev_last_curr_first,
    #     # curr_last_next_first,
    #     # position,
    #     # production_rule,
    #     # is_curr_NNP_prev_PRP_or_NNP,
    #     # prev_curr_production_rule,
    #     prev_curr_CP_production_rule,
    #     # curr_next_CP_production_rule,
    #     # prev2_pos_lemma_verb,
    #     curr_first_to_prev_last_path,
    #     clause_word_num,
    #     # is_NNP_WP,
    #
    # ]

    # # NaiveBayes best, arg1 acc : 68.41
    # feature_function_list = [
    #     lowercase_verbs,
    #     next_first,
    #     prev_curr_CP_production_rule,
    #     prev2_pos_lemma_verb,
    # ]

    # MaxEnt , arg1 acc : 69.82
    # feature_function_list = [
    #     prev_curr_CP_production_rule,
    #     curr_last,
    # ]

    # MaxEnt , arg1 acc : 70.02
    feature_function_list = [
        prev_curr_CP_production_rule,
        curr_last,
        is_NNP_WP,
        is_curr_NNP_prev_PRP_or_NNP,
        clause_word_num,
        prev2_pos_lemma_verb,
        lemma_verbs
    ]




    ''' train & dev pdtb parse'''
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)

    ''' train & dev feature output path '''
    train_feature_path = config.IMPLICIT_ARG1_TRAIN_FEATURE_OUTPUT_PATH
    dev_feature_path = config.IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH

    ''' classifier '''
    classifier = Mallet_classifier(MaxEnt())

    ''' model path '''
    model_path = config.IMPLICIT_ARG1_CLASSIFIER_MODEL

    ''' dev_result_file_path'''
    dev_result_file_path = config.IMPLICIT_ARG1_DEV_OUTPUT_PATH

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

    # best_feature_list = []
    #
    # dict_feat_functions_to_score = {}
    #
    # while len(best_feature_list) <= len(feature_function_list):
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
    #         Arg1_Acc = trainer.get_evaluation()
    #         score[index] = Arg1_Acc
    #
    #         # 加入字典
    #         feat_func_name = " ".join([func.func_name for func in train_feature_function_list])
    #         dict_feat_functions_to_score[feat_func_name] = Arg1_Acc
    #
    #
    #     # 将最好的放入 best_feature_list
    #     best_index = score.index(max(score))
    #     best_feature_list.append(T[best_index])
    #
    # #将各种特征的组合及对应的score写入文件, 按sore降排
    # fout = open("result.txt", "w")
    # for func_names, score in sorted(dict_feat_functions_to_score.iteritems(), key=itemgetter(1), reverse=True):
    #     fout.write("%s : %.2f\n" % (func_names, score))
    # fout.close()


    pass