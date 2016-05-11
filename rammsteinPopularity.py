import sys,os,os.path
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['HTTP_PROXY']="http://www-proxy.idc.oracle.com:80"
os.environ['HTTPS_PROXY']="http://www-proxy.idc.oracle.com:80"

from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import json

import pandas as pd
from pandas import DataFrame

import seaborn as sns
sns.set_context("talk")
sns.set_style("white")

import matplotlib
import matplotlib.pyplot as plt


BASE_URL = "http://lyricstranslate.com/en/rammstein-lyrics.html#"

song_album_tuple = ()
songname_list = []
album_list = []
reqcount_list = []
song_album_list = []

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def xstr(s):
    if s is None:
        return 'Unclassified'
    return str(s.string)

def get_language_requests(section_url):
    soup = make_soup(section_url)

    songlist_table = soup.find("table", id="artistsonglist")

    table_body = songlist_table.findAll("tr", {"class":["odd", "even"]})
    for link in table_body:
        songname = link.find(class_ = "songName")
        song_name = songname.find("a")
        album = songname.find(class_="langalbum")
        song_title = link.findAll(class_ = "lang")
        album_list.append(album)
        songname_list.append(song_name.string)
        reqcount_list.append(len(song_title))
        song_album_tuple = (song_name.string,) + (xstr(album),)
        song_album_list.append(song_album_tuple)

    print song_album_list
    mydict = dict(zip(song_album_list, reqcount_list))
    df = pd.DataFrame(mydict.values(), mydict.keys())
    df = df.rename(columns={0:'count'})
    print df.head()

    df.plot(kind = 'bar')
    plt.show()



if __name__ == '__main__':
     names = get_language_requests(BASE_URL)