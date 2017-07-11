# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:38:37 2017

@author: jzuber
"""
import nltk
import requests

from bs4 import BeautifulSoup
from numpy.random import shuffle, seed

def load_born_names(year):
    filename = "./us_census/yob{}.txt".format(year)
    df = pd.read_csv(filename, header=None, names=['name', 'sex', 'count'])
    girls = df[df.sex=='F'].copy()
    boys = df[df.sex=='M'].copy()
    in_both = pd.merge(girls, boys, on='name')
    n_boys = in_both.count_y
    n_grils = in_both.count_x
    likely_boy = n_boys / (n_boys + n_girls) > 0.7
    likely_girl = n_girls / (n_boys + n_girls) > 0.7
   # with open(filename, 'r') as inf

def load_names():        
    with open('../sample_data/boys.csv', 'r') as inf:
        boys_names = inf.read().split(',\n')
    with open('../sample_data/girls.csv', 'r') as inf:
        girls_names = inf.read().split(',\n')
    return boys_names, girls_names

def pull_names():
    """
    Reads 1000 most common American baby names from the internet, 
    
    Returns names in two lists: boys_names, girls_names
    """
    site = 'https://www.babble.com/pregnancy/'
    boys_url = site + '1000-most-popular-boy-names/'
    girls_url = site + '1000-most-popular-girl-names/'

    boys_page = requests.get(boys_url)
    girls_page = requests.get(girls_url)

    def get_name(x):
        if x.attrs.get('class', None) == [u'p1'] \
            and x.getText() \
            and x.getText().isalpha():
            return x.getText()
        return None

    boys_soup = BeautifulSoup(boys_page.text, "html.parser")
    boys_names = [get_name(x) for x in boys_soup.find_all('li')]
    boys_names = filter(None, boys_names)

    girls_soup = BeautifulSoup(girls_page.text, "html.parser")
    girls_names = [get_name(x) for x in girls_soup.find_all('li')]
    girls_names = filter(None, girls_names)

    return boys_names, girls_names

def first_letter(name):
    """ 
    A simple nltk feature calculator
    """
    return {'first_letter': name[0]}

def last_letter(name):
    return {'Last_letter': name[-1]}
    
    
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
    py_names = ['James', 'Shailja', 'Chris', 'Dave', 'Sheng', 
                'Claire', 'Akshay', 'Catherine', 'Rhonda', 'Emily']
    py_genders = ['male', 'female', 'male', 'male', 'male',
                  'female', 'male', 'female', 'female', 'female']

    for name, gender in zip(py_names, py_genders):
        gender_guess = classifier.classify(func(name))
        if gender_guess != gender:
            print "Incorrectly classified: {:<8}".format(name)
    print "\n"    
    
def ends_and_vowels(name):
    """
    A slightly better feature set.
    """
    n_vowels = sum(map(name.lower().count, "aeiou"))
    vowel_decile = int(10*n_vowels / float(len(name)))
    return {'first_letter': name[0],
            'last_letter':name[-1],
            'vowel_decile':vowel_decile}

def shailja_features(name):
    """
    A slightly better feature set.
    """
    n_vowels = sum(map(name.lower().count, "aeiou"))
    vowel_decile = int(10*n_vowels / float(len(name)))
    contains_a = True
    try:
        name.lower().index('a') >= 0              
    except ValueError:
        contains_a = False
        
    vowel_end = name[-1] in "aeiou"
    
    return {'first_letter': name[0],
            'last_letter':name[-1],
            'vowel_decile':vowel_decile,
            'contains_a':contains_a,
            'vowel_end':vowel_end}
            
def feature3(name):
    n_vowels = sum(map(name.lower().count, "aeiou"))
    vowel_decile = int(10*n_vowels / float(len(name)))
    contains_v = True
    try:
        name.lower().index('v') >= 0              
    except ValueError:
        contains_v = False  
    
    contains_a = True
    try:
        name.lower().index('a') >= 0              
    except ValueError:
        contains_a = False              
        
    vowel_end = name[-1] in "aeiou"
    
    contains_elle = True
    try:
        name.lower().index('elle') >= 0              
    except ValueError:
        contains_elle = False
    
    return {'first_letter': name[0],
            'last_letter':name[-1],
            'vowel_decile':vowel_decile,
            'contains_a':contains_a,
            'vowel_end':vowel_end,
            'contains_v':contains_v,
            'contains_elle':contains_elle}

def test_classifier(classifier_type, func):    
    boys, girls = load_names()
    test_set, train_set = label_names(boys, girls, func)
    classifier = classifier_type.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    test_our_class(classifier, func)
    return accuracy
            
if __name__ == "__main__":
    func = first_letter
    boys, girls = pull_names()  
    seed(2)    
    test_set, train_set = label_names(boys, girls, func)
       
    classifier = nltk.DecisionTreeClassifier.train(train_set)
    print "Accuracy: {}".format(nltk.classify.accuracy(classifier, test_set))
    test_our_class(classifier, func)
    
    print test_classifier(nltk.NaiveBayesClassifier, ends_and_vowels)
    print test_classifier(nltk.NaiveBayesClassifier, shailja_features)
    print test_classifier(nltk.NaiveBayesClassifier, feature2)
    print test_classifier(nltk.NaiveBayesClassifier, feature3)