#coding:utf-8
from pdtb_parse import PDTB_PARSE
import config
import operator

def do_statistic():
    pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    # pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    relations = pdtb_parse.pdtb.explicit_relations


    # 纪录每个sense出现的次数
    dict = {}
    total = 0.0
    for relation in relations:
        for sense in relation["Sense"]:
            if sense not in dict:
                dict[sense] = 0
            dict[sense] += 1
            total += 1

    dict = sorted(iter(dict.items()), key=operator.itemgetter(1),reverse = True)
    print(total)
    for sense, freq in dict:
        print("%s" % (sense))
    for sense, freq in dict:
        print("%d" % (freq))
    for sense, freq in dict:
        print("%.2f" % (freq/total * 100))

def delete_non_explicit_sense(pdtb_file_path, delete_sense_set):
    import json
    pdtb_file = open(pdtb_file_path)
    relations = [json.loads(x) for x in pdtb_file]
    pdtb_file.close()
    temp = []

    for relation in relations:
        if relation["Type"] == "Explicit":
            temp.append(relation)
        else:
            flag = 0
            for sense in relation["Sense"]:
                if sense in delete_sense_set:
                    flag = 1
            if flag == 0:
                temp.append(relation)


    output = open(pdtb_file_path+".temp", 'w')
    for relation in temp:
        output.write('%s\n' % json.dumps(relation))
    output.close()


def print_instance(pdtb_parse, sense):
    relations = pdtb_parse.pdtb.non_explicit_relations
    for relation in relations:
        for _sense in relation["Sense"]:
            if _sense == sense:
                print("--" * 45)
                print(relation["Arg1"]["RawText"])
                # print "[%s]" % relation["Connective"]["RawText"],
                print(relation["Arg2"]["RawText"])
                print(relation["Connective"]["RawText"])
                print(sense)




if __name__ == "__main__":
    # delete_sense_list = ["Expansion.Alternative",
    #                     "Contingency.Condition",
    #                     "Contingency",
    #                     "Expansion.Exception",
    #                     "Contingency.Cause",
    #                     "Temporal"
    # ]
    # delete_non_explicit_sense(config.PDTB_TRAIN_PATH, set(delete_sense_list))

    # do_statistic()

    # pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pdtb_parse =  PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)

    # parse_dict = pdtb_parse.parse_dict
    #
    #
    # for DocID in parse_dict:
    #     for sent_index in range(len(parse_dict[DocID]["sentences"])):
    #         sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    #         # print DocID, sent_index
    #         sent_tokens = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)]
    #         sent_NER_Tag = [parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["NER_TAG"] for index in range(sent_length)]
    #
    #         print sent_tokens
    #         print sent_NER_Tag

    sense = "EntRel"
    print_instance(pdtb_parse, sense)

    Sense_To_Label = {
        'Temporal.Asynchronous.Precedence': '1',
		'Temporal.Asynchronous.Succession': '2',
		'Temporal.Synchrony': '3',
		'Contingency.Cause.Reason': '4',
		'Contingency.Cause.Result': '5',
		'Contingency.Condition': '6',
		'Comparison.Contrast': '7',
		'Comparison.Concession': '8',
		'Expansion.Conjunction': '9',
		'Expansion.Instantiation': '10',
		'Expansion.Restatement': '11',
		'Expansion.Alternative': '12',
		'Expansion.Alternative.Chosen alternative': '13',
		'Expansion.Exception': '14',
        'EntRel': '15',
        'Comparison': '16',
        'Contingency': '17',
        'Expansion': '18',
        'Temporal': '19',
        'Contingency.Cause': '20',
        'Temporal.Asynchronous': '21'
    }