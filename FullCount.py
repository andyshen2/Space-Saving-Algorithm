import glob
import pandas
from pandas.io.json import json_normalize
from collections import Counter

hD = {}
tD = {}
lD = {}

def updateLang(lang, hash):

    if lang+"*"+hash in lD.keys():
        lD[lang+"*"+hash] += 1
    else:
        lD[lang+"*"+hash] = 1
    # print(lD)

def updateText(list, hash):
    for t in list:

        if t+"*"+hash in tD.keys():
            tD[t+"*"+hash] += 1
        else:
            tD[t+"*"+hash] = 1
    # print(tD)
def full_count(folder):
    for filename in glob.glob(folder + '/*.json.gz'):

        tweets = pandas.read_json(filename, lines=True, compression="gzip")

        count = 0
        while (count < len(tweets.index)):
            hashtags = json_normalize(tweets.loc[count].entities['hashtags']).text.to_string(index=False, header=None).split()
            text = tweets.loc[count].text.split()
            lang = tweets.loc[count].lang

            for t in hashtags:
                updateText(text, t)
                updateLang(lang, t)

                if t in hD.keys():
                    hD[t] += 1
                else:
                    hD[t] = 1

            count += 1

    count_hD = Counter(hD)
    count_tD = Counter(tD)
    count_lD = Counter(lD)
    sorted_hD = count_hD.most_common(10)
    sorted_tD = count_tD.most_common(10)
    sorted_lD = count_lD.most_common(10)
    print(sorted_hD)
    print(sorted_tD)
    print(sorted_lD)

x = input("Enter Folder: ")


full_count(x)
