import sys,os,os.path
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
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

songname_list = []
album_list = []
reqcount_list = []
song_album_list = []

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def simplify_album(s):
    if s is None:
        return 'Unclassified'
    elif 'Mutter' in str(s.string):
        return 'Mutter'
    elif 'Liebe' in str(s.string):
        return 'Liebe Ist Fur Alle Da'
    elif 'Herzeleid' in str(s.string):
        return 'Herzeleid'
    elif 'Reise' in str(s.string):
        return 'Reise Reise'
    elif 'sucht' in str(s.string):
        return 'Sehnsucht'
    elif 'Rosenrot' in str(s.string):
        return 'Roesenrot'
    else:
        return 'Singles'

def get_language_requests(section_url):
    soup = make_soup(section_url)

    songlist_table = soup.find("table", id="artistsonglist")

    table_body = songlist_table.findAll("tr", {"class":["odd", "even"]})
    for link in table_body:
        songname = link.find(class_ = "songName")
        song_name = songname.find("a")
        song_name = song_name.string
        album = songname.find(class_="langalbum")
        song_title = link.findAll(class_ = "lang")

        album_list.append(simplify_album(album))
        songname_list.append(re.sub("[\(\[].*?[\)\]]", "", song_name))
        reqcount_list.append(len(song_title))


    mydict_count = dict(zip(songname_list, reqcount_list))
    mydict_album = dict(zip(songname_list, album_list))

    print mydict_album
    print mydict_count

    df_count = pd.DataFrame({'song':mydict_count.keys(), 'count':mydict_count.values()})
    df_album = pd.DataFrame({'song':mydict_album.keys(), 'album':mydict_album.values()})

    print df_count.head()
    print df_album.head()

    df_final = pd.merge(df_count, df_album, on='song', how='outer')
    print df_final.head()

    sorted_df = df_final[(df_final.album != 'Singles') & (df_final.album != 'Unclassified')].sort('album')
    print "\n"

    grouped = df_final.groupby('album', sort = True)

    sns.set(font_scale=1.0)
    #s = plt.subplot(1, 1, 1)
    g = sns.barplot(x="song", y="count", hue="album", data=sorted_df)
    #s.set_ylim(0,50)
    sns.plt.xticks(rotation=90)
    sns.plt.tight_layout()
    sns.plt.xlabel('Song')
    sns.plt.ylabel('Translation Requests')
    g.set(ylim=(0, 50))
    #sns.plt.savefig('output.png')

    sns.plt.show()


if __name__ == '__main__':
     names = get_language_requests(BASE_URL)
