#coding:utf-8
from model_trainer.mallet_classifier import *
from model_trainer.Non_Explicit_classifier.make_feature_file import non_explicit_make_feature_file, non_explicit_make_feature_file_train
from model_trainer.Non_Explicit_classifier.feature_functions import *
from pdtb_parse import PDTB_PARSE
from model_trainer.Non_Explicit_classifier import evaluation



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
        # cm.print_out()
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
        prev_context_conn,

        # EntRel
        # have_all_case,

        # arg_tense_pair,
        # arg1_tense,
        # arg2_tense,
        #
        # arg_first3_conn_pair,
        arg1_first3_conn,
        # arg2_first3_conn,


        # word2vec_predicted_conn_1,
        # word2vec_predicted_conn_2
        # LM_exp_conn2_from_file,
        # LM_exp_conn1_from_file,
        # LM_conn,
        # LM_impl_conn_1_from_file,
        # LM_impl_conn_2_from_file
        # prev_context_sense,
        #
        # prev_context_conn_sense,
        #
        # next_context_conn,
        #
        # prev_next_context_conn,

        # verb_pair,

        # arg_brown_cluster,

        # MPQA_polarity_score,
        # MPQA_polarity_no_strong_weak,
        # main_verb_pair
        # money_date_percent,
        # Arg_word2vec
        # cp_production_rules
        # word2vec_cluster_pair,
    ]

    # feature_function_list = [
    #     # LM_conn,
    #     # LM_impl_conn_1_from_file,
    #     # LM_impl_conn_2,
    #     # LM_exp_conn_1,
    #     # LM_impl_conn_2_from_file,
    #     # LM_exp_conn_2
    #     LM_exp_conn_3
    # ]

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
    trainer.make_feature_file(train_pdtb_parse, dev_pdtb_parse)
    #训练
    trainer.train_mode()
    #测试
    trainer.test_model()
    #结果
    trainer.get_evaluation()


    pass