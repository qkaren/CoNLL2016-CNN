import json
import codecs

trian_file_path = "../../data/conll16st-en-01-12-16-train/"
dev_file_path = "../../data/conll16st-en-01-12-16-dev/"
relations_file_name = "relations.json"
train_relations = trian_file_path + relations_file_name
dev_relations = dev_file_path + relations_file_name


def data_process(relations_file):
    Sense_To_Label = {}
    Label_To_Sense = {}
    sense_set = set()
    rf = open(relations_file)
    relations = [json.loads(x) for x in rf]
    for r in relations:
        type = r['Type']
        if type == 'Explicit':
            sense = r['Sense'][0]
            sense_set.add(sense)

    for i,s in enumerate(sense_set):
        Sense_To_Label[s] = i
        Label_To_Sense[i] = s

    print(Sense_To_Label)
    print(Label_To_Sense)
    print(len(sense_set))

# data_process(train_relations)
Sense_To_Label = {'Expansion.Alternative.Chosen alternative': 0, 'Expansion': 1, 'Expansion.Restatement': 18, 'Comparison': 9, 'Contingency.Cause.Reason': 2, 'Contingency.Cause.Result': 3, 'Temporal.Asynchronous.Succession': 5, 'Temporal': 7, 'Temporal.Synchrony': 8, 'Expansion.Instantiation': 10, 'Expansion.Conjunction': 11, 'Expansion.Exception': 12, 'Comparison.Contrast': 13, 'Contingency.Condition': 14, 'Expansion.Alternative': 4, 'Temporal.Asynchronous.Precedence': 16, 'Contingency': 15, 'Comparison.Concession': 17, 'Temporal.Asynchronous': 6}
Label_To_Sense = {0: 'Expansion.Alternative.Chosen alternative', 1: 'Expansion', 2: 'Contingency.Cause.Reason', 3: 'Contingency.Cause.Result', 4: 'Expansion.Alternative', 5: 'Temporal.Asynchronous.Succession', 6: 'Temporal.Asynchronous', 7: 'Temporal', 8: 'Temporal.Synchrony', 9: 'Comparison', 10: 'Expansion.Instantiation', 11: 'Expansion.Conjunction', 12: 'Expansion.Exception', 13: 'Comparison.Contrast', 14: 'Contingency.Condition', 15: 'Contingency', 16: 'Temporal.Asynchronous.Precedence', 17: 'Comparison.Concession', 18: 'Expansion.Restatement'}