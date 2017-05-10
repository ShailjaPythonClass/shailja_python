# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 12:22:46 2017

@author: jzuber
"""
import unicodecsv

import numpy as np
import pandas as pd

def _datapath(filename):
    return './data_sets/' + filename

def add_ambiguous(function, *args, **kwargs):
    """
    Add an ambiguous option to the return from a name loading function.
    """
    ambiguous = None
    try:
        if args or kwargs:
            boys, girls, ambiguous = function(*args, **kwargs)
        else:
            boys, girls, ambiguous = function()
    except ValueError:
        if args or kwargs:
            boys, girls = function(*args, **kwargs)
        else:
            boys, girls = function()
    if not ambiguous:
        try:
            boys, girls, ambiguous = _find_ambiguous_from_df(boys, girls)
        except (TypeError, IndexError, ValueError):
            boys, girls, ambiguous = _find_ambiguous(boys, girls)
    return boys, girls, ambiguous


def load_born_names(year, *args, **kwargs):
    """
    Load names from census data for all people born in given year.
    """
    filename = "us_census/yob{}.txt".format(year)
    df = pd.read_csv(_datapath(filename),
                     header=None,
                     names=['name', 'sex', 'count'])
    girls_df = df[df.sex=='F'].copy()
    boys_df = df[df.sex=='M'].copy()
    return _find_ambiguous_from_df(boys_df, girls_df)

def load_census_names():
    """
    Load all names from the census-dist files (names with frequency)
    """
    def name_only(x):
        return x.split(' ')[0].title()
    with open(_datapath('census-dist-female-first.txt'), 'r') as inf:
        girls = inf.read().split('\n')
    girls = map(name_only, girls)
    with open(_datapath('census-dist-male-first.txt'), 'r') as inf:
        boys = inf.read().split('\n')
    boys = map(name_only, boys)
    return boys, girls

def load_us_names():
    """
    Reads in unicode csvs containing international names

    Returns boys_names, girls_names
    """
    retval = {}
    jobs = (('boys', _datapath('boys.csv')),
            ('girls', _datapath('girls.csv')))
    for gender, fname in jobs:
        with open(fname, 'r') as inf:
            r = unicodecsv.reader(inf, encoding='utf-8')
            retval.update({gender:[name[0] for name in r]})

    return retval['boys'], retval['girls']

def load_international_names():
    """
    Reads in unicode csvs containing international names

    Returns boys_names, girls_names
    """
    retval = {}
    jobs = (('boys', _datapath('intl_boys.csv')),
            ('girls', _datapath('intl_girls.csv')))
    for gender, fname in jobs:
        with open(fname, 'r') as inf:
            r = unicodecsv.reader(inf, encoding='utf-8')
            retval.update({gender:[name[0] for name in r]})

    return retval['boys'], retval['girls']


def _find_ambiguous_from_df(boys_df, girls_df):
    """
    Find boys, girls and ambiguous names from two input dataframes
    with columns: name, count.

    A name is ambiguous if the (boys' count - girls' count) / total <= 0.4

    returns lists: boys, girls, ambiguous
    """
    in_both = pd.merge(girls_df, boys_df, on='name')
    n_boys = in_both.count_y
    n_girls = in_both.count_x
    is_boy = n_boys / (n_boys + n_girls) > 0.7
    is_girl = n_girls / (n_boys + n_girls) > 0.7

    is_ambiguous = np.abs(n_boys - n_girls) / (n_boys + n_girls) <= 0.4

    girls = set(girls_df['name'])
    boys = set(boys_df['name'])

    likely_girls = set(in_both[is_girl]['name'])
    likely_boys = set(in_both[is_boy]['name'])
    ambiguous_names = set(in_both[is_ambiguous]['name'])

    girls = girls.difference(likely_boys, ambiguous_names)
    boys = boys.difference(likely_girls, ambiguous_names)
    return list(boys), list(girls), list(ambiguous_names)


def _find_ambiguous(boys, girls):
    """
    Find boys, girls and ambiguous names from two input lists

    A name is ambiguous if it is in both lists

    returns lists: boys, girls, ambiguous
    """
    boys = set(boys)
    girls = set(girls)
    ambiguous = boys.intersection(girls)

    boys = boys.difference(ambiguous)
    girls = girls.difference(ambiguous)
    return list(boys), list(girls), list(ambiguous)


if __name__ == "__main__":
    int_boys, int_girls, int_ambig = add_ambiguous(load_international_names)
    us_boys, us_girls, us_ambig = add_ambiguous(load_us_names)
    old_boys, old_girls, old_ambig = add_ambiguous(load_born_names, 1994)
    cen_boys, cen_girls, cen_ambig = add_ambiguous(load_census_names)