# CoNLL2016-CNN

This is the source code of the system of "Shallow Discourse Parsing Using Convolutional Neural Network" for CoNLL 2016 shared task, the focus is implicit discourse recognition using CNN.

The system is based on the best system (Wang and Lan, 2015) of CoNLL 2015, replacing the implicit part with CNN model.

- Note: some of the models (model_trainer/\*/\*.h5) are compressed with gzip to limit them below 100M, thus they should be decompressed before usage.

Abstract:
This paper describes a discourse pars- ing system for our participation in the CoNLL 2016 Shared Task. We focus on the supplementary task: Sense Classi- fication, especially the Non-Explicit one which is the bottleneck of discourse pars- ing system. To improve Non-Explicit sense classification, we propose a Con- volutional Neural Network (CNN) model to determine the senses for both English and Chinese tasks. We also explore a tra- ditional linear model with novel depen- dency features for Explicit sense classifi- cation. Compared with the best system (Wang and Lan, 2015) in CoNLL-2015, our system achieves competitive perfor- mances. Moreover, as shown in the re- sults, our system has higher F1 score on Non-Explicit sense classification.


URL of this paper: http://www.aclweb.org/anthology/K/K16/K16-2010.pdf
