import requests
import random
import json
from hashlib import md5
import sys



appid = ""
appkey = ""
from_lang = 'en'
to_lang =  'zh'
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def get_vtt(vtt):
    cc = 0
    with open(vtt,"r") as f :
        text = f.readlines()
    subtitles = []
    one_sentence = []
    num_subtitle = 0
    END = False
    time1 = None
    rest = ""
    stop_time_1 = "00:00:00.000"
    for i in text :
        cc += 1
        i = i.rstrip("\n")
        if len(i) < 1:
            continue
        elif i == "WEBVTT": # begin of subtitle
            subtitles.append(i)
        elif len(i) < 4 and i.isdigit(): # num of subtitle
            continue
        elif len(i) == 29 and (i[0:1].isdigit() and i[-3:-1].isdigit()):
            # print("[",i[:12],"]-->[",i[17:],"]")
            time1 = i[:12]
            time2 = i[17:]
        else :
            if ((',') in i or ('.') in i or ('?') in i) :
                split1 = i.split(',')
                split2 = i.split('.')
                split3 = i.split('?')
                # print(split1,split2)
                if len(split1) == 2 :
                    rest1 = split1[-1]
                    if len(rest1) == 0 or not rest1[-1].isalpha():
                        rest1 = ""
                elif len(split2) == 2 :
                    rest1 = split2[-1]
                    # print(rest1)
                    if len(rest1) == 0 or not rest1[-1].isalpha():
                        rest1 = ""
                    if len(rest1) != 0 and rest1[0][-1].isdigit() and rest1[1][0].isdigit():
                        rest1 = ""
                elif len(split3) == 2:
                    rest1 = split3[-1]
                    if len(rest1) == 0 or not rest1[-1].isalpha():
                        rest1 = ""
                END = True
                one_sentence.append(i)
                num_subtitle += 1
            else:
                one_sentence.append(i)
        if END :
            END = False
            subtitles.append("")
            subtitles.append(num_subtitle)
            subtitles.append(stop_time_1 + " --> " + time2)
            subtitles.append(rest + " " + " ".join(one_sentence))
            one_setence = []
            rest = rest1
            stop_time_1 = time2
    return subtitles


def translate(query):

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    rr = json.dumps(result, indent=4, ensure_ascii=False)
    res = json.loads(rr)
    return res["trans_result"][0]["dst"]




if __name__ == "__main__":
    args = sys.argv

    tfile = args[1]
    dst = args[2]
    print(tfile,dst)
    print("run\nrun\nrun")
    rr = get_vtt(tfile)
    rr.pop(0)
    with open(dst,"w") as ffile :
        ffile.write("WEBVTT")
        for i in rr:
            # print(i)
            if (not str(i).isdigit()) and len(str(i)) != 0 and i[1].isalpha():
                trans_result = translate(i)
                ffile.write(trans_result + "\n")
            ffile.write(str(i) + "\n")