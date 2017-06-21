# -*- coding: utf-8 -*-
"""
Created on Tue May 02 13:41:47 2017

@author: apsingh
"""

import nltk
from numpy.random import shuffle, seed

from features import ends_and_vowels , ngrams_ends_and_vowels
from load_names import load_international_names, load_us_names, load_born_names
from classifiers import ConditionalExponential, DecisionTree,  Maxent, \
                        NaiveBayes

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

def test_our_class(classifier, func):
    """
    See how well this classifier does on our class.
    """
    names = ['James', 'Shailja', 'Chris', 'Dave', 'Sheng', 
                'Claire', 'Akshay', 'Catherine', 'Rhonda', 'Emily',
                'Purti']
    genders = ['male', 'female', 'male', 'male', 'male',
                  'female', 'male', 'female', 'female', 'female', 
                  'female']

    gender_guess = [classifier.classify(func(name)) for name in names]
    fails = [name 
             for (name, real, guess) in zip(names, gender_guess, genders)
             if real != guess]
    return fails
    
def test_classifier(classifier_type, boys, girls, func):
    classifier_dict = {'ConditionalExponential':ConditionalExponential,
                       'DecisionTree':DecisionTree,
                       'Maxent':Maxent,
                       'NaiveBayes':NaiveBayes}
    
    classifier, accuracy = classifier_dict[classifier_type](boys, girls, func) 
    fails = test_our_class(classifier, func)
    return accuracy, fails


if __name__ == "__main__":    
    boys, girls = load_us_names()
    classifiers = ['DecisionTree', 'Maxent', 'NaiveBayes', 
                   'ConditionalExponential']
    classifier_type = 'DecisionTree'
    feature = ngrams_ends_and_vowels
    accuracy, fails = test_classifier(classifier_type, 
                                      boys,
                                      girls, 
                                      feature)
    print "US accuracy: {}\n".format(accuracy)
    for name in fails:
        print "{} was misclassified.".format(name)
    print ""
    
    boys, girls = load_international_names()
    accuracy, fails = test_classifier(classifier_type, 
                                      boys, 
                                      girls, 
                                      feature)
    print "International accuracy: {}\n".format(accuracy)
    for name in fails:
        print "{} was misclassified.".format(name)
    print ""
    
    