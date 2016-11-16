#coding:utf-8
import os, config
from . import mallet_util
from sklearn import svm
from sklearn.datasets import load_svmlight_file
import pickle
from sklearn.externals import joblib


class Strategy:
    def train_model(self, train_file_path, model_path):
        return None
    def test_model(self, test_file_path, result_file_path, model_path):
        return None


''' MaxEnt '''
class MaxEnt(Strategy):
    def __init__(self):
        self.trainer = "MaxEnt"

    def train_model(self, train_file_path, model_path):
        print("training %s ..." % (self.trainer))


        cmd = config.MALLET_PATH + \
              "/bin/mallet import-svmlight --input " + train_file_path + " --output "+ config.MALLET_FILE
        os.system(cmd)
        cmd = config.MALLET_PATH + \
              "/bin/mallet train-classifier --input " + config.MALLET_FILE + \
              " --output-classifier " + model_path + " --trainer " + self.trainer \
              # + " -Xms256m -Xmx2048m "
              # + " --cross-validation 10"
        os.system(cmd)
        print("\n%s model 已经生成：%s " %( self.trainer, model_path))

    def test_model(self, test_file_path, result_file_path, model_path):
        cmd = config.MALLET_PATH + "/bin/mallet classify-file --input " + test_file_path + " --output " + result_file_path + " --classifier " + model_path
        os.system(cmd)
        print("test the model ...")



''' Naive Bayes '''
class NaiveBayes(Strategy):
    def __init__(self):
        self.trainer = "NaiveBayes"

    def train_model(self, train_file_path, model_path):
        print("training %s ..." % (self.trainer))

        cmd = config.MALLET_PATH + \
              "/bin/mallet import-svmlight --input " + train_file_path + " --output "+ config.MALLET_FILE
        os.system(cmd)
        cmd = config.MALLET_PATH + \
              "/bin/mallet train-classifier --input " + config.MALLET_FILE + \
              " --output-classifier " + model_path + " --trainer " + self.trainer \
              # + " --cross-validation 10"
        os.system(cmd)
        print("\n %s model 已经生成：%s " %(self.trainer, model_path))

    def test_model(self, test_file_path, result_file_path, model_path):
        cmd = config.MALLET_PATH + "/bin/mallet classify-file --input " + test_file_path + " --output " + result_file_path + " --classifier " + model_path
        os.system(cmd)
        print("test the model ...")


''' svm '''
class SK_SVM(Strategy):
    def __init__(self):
        self.trainer = "SVM"

    def train_model(self, train_file_path, model_path):
        print("training %s ..." % (self.trainer))

        clf = svm.LinearSVC(C = 1)
        X, y = load_svmlight_file(train_file_path)
        clf.fit(X, y)

        pickle.dump(clf, open(model_path, "w"))

        print("\n %s model 已经生成：%s " %(self.trainer, model_path))

    def test_model(self, test_file_path, result_file_path, model_path):
        print("test the model ...")
        clf = pickle.load(open(model_path, "rb"))

        n_features = clf.coef_.shape[1]

        # 改变test 数据的维度与train一样。 添加 n_features：0
        self.change_test_dimension(test_file_path, n_features)

        X, gold_y = load_svmlight_file(test_file_path)
        pred_y = clf.predict(X)

        #将预测结果写入文件，同mallet一样
        fout = open(result_file_path, "w")
        for gold, pred in zip(gold_y, pred_y):
            fout.write(str(int(gold)) + "\t" + str(int(pred)) + "\t" + "1.0\n")
        fout.close()

    def change_test_dimension(self, test_file_path, n_features):
        file = open(test_file_path)
        lines = []
        flag = 0
        for line in file:# 175:1 21381:1 #
            line = line.rstrip()
            if flag == 0 and line.split("#")[0].strip() != "":
                last_feat_dimension = int(line.split("#")[0].rstrip().split(" ")[-1].split(":")[0])
                if last_feat_dimension < n_features:#加一维
                    line = line.split("#")[0] +"%d:0 #" % n_features + line.split("#")[1]
                    flag = 1
            lines.append(line)
        file.close()
        file = open(test_file_path, "w")
        file.write("\n".join(lines))
        file.close()




class Mallet_classifier:
    def __init__(self,strategy):
        self.strategy = strategy

    def train_model(self, train_file_path, model_path):
        self.strategy.train_model(train_file_path, model_path)

    def test_model(self, test_file_path, result_file_path, model_path):
        self.strategy.test_model(test_file_path, result_file_path, model_path)


if __name__ == "__main__":
    pass
