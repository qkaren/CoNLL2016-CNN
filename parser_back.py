#coding:utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import parser_util
import config

from model_trainer.connective_classifier.feature_functions \
    import all_features as _conn_clf_feature_function

from model_trainer.arg_position_classifier.feature_functions\
    import all_features as _arg_position_feature_function

from model_trainer.NT_arg_extractor.feature_functions \
    import all_features as _constituent_feat_func

from model_trainer.Explicit_classifier.feature_functions \
    import all_features as _explicit_feat_func

from model_trainer.Non_Explicit_classifier.feature_functions \
    import all_features as _non_explicit_feat_func

from model_trainer.Non_Explicit_classifier.feature_functions \
    import prev_context_conn

from model_trainer.Attribution_Span_Laber.non_connective.feature_functions \
    import all_features as _attribution_feat_func

from model_trainer.PS_Arg2_extractor.feature_functions \
    import all_features as _ps_arg2_extractor_feat_func

from model_trainer.PS_Arg1_extractor.feature_functions \
    import all_features as _ps_arg1_extractor_feat_func

from model_trainer.Implicit_Arg1_extractor.feature_functions \
    import all_features as _implicit_arg1_feat_func

from model_trainer.Implicit_Arg2_extractor.feature_functions \
    import all_features as _implicit_arg2_feat_func

import codecs

