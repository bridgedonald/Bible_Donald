from bs4 import BeautifulSoup
import time, os
import simplejson as json
import requests, random
from bs4 import BeautifulSoup

import re

top_dir = './CEV'
url_entrance = 'https://www.biblegateway.com/versions/Contemporary-English-Version-CEV-Bible/#booklist'

def scrape():
    response = requests.get(url=url_entrance)

    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='infotable chapterlinks updatepref')

    trs = table.find_all('tr')

    chapter = ''
    sector = ''
    for tr in trs:
        tds = tr.find_all('td')
        sss = tds[0].text.split('\n')
        chapter = sss[-1]
        sss = chapter.split(' ')
        for i in range(len(sss)):
            sss[i] = sss[i].strip(' ')
        chapter = ' '.join(sss[0:-1])
        chapter = chapter.rstrip(' ')
        # if chapter!='Genesis':
        #     continue


        refs = tds[1].find_all('a')
        for r in refs:
            url = 'https://www.biblegateway.com' + r.get('href')
            sector = r.text
            _path = f'{top_dir}/{chapter}/{sector}.html'

            if os.path.exists(_path):
                print(f'skip {chapter}: {sector}')
                continue

            save_sector(url)
            print(f'{chapter}/{sector} downloaded')



def parse_chapter_sector(title):
    lst = title.split(' CEV')
    lst = lst[0]
    lst = lst.split(' ')
    sector = lst[-1]
    chapter = ' '.join(lst[0:-1])
    return chapter, sector

def save_sector(url):

    response = requests.get(url=url)

    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('sup', class_='crossreference')
    for e in elements:
        e.decompose()
    elements = soup.find_all('div', class_='crossrefs')
    for e in elements:
        e.decompose()

    elements = soup.find_all('div', class_='passage-text')
    passage_txt = ''
    for e in elements:
        passage_txt += f'{e}'

    title = f"{soup.find('title').text}"
    chapter, sector = parse_chapter_sector(title)

    _path = f'{top_dir}/{chapter}'

    filename = f'{_path}/{sector}.html'

    if not os.path.exists(_path):
        os.mkdir(_path)

    with open(filename, 'w') as file:
        file.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../css/passage_min.css">
    <link rel="stylesheet" href="../css/default_min.css">
</head> 
<body>''')
        file.write(passage_txt)
        file.write('''</body>
</html>''')
        
def read_sector(_chapter='', _sector=''):
    _path = f'{top_dir}/{_chapter}/{_sector}.html'
    _contents = ''
    with open(_path, 'r') as file:
        _contents = file.read()

    soup = BeautifulSoup(_contents, 'html.parser')

    elements = soup.find_all('div', class_='version-CEV result-text-style-normal text-html')
    passage_txt = ''
    for e in elements:
        passage_txt += f'{e}'
    
    id0 = None
    ppp = soup.find_all('span')
    for p in ppp:
        id0 = p.get('id')
        if id0 != None:
            break
    
    return (id0, passage_txt)



def merge_all_into_one_html():
    file_toc='toc.txt'
    file_contents = 'contents.txt'
    f = open(file_toc, "w")
    f.write("")
    f.close()

    f = open(file_contents, "w")
    f.write("")
    f.close()

    response = requests.get(url=url_entrance)

    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='infotable chapterlinks updatepref')

    trs = table.find_all('tr')

    chapter = ''
    sector = ''
    for tr in trs:
        tds = tr.find_all('td')
        sss = tds[0].text.split('\n')
        chapter = sss[-1]
        sss = chapter.split(' ')
        for i in range(len(sss)):
            sss[i] = sss[i].strip(' ')
        chapter = ' '.join(sss[0:-1])
        chapter = chapter.rstrip(' ')
        # if chapter!='Genesis':
        #     continue

        txt_toc = f'<p> {chapter} ['

        refs = tds[1].find_all('a')
        for r in refs:
            url = 'https://www.biblegateway.com' + r.get('href')
            sector = r.text

            _path = f'{top_dir}/{chapter}/{sector}.html'
            if not os.path.exists(_path):
                save_sector(url=url)

            id0, txt = read_sector(chapter, sector)

            _header = ''
            _header += f'<p class="scenechange">* * *</p>'
            _header += '<p></p>'
            _header += f'<p class="sector_title">{chapter} - {sector}      </p>'

            txt = _header + txt
            with open(file_contents, 'a') as file:
                file.write(txt)

            txt_toc += f'<a href="#{id0}">  {sector} </a>'
            print(f'disposing {chapter} - {sector}')

        txt_toc += ']</p>'

        with open(file_toc, 'a') as file:
            file.write(txt_toc)

    # combine into a full html file
    title = "Holy Bible CEV"
    txt_toc = ''
    txt_contents = ''
    with open(file_toc, 'r') as file:
        txt_toc = file.read()
    with open(file_contents, 'r') as file:
        txt_contents = file.read()

    with open(f'{top_dir}/Bible-CEV.html', 'w') as file:
        file.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="Author" content="Donald Bridge Li (bridge5077@gmail.com)">
    <meta name="Publisher" content="American Bible Society">
    <link rel="stylesheet" href="css/passage_min.css">
    <link rel="stylesheet" href="css/default_min.css">
    <link rel="stylesheet" href="css/don.css">
</head> 
<body>
    <h1>Holy Bible</h1>
    <h3>Version: CEV (Contemporary English Version)</h3>
    <h3>Publisher: American Bible Society</h3>
    <p>Recompiled by Donald Bridge Li (bridge5077@gmail.com)</p>
    <p></p>
    <h2>Table of Contents</h2>
    <p></p>
''')
        file.write(txt_toc)
        file.write(txt_contents)
        file.write('''</body>
</html>''')



# scrape()

merge_all_into_one_html()
