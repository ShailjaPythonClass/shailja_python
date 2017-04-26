# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 18:29:18 2017

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
    
def first_letter(name):
    """ 
    A simple nltk feature calculator
    """
    return {'first_letter': name[0]}

def label_names(boys_names, girls_names, func):
    """
    Apply feature function, func to each name, 
    and return test and training feature sets of the form
    feature_vector, label.
    
    Returns: test_set, training_set
    """
    labeled_names = [(name, 'male') for name in boys_names] + \
                    [(name, 'female') for name in girls_names]

    featuresets = [(func(x), g) for (x, g) in labeled_names]
    shuffle(featuresets)   
    train_set = featuresets[:-len(featuresets)/3]
    test_set = featuresets[-len(featuresets)/3:]
    return test_set, train_set
    
if __name__ == "__main__":
    seed(139)
    boys, girls = load_names()      
    test_set, train_set = label_names(boys, girls, first_letter)
    
    classifier = nltk.DecisionTreeClassifier.train(train_set)
    print "Accuracy: {}".format(nltk.classify.accuracy(classifier, test_set))