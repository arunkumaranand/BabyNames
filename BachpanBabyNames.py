__author__ = 'Arunkumar Anand'

import httplib
import sys,codecs, locale
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


'''
Names downloader from Bachpan.com

Logic:
sample URL: http://www.bachpan.com/Indian-Girl-Names-A.aspx?page=2
Request will be made to above Bachpan URL from A to Z
Within each letter, the page will be incremented from 1 to n
Whenever the result count(ie. number of names) is Zero for any n-th page, then alphabet will be incremented
'''



LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

httpConnection = httplib.HTTPConnection('www.bachpan.com')

def getNamesMap(req_url):
    httpConnection.request('GET', req_url)
    response = httpConnection.getresponse()
    res = response.read()
    soup = BeautifulSoup(res, "html.parser")
    # CSS selector syntax
    # Refer: http://www.w3.org/TR/CSS21/selector.html%23id-selectors
    names = soup.select(".search-result .c1 a")
    meaning = soup.select(".search-result .tblMeaning")
    # Actual names are tag content
    names = map(lambda x: x.string, names)
    meaning = map(lambda x: ("".join(map(lambda y: 'None' if y.string == None else y.string, x))).strip(), meaning)
    return dict(zip(names, meaning))

def printNames(names_map):
    for k, v in names_map.items():
        line = [k, ": ", v, '\n']
        sys.stdout.writelines(line)



for start_letter in LETTERS: # iterate through each letters
    for page in range(1,15):
        # /Indian-Girl-Names-A.aspx?page=2
        req_url = "".join(['/Indian-Girl-Names-', start_letter, '.aspx?page=', str(page)])
        #print req_url
        names_map = getNamesMap(req_url)
        if(len(names_map) > 0):
            printNames(names_map)
        else :
            break


