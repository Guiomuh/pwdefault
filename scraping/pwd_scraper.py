#!/usr/bin/python3
import requests, re, random
from random import randint
from time import sleep
from tqdm import tqdm

L = []
s = requests.session()

r = s.get("https://cirt.net/passwords")

#print(r.text)

urls = re.findall(r'<td><a href="(\?vendor=[^"]*)">[^<]*<\/a><\/td>', r.text)
random.shuffle(urls)

for u in tqdm(urls):
    url = "https://cirt.net/passwords"+u
    tqdm.write(url)
    r = s.get(url)
    tables = re.findall(r'<table[^><]*>(.*?)<\/table>', r.text, flags=re.DOTALL)
    #print(r.text)
    #print(tables)
    for t in tables:
        name = re.search(r'<tr><td [^><]*"#E6E6E6"><a [^><]*><\/a><h3><b>(.*)<b><\/h3><\/td><\/tr><tr><td [^><]*>', t)
        method = re.search(r'<tr><td [^><]*><b>Method<\/b><\/td><td [^<>]*>([^<>]*)<\/td><\/tr>', t)
        user = re.search(r'<tr><td [^><]*><b>User ID<\/b><\/td><td [^<>]*>([^<>]*)<\/td><\/tr>', t)
        passwd = re.search(r'<tr><td [^><]*><b>Password<\/b><\/td><td [^<>]*>([^<>]*)<\/td><\/tr>', t)
    
        if (name != None and passwd != None):
            name = name.group(1).replace("<i>","").replace("</i>","").replace("&nbsp;","").replace(":","")
            if user == None:
                user = "[no user needed]"
            else:
                user = user.group(1)
            passwd = passwd.group(1)

            if (method != None):
                L.append(name+" ("+method.group(1)+"):"+user+":"+passwd)
            else:
                L.append(name+":"+user+":"+passwd)
            tqdm.write(L[-1])
        else:
            tqdm.write("One login of {} skipped".format(u))
            continue

    # sleep before each request
    # sleep(random.randint(500,5000)/1000)
    

for a in L:
    print(a)
