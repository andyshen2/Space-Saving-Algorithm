import glob
import pandas
from pandas.io.json import json_normalize
from collections import Counter

hD = {}
tD = {}
lD = {}

def updateLang(lang, hash, counters):

    if lang+"*"+hash in lD.keys():
        lD[lang+"*"+hash] += 1

    elif lang+"*"+hash not in lD.keys() and len(lD) < counters:
        lD[lang+"*"+hash] = 1
    else:
        lD.pop(min(lD, key=lD.get))
        lD[lang+"*"+hash] = 1

def updateText(list, hash, counters):
    for t in list:

        if t+"*"+hash in tD.keys():
            tD[t+"*"+hash] += 1

        elif t+"*"+hash not in tD.keys() and len(tD) < counters:
            tD[t+"*"+hash] = 1
        else:
            tD.pop(min(tD, key=tD.get))
            tD[t+"*"+hash] = 1


def space_save(folder, counters):

    for filename in glob.glob(folder + '/*.json.gz'):
        try:
            tweets = pandas.read_json(filename, lines=True,compression="gzip")
            print('file done')
            count = 0

            while (count < len(tweets.index)):
                hashtags = json_normalize(tweets.loc[count].entities['hashtags']).text.to_string(index=False, header=None).split()
                text = tweets.loc[count].text.split()
                lang = tweets.loc[count].lang

                for t in hashtags:
                    updateText(text, t, counters)
                    updateLang(lang, t, counters)
                    if t in hD.keys():
                        hD[t] += 1

                    elif t not in hD.keys() and len(hD) < counters:
                        hD[t] = 1
                    else:
                        hD.pop(min(hD, key=hD.get))
                        hD[t] = min(hD.items(), key=lambda x: x[1])[1] + 1
                count += 1
        except:
            print("An exception occurred")

    #Sorts the dictionary to top ten
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
counters = input("Enter Number of counters: ")

space_save(x, int(counters))
