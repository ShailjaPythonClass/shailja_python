# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 12:22:46 2017

@author: jzuber
"""
import requests
import unicodecsv
import progressbar
from bs4 import BeautifulSoup

def get_links():
    url = 'http://www.babynamewizard.com/'
    url += 'international-names-lists-popular-names-from-around-the-world'
    
    index_page = requests.get(url)
    index_soup = BeautifulSoup(index_page.text, "html.parser") 
    links = index_soup.find_all('a')
    
    girls_links = [x.get('href', None) for x in links if x.text==u'Girls']
    girls_links = filter(None, girls_links)
    
    boys_links = [x.get('href', None) for x in links if x.text==u'Boys']
    boys_links = filter(None, boys_links)
    
    return boys_links, girls_links
                   
    
def parse_single_gender_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser") 
    try:
        name_list = soup.find('ol').find_all('li')
    except AttributeError:
        return []
    
    def get_name(list_item):        
        if list_item.getText().isalpha():
            return list_item.getText()        
        return None

    names = [get_name(x) for x in name_list]
    names = filter(None, names)
    return names

    
def pull_us_names():
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

def pull_all_from_internet():
    boys_links, girls_links = get_links()
    boys, girls = pull_us_names()
    
    bar = progressbar.ProgressBar(0, len(boys_links))
    for url in bar(boys_links):        
        boys += list(parse_single_gender_page(url))        
    boys = set(boys)
    
    bar = progressbar.ProgressBar(0, len(girls_links))
    for url in bar(girls_links):        
        girls += list(parse_single_gender_page(url))        
    girls = set(girls)        
    
    jobs = ((boys, '../sample_data/intl_boys.csv'),
            (girls, '../sample_data/intl_girls.csv'))    
    for data, fname in jobs:
        with open(fname, 'w') as outf:
            w = unicodecsv.writer(outf)
            w.writerows([[n] for n in data])            
    return boys, girls

def load_us_names():        
    """
    Reads in unicode csvs containing international names
    
    Returns boys_names, girls_names
    """
    retval = {}
    jobs = (('boys', '../sample_data/boys.csv'), 
            ('girls', '../sample_data/girls.csv'))
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
    jobs = (('boys', '../sample_data/intl_boys.csv'), 
            ('girls', '../sample_data/intl_girls.csv'))
    for gender, fname in jobs:
        with open(fname, 'r') as inf:
            r = unicodecsv.reader(inf, encoding='utf-8')
            retval.update({gender:[name[0] for name in r]})    
    
    return retval['boys'], retval['girls']
    
if __name__ == "__main__":
    boys, girls = load_international_names()    
    print len(boys), len(girls)
    
    boys = set(boys)
    girls = set(girls)
    
    overlap = boys.intersection(girls)
    boys.difference_update(overlap)
    girls.difference_update(overlap)
    
    print len(boys), len(girls)