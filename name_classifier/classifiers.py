# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:38:37 2017

@author: jzuber
"""
import nltk
from numpy.random import shuffle, seed

def load_names():        
    with open('../sample_data/boys.csv', 'r') as inf:
        boys_names = inf.read().split(',\n')
    with open('../sample_data/girls.csv', 'r') as inf:
        girls_names = inf.read().split(',\n')
    return boys_names, girls_names

    
def label_names(boys_names, girls_names, func):
    """
    Apply feature function, func to each name, 
    and return test and training feature sets of the form
    feature_vector, label.
    
    Returns: test_set, training_set
    """
    seed(2)  
    labeled_names = [(name, 'male') for name in boys_names] + \
                    [(name, 'female') for name in girls_names]

    featuresets = [(func(x), g) for (x, g) in labeled_names]
    shuffle(featuresets)   
    train_set = featuresets[:-len(featuresets)/3]
    test_set = featuresets[-len(featuresets)/3:]
    return test_set, train_set

    
def DecisionTree(boys, girls, func):
        test_set, train_set = label_names(boys, girls, func)
        classifier = nltk.DecisionTreeClassifier.train(train_set)
        accuracy = nltk.classify.accuracy(classifier, test_set)
        return classifier, accuracy


def ConditionalExponential(boys, girls, func):
        test_set, train_set = label_names(boys, girls, func)
        classifier = nltk.ConditionalExponentialClassifier.train(train_set)
        accuracy = nltk.classify.accuracy(classifier, test_set)
        return classifier, accuracy 


def Maxent(boys, girls, func):
        test_set, train_set = label_names(boys, girls, func)
        classifier = nltk.MaxentClassifier.train(train_set)
        accuracy = nltk.classify.accuracy(classifier, test_set)
        return classifier, accuracy 


def NaiveBayes(boys, girls, func):
        test_set, train_set = label_names(boys, girls, func)
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        accuracy = nltk.classify.accuracy(classifier, test_set)
        return classifier, accuracy 
    
    