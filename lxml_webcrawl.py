# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen
# import re
# import unicodedata
# from lxml import etree
# from lxml.html import parse
# from lxml.etree import tostring
# from io import StringIO, BytesIO

import requests
from lxml import html
import unicodedata
import time
from urllib.parse import urljoin
import pickle


RC_url_list1 = 'http://rosettacode.org/mw/index.php?title=Special:Ask&q=%5B%5BIs+task%3A%3Atrue%5D%5D&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3Dmore%2Fclass%3Dsortable-20wikitable-20smwtable&sort=Modification+date&order=desc&offset=15&limit=500&eq=no'
RC_url_list2= 'http://rosettacode.org/mw/index.php?title=Special:Ask&offset=515&limit=500&q=%5B%5BIs+task%3A%3Atrue%5D%5D&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3Dmore%2Fclass%3Dsortable-20wikitable-20smwtable&sort=Modification+date&order=desc&eq=no'

base_url = 'http://rosettacode.org/'

test_url = 'http://rosettacode.org/wiki/Fibonacci_sequence'

lang_dict = {'C++':'cpp ',
            'C': 'c ',
            'CommonLisp': 'lisp ',
            'C#': 'csharp ',
            'Clojure': 'clojure ',
            'Haskell': 'haskell ',
            'HicEst': 'hicest ',
            'Java': 'java ',
            'JavaScript': 'javascript ',
            'OCaml': 'ocaml ',
            'Perl': 'perl ',
            'PHP': 'php ',
            'Python': 'python ',
            'Ruby': 'ruby ',
            'Scala': 'scala ',
            'Scheme': 'scheme '}


example_semantics_dict = {}

# Go to RosettaCode's webiste and grab ULRs of examples
# Returns a list subset of useful ULRs
def get_urls_from_RC(url):
    url_page = requests.get(url)
    url_tree = html.fromstring(url_page.content)
    urls = url_tree.xpath('//a/@href')
    #print(urls[28:527])
    return urls[28:527]

# Takes a url from a supplied link
# Returns a list of codes on that example
# and the tree for further parsing
def find_langauges_on_semantic_page(url):
    semantic_page = requests.get(url)
    tree = html.fromstring(semantic_page.content)
    website_codes = tree.xpath('//*[@id]/a/text()')
    return website_codes, tree

# Takes the semantic_page and looks for the example codes
# If it finds an example, it will send it to the process_string
def get_examples_on_semantic_page(website_codes, tree):
    for key in lang_dict:
        if key in website_codes:
            xpath_string = "//pre[@class='{}highlighted_source'][1]".format(lang_dict[key])
            process_string(key, tree, xpath_string)

# takes an xpath string in, normlizes & removes the unicode bits
# adds to the example_semantics_dict dict
def process_string(key, tree, xpath_string):
    for item in tree.xpath(xpath_string):
        temp = item.xpath("normalize-space()")
        new_str = unicodedata.normalize("NFKD", temp)
        if key in example_semantics_dict:
            example_semantics_dict[key].append(new_str)
        else:
            example_semantics_dict[key] = [new_str]


def semantics_main(RC_url_list):
    url_list = get_urls_from_RC(RC_url_list)

    for url in url_list:
        # take the shortened urls and make them long urls
        long_url = urljoin(base_url, url)
        # take the long_url and return the website information
        website_codes, tree = find_langauges_on_semantic_page(long_url)
        # grab the examples from the website
        get_examples_on_semantic_page(website_codes, tree)
        print(len(example_semantics_dict['HicEst']))
        # prevent from overwhelming the server
        time.sleep(.5)


# saves the data dump to a pickle file to be opened later
def save_pickle_file():
    with open('language_data/data1.p', 'wb') as fp:
        pickle.dump(example_semantics_dict, fp)




semantics_main(RC_url_list1)
semantics_main(RC_url_list2)
save_pickle_file()