class DiscourseParser():
    def __init__(self, input_dataset, input_run):
        self.pdtb_parse = '%s/pdtb-parses.json' % input_dataset
        self.raw_path = '%s/raw' % input_dataset
        self.input_run = input_run
        self.relations = []
        self.explicit_relations = []
        self.non_explicit_relations = []

        self.documents = json.loads(codecs.open(self.pdtb_parse, encoding="utf-8", errors="ignore").read())
        # self.documents = json.loads(open(self.pdtb_parse).read())
        self.parse_dict = self.documents

        pass

    def parse(self):

        # add paragraph info
        parser_util.add_paragraph_info_for_parse(self.parse_dict, self.raw_path)

        ''' step 1 '''

        # 获取所有连接词 [(DocID, sent_index, conn_indices), ()..]
        conns_list = parser_util.get_all_connectives(self.documents)


        ''' 1.1 Connective classifier '''

        conn_clf_feature_function = _conn_clf_feature_function
        conn_clf_feat_path = config.PARSER_CONN_CLF_FEATURE
        conn_clf_model_path = config.CONNECTIVE_CLASSIFIER_MODEL
        conn_clf_model_output = config.PARSER_CONN_CLF_MODEL_OUTPUT

        # 为每个连接词抽取特征。
        parser_util.conn_clf_print_feature(self.parse_dict, conns_list, conn_clf_feature_function, conn_clf_feat_path)
        # 特征放入model,
        parser_util.put_feature_to_model(conn_clf_feat_path, conn_clf_model_path, conn_clf_model_output)
        # 读取model_output, 得到语篇连接词
        conns_list = parser_util.conn_clf_read_model_output(conn_clf_model_output, conns_list)

        ''' 1.2.1 Argument position classifier '''
        arg_position_feat_func = _arg_position_feature_function
        arg_position_feat_path = config.PARSER_ARG_POSITION_FEATURE
        arg_position_model_path = config.ARG_POSITION_CLASSIFIER_MODEL
        arg_position_model_output = config.PARSER_ARG_POSITION_MODEL_OUTPUT

        # 为每个语篇连接词抽取特征
        parser_util.arg_position_print_feature(self.parse_dict, conns_list, arg_position_feat_func, arg_position_feat_path)
        # 特征放入model,
        parser_util.put_feature_to_model(arg_position_feat_path, arg_position_model_path, arg_position_model_output)
        # 读取model output ,将  conns_list 分为两类 SS_conns_list , PS_conns_list
        SS_conns_list, PS_conns_list = parser_util.arg_position_read_model_output(arg_position_model_output, conns_list)


        ''' 1.2.2 Argument extractor '''

        # SS 分成 SS_conns_parallel : if then either or 和 SS_conns_not_parallel : and or
        SS_conns_parallel_list, SS_conns_not_parallel_list = parser_util.divide_SS_conns_list(SS_conns_list)

        constituent_feat_func = _constituent_feat_func
        constituent_feat_path = config.PARSER_CONSTITUENT_FEATURE
        constituent_model_path = config.NT_CLASSIFIER_MODEL
        constituent_model_output = config.PARSER_CONSTITUENT_MODEL_OUTPUT

        # 每个SS_conns_not_parallel的连接词，所在的句子，获取connective对象
        connectives = parser_util.get_all_connectives_for_NT(self.parse_dict, SS_conns_not_parallel_list)
        # 为每一个 constituent 抽取特征
        parser_util.constituent_print_feature(self.parse_dict, connectives, constituent_feat_func, constituent_feat_path)
        # 特征放入model
        parser_util.put_feature_to_model(constituent_feat_path, constituent_model_path, constituent_model_output)
        # 读取model output，得到SS_conns_not_parallel 的两个arg,将list变成[("SS", DocID, sent_index, conn_indices,Arg1,Arg2)]
        SS_conns_not_parallel_list_args = \
            parser_util.constituent_read_model_output(
                constituent_feat_path, constituent_model_output, self.parse_dict, SS_conns_not_parallel_list)
        # 为SS_conns_parallel_list 获取Arg1, Arg2
        SS_conns_parallel_list_args = parser_util.get_Args_for_SS_parallel_conns(self.parse_dict, SS_conns_parallel_list)
        #为PS 获取Arg1, Arg2
        PS_conns_list_args = parser_util.get_Args_for_PS_conns(self.parse_dict, PS_conns_list)

        ''' Explicit classifier '''
        #[(source, DocID, sent_index, conn_indices, Arg1, Arg2)...]
        conns_list_args = SS_conns_not_parallel_list_args + SS_conns_parallel_list_args + PS_conns_list_args

        explicit_feat_func = _explicit_feat_func
        explicit_feat_path = config.PARSER_EXPLICIT_CLF_FEATURE
        explicit_model_path = config.EXPLICIT_CLASSIFIER_MODEL
        explicit_model_output = config.PARSER_EXPLICIT_CLF_MODEL_OUTPUT

        # 抽取相应特征
        parser_util.explicit_clf_print_feature(self.parse_dict, conns_list_args, explicit_feat_func, explicit_feat_path)
        # 特征放入分类器
        parser_util.put_feature_to_model(explicit_feat_path, explicit_model_path, explicit_model_output)
        # 读取model output，得到 conns_list_args_rel =[(source, DocID, sent_index, conn_indices, Arg1, Arg2, sense)]
        conns_args_sense_list = parser_util.explicit_clf_read_model_output(explicit_model_output, conns_list_args)

        ''' Explicit relation '''
        #ss的已经设置好Arg1,Arg2. PS要识别Attribution
        SS_explicit_relations, PS_explicit_relations = parser_util.get_explicit_relations(self.parse_dict, conns_args_sense_list)

        ''' Explicit PS Arg2 extractor '''

        PS_Arg2_feat_func = _ps_arg2_extractor_feat_func
        PS_Arg2_feat_path = config.PARSER_PS_ARG2_FEATURE
        PS_Arg2_model_path = config.PS_ARG2_CLASSIFIER_MODEL
        PS_Arg2_model_output = config.PARSER_PS_ARG2_MODEL_OUTPUT

        #抽取相应的特征
        parser_util.ps_arg2_extractor_print_feature \
            (self.parse_dict, PS_explicit_relations, PS_Arg2_feat_func, PS_Arg2_feat_path)
        #特征放入分类器
        parser_util.put_feature_to_model(PS_Arg2_feat_path, PS_Arg2_model_path, PS_Arg2_model_output)
        # 读取model output, 获取PS的Arg2，不去处理Arg1, relation['Connective']['TokenList']
        # 只处理 relation['Arg2']['TokenList']
        PS_explicit_relations = parser_util.ps_arg2_extractor_read_model_output(
            PS_Arg2_feat_path, PS_Arg2_model_output, self.parse_dict, PS_explicit_relations)

        ''' Explicit PS Arg1 extractor '''

        PS_Arg1_feat_func = _ps_arg1_extractor_feat_func
        PS_Arg1_feat_path = config.PARSER_PS_ARG1_FEATURE
        PS_Arg1_model_path = config.PS_ARG1_CLASSIFIER_MODEL
        PS_Arg1_model_output = config.PARSER_PS_ARG1_MODEL_OUTPUT

        #抽取相应的特征
        parser_util.ps_arg1_extractor_print_feature \
            (self.parse_dict, PS_explicit_relations, PS_Arg1_feat_func, PS_Arg1_feat_path)
        #特征放入分类器
        parser_util.put_feature_to_model(PS_Arg1_feat_path, PS_Arg1_model_path, PS_Arg1_model_output)
        # 读取model output, 获取PS的Arg1，处理relation['Connective']['TokenList']
        PS_explicit_relations = parser_util.ps_arg1_extractor_read_model_output(
            PS_Arg1_feat_path, PS_Arg1_model_output, self.parse_dict, PS_explicit_relations)

        ''' explicit relation 完成'''
        self.explicit_relations = SS_explicit_relations + PS_explicit_relations

        # 测试 explicit
        parser_util.test_explicit_relations(self.explicit_relations)

        ''' Non-Explicit classifier '''
        # 获取所有相邻的，但没有explicit relation 的句子对，[(DocID,sent1_index,sent2_index) ]
        adjacent_non_exp_list = parser_util.get_adjacent_non_exp_list(self.parse_dict, PS_conns_list)

        # 通过[(DocID,sent1_index,sent2_index) ] 获得 non_explicit_relations(无sense), Token_list 有所不同
        self.non_explicit_relations = parser_util.get_non_explicit_relations(self.parse_dict, adjacent_non_exp_list)

        non_explicit_feat_func = _non_explicit_feat_func
        non_explicit_feat_path = config.PARSER_NON_EXPLICIT_CLF_FEATURE
        non_explicit_model_path = config.NON_EXPLICIT_CLASSIFIER_MODEL
        non_explicit_model_output = config.PARSER_NON_EXPLICIT_CLF_MODEL_OUTPUT

        #  为implicit 提供 explicit 的上下文
        implicit_context_dict = parser_util.get_implicit_context_dict(self.explicit_relations)

        # 抽取相应特征
        parser_util.non_explicit_clf_print_feature \
            (self.parse_dict, self.non_explicit_relations, non_explicit_feat_func, implicit_context_dict, prev_context_conn, non_explicit_feat_path)
        # 特征放入分类器
        parser_util.put_feature_to_model(non_explicit_feat_path, non_explicit_model_path, non_explicit_model_output)
        # 读取model output，给relation加sense，
        self.non_explicit_relations = parser_util.non_explicit_read_model_output(non_explicit_model_output, self.parse_dict, self.non_explicit_relations)

        #将self.non_explicit_relations 拆分，因为EntRel没有Attribution
        EntRel_relations, Implicit_AltLex_relations = parser_util.divide_non_explicit_relations(self.non_explicit_relations, self.parse_dict)

        ''' implicit Arg1 '''
        #识别implicit 中的 Arg1
        implicit_arg1_feat_func = _implicit_arg1_feat_func
        implicit_arg1_feat_path = config.PARSER_IMPLICIT_ARG1_FEATURE
        implicit_arg1_model_path = config.IMPLICIT_ARG1_CLASSIFIER_MODEL
        implicit_arg1_model_output = config.PARSER_IMPLICIT_ARG1_MODEL_OUTPUT

        # 抽取特征
        parser_util.implicit_arg1_print_feature \
            (self.parse_dict, Implicit_AltLex_relations, implicit_arg1_feat_func, implicit_arg1_feat_path)
        # 特征放入分类器
        parser_util.put_feature_to_model(implicit_arg1_feat_path, implicit_arg1_model_path, implicit_arg1_model_output)
        # 读取model output 给relation的Arg1 赋值
        Implicit_AltLex_relations = parser_util.implicit_arg1_read_model_output(
            implicit_arg1_feat_path, implicit_arg1_model_output, self.parse_dict, Implicit_AltLex_relations)

        ''' implicit Arg2 '''
        #识别implicit 中的 Arg2
        implicit_arg2_feat_func = _implicit_arg2_feat_func
        implicit_arg2_feat_path = config.PARSER_IMPLICIT_ARG2_FEATURE
        implicit_arg2_model_path = config.IMPLICIT_ARG2_CLASSIFIER_MODEL
        implicit_arg2_model_output = config.PARSER_IMPLICIT_ARG2_MODEL_OUTPUT

        # 抽取特征
        parser_util.implicit_arg2_print_feature \
            (self.parse_dict, Implicit_AltLex_relations, implicit_arg2_feat_func, implicit_arg2_feat_path)
        # 特征放入分类器
        parser_util.put_feature_to_model(implicit_arg2_feat_path, implicit_arg2_model_path, implicit_arg2_model_output)
        # 读取model output 给relation的Arg2 赋值
        Implicit_AltLex_relations = parser_util.implicit_arg2_read_model_output(
            implicit_arg2_feat_path, implicit_arg2_model_output, self.parse_dict, Implicit_AltLex_relations)


        self.non_explicit_relations = EntRel_relations + Implicit_AltLex_relations

        # 测试 non-explicit
        print "--" * 45
        print "未用抽取后的argument, 重新获取 sense"
        print "--" * 45

        parser_util.test_non_explicit_relations(self.non_explicit_relations)

        ''' 利用抽取后的argument，重新获取下 sense'''
        # 注意这里的relation的Argument, 原来的arg的token为doc_offset --> sent_index, sent_offset
        self.non_explicit_relations = parser_util.change_arg_doc_offset(self.non_explicit_relations, self.parse_dict)
                #  format for CNN
        CNN_input_file_path = "cnn.txt"
        parser_util.format_for_CNN(self.parse_dict, adjacent_non_exp_list, CNN_input_file_path)
        instances = parser_util.get_CNN_input(CNN_input_file_path)

        # 抽取相应特征
        parser_util.non_explicit_clf_print_feature \
            (self.parse_dict, self.non_explicit_relations, non_explicit_feat_func, implicit_context_dict, prev_context_conn, non_explicit_feat_path)
        # 特征放入分类器
        parser_util.put_feature_to_model(non_explicit_feat_path, non_explicit_model_path, non_explicit_model_output)
        # 读取model output，给relation加sense，
        self.non_explicit_relations = parser_util.non_explicit_read_model_output(non_explicit_model_output, self.parse_dict, self.non_explicit_relations)

        # 改变argument,  sent_index, sent_offset  --> doc_offset
        self.non_explicit_relations = parser_util.change_arg_sent_offset(self.non_explicit_relations, self.parse_dict)


        # 测试 non-explicit
        parser_util.test_non_explicit_relations(self.non_explicit_relations)

        ''' relations '''
        self.relations = self.explicit_relations + self.non_explicit_relations
        parser_util.test_relation(self.relations)





if __name__ == '__main__':
    # input_dataset = sys.argv[1]
    # input_run = sys.argv[2]
    # output_dir = sys.argv[3]

    input_dataset = config.CWD + "data/conll15-st-03-04-15-dev"
    input_run = ""
    output_dir = ""

    parser = DiscourseParser(input_dataset, input_run)
    parser.parse()

    relations = parser.relations

    # output = open('%s/output.json' % output_dir, 'w')
    # for relation in relations:
    #     output.write('%s\n' % json.dumps(relation))
    # output.close()

