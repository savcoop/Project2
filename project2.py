## SI 206 F18 - Project 2

## COMMENT HERE WITH:
## Your name:
## Anyone you worked with on this project and how you worked together
## You can not share code, but can share ideas
###########

## Import statements
import unittest
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl


def grab_headlines(soup):
    headline_div = soup.find("div", {"class": "view-most-read"})
    headline_a = headline_div.find_all('a')
    title_list = [] 
    for headline in headline_a:
        title_list.append(headline.get_text())
    return title_list   

def get_headline_dict(soup): 
    headline_dict = {}
    storywrap = soup.find_all('div', {'class': 'storywrap'})
    for story in storywrap:
        short_headline = story.find('div', {'class': 'views-field-field-short-headline'}).get_text().strip()
        headline_url = story.find('a')['href']
        headline_dict[short_headline] = headline_url
    return headline_dict

## PART 3 Define a function called get_page_info. It will take a soup object for a story
## and return a tuple with the title, author, date, and the number of paragraphs
## in the body of the story
## INPUT: soup - the soup object
## OUTPUT: Return - a tuple with the title, author, date, and number of paragraphs
def get_page_info(soup):
   title = soup.find('div', {'class': 'pane-node-title'}).get_text().strip()
   author = soup.find('div', {'class': 'byline'}).a.get_text()
   date = soup.find('div', {'class': 'pane-node-created'}).find('div', {'class': "pane-content"}).get_text()
   paragraph_initial = soup.find('div', {'class': 'field-name-body'})
   paragraphs = len(paragraph_initial.find_all('p'))

   return (title, date, author, paragraphs)


## Extra Credit
## INPUT: the dictionary that was returned from part 2
## OUTPUT: a new dictionary with just items that contain the word U-M or Ann Arbor
def find_mich_stuff(dict):
    pass

########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########

def getSoupObjFromURL(url):
    """ return a soup object from the url """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getSoupObjFromFile(fileName):
    """ return a soup object from the file with the passed fileName"""
    file = open(fileName, 'r')
    text = file.read().strip()
    file.close()
    soup = BeautifulSoup(text, "html.parser")
    return soup

# testing on live urls - remove the string comments to run this 
"""
soup = getSoupObjFromURL("https://www.michigandaily.com/section/news")
print(grab_headlines(soup))
hDict = get_headline_dict(soup)
print(hDict)
# get page info for each story in hDict
for key, value in hDict.items():
    tuple = getPageInfo(hDict, "http://www.michigandaily.com/")
    print(tuple)
#nDict = find_mich_stuff(hDict) # for extra credit
#print(nDict)
"""

# Test using unittests and saved pages
class TestP2(unittest.TestCase):

    def setUp(self):
        self.soup = getSoupObjFromFile("news1.html")
        self.soup2 = getSoupObjFromFile("newsStory1.html")
        self.dict = get_headline_dict(self.soup)

    def test_grab_headlines(self):
        self.assertEqual(grab_headlines(self.soup),['Broken Record: Student survivor navigates painful reporting process', 'Assistant women’s gymnastics coach resigns after charge of obscene conduct with gymnast', 'Ann Arbor Pieology shuts down because of “unfortunate circumstances”', 'To the white men who told me that they “prefer” white women', 'Op-Ed: Why I declined to write a letter of recommendation  '])

    def test_get_headline_dict(self):
        dict = get_headline_dict(self.soup)
        url = dict['Dialogues on Diversity holds discussion on microaggressions, accountability']
        self.assertEqual(len(dict.items()), 19)
        self.assertEqual(url,'https://www.michigandaily.com/section/campus-life/diversity-sciences')

    def test_get_page_info(self):
        self.assertEqual(get_page_info(self.soup2), ('Panel discusses pros, cons of Library Lot ballot proposal', '\n    Thursday, October 25, 2018 - 9:28pm  ', 'Leah Graham', 17))

    """
    def test_find_mich_stuff(self):
        dict = find_mich_stuff(self.dict)
        url1 = dict[' Ann Arbor state Rep. proposes bill to vastly increase renewable energy ']
        url2 = dict[' U-M freshman runs for Ann Arbor School Board position ']
        self.assertEqual(len(dict), 4)
        self.assertEqual(url1,'https://www.michigandaily.com/section/government/state-rep-proposes-bill-100-percent-renewable-energy-michigan-2050')
        self.assertEqual(url2,'https://www.michigandaily.com/section/ann-arbor/school-board-candidates-fight-name-recognition-race')
    """

unittest.main(verbosity=2)
