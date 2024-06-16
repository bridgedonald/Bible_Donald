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
        

def scrapeOne(url='https://www.biblegateway.com/passage/?search=Genesis%202&version=CEV'):

    print('\n\n\n')

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

    elements = soup.find_all('div', class_='version-CEV result-text-style-normal text-html')
    passage_txt = ''
    for e in elements:
        passage_txt += f'{e}'
    
    print(passage_txt)

    id0 = None
    ppp = soup.find_all('span')
    for p in ppp:
        id0 = p.get('id')
        if id0 != None:
            break
    
    return (id0, passage_txt)


def toc():
    url = 'https://www.biblegateway.com/versions/Contemporary-English-Version-CEV-Bible/#booklist'

    response = requests.get(url=url)

    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='infotable chapterlinks updatepref')

    trs = table.find_all('tr')

    passage_txt = ''
    passage_txt += '<p>Holy Bible --- CEV</p>'
    passage_txt += '<p>Compiled by Donald</p>'
    passage_txt += '<p></p>'

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
        if chapter!='Genesis':
            continue

        _path = f'{top_dir}/{chapter}'
        print(f'"{_path}"')

        if os.path.exists(_path):
            print(f'skip {chapter}')
            continue

        print(f'ch: {chapter}')

        passage_txt += f'<p> {chapter} ['

        refs = tds[1].find_all('a')
        for r in refs:
            url = 'https://www.biblegateway.com' + r.get('href')
            sector = r.text
            dnld(url=url)
            passage_txt += f'<a href="{chapter}/{sector}.html"> .{sector} </a>'
            print(sector)
        passage_txt += ']</p>'


    title = "Holy Bible CEV"
    _path = f'{top_dir}/'

    filename = f'{_path}/cev.html'

    if not os.path.exists(_path):
        os.mkdir(_path)

    with open(filename, 'w') as file:
        file.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="stylesheet" href="css/passage_min.css">
    <link rel="stylesheet" href="css/default_min.css">
</head> 
<body>''')
        file.write(passage_txt)
        file.write('''</body>
</html>''')


def scrape_full(urlStart = 'https://www.biblegateway.com/versions/Contemporary-English-Version-CEV-Bible/#booklist'):
    file_toc='toc.txt'
    file_contents = 'contents.txt'
    f = open(file_toc, "w")
    f.write("")
    f.close()

    f = open(file_contents, "w")
    f.write("")
    f.close()

    response = requests.get(url=urlStart)

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
            id0, txt = scrapeOne(url=url)
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

    with open('Bible-CEV.html', 'w') as file:
        file.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="stylesheet" href="css/passage_min.css">
    <link rel="stylesheet" href="css/default_min.css">
</head> 
<body>''')
        file.write(txt_toc)
        file.write(txt_contents)
        file.write('''</body>
</html>''')




scrape()

# scrape_full()

# toc()

