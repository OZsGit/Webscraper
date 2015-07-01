import urllib.request as ur
from bs4 import BeautifulSoup
import os

urls = ["http://www.afr.com","http://www.abc.net.au/news"]
Tkeys = ["greece","telstra","greek","mafia"]

url0 = []
url1 = []
url2 = []
url3 = []
url4 = []
pages = [url0, url1, url2, url3, url4]

i = 0 #website number

while i<len(urls):
    htmltext = ur.urlopen(urls[i]).read()
    soup = BeautifulSoup(htmltext, 'html.parser')
    text = soup.get_text()
    tree = soup.prettify()
    #print(tree)
    #print(text)


    for link in soup.find_all('a'):
        #print(urls[i],end='')
        #print(link.get('href'))
        check = link.get('href')

        tchecks = 0 #number of the keyword being checked
        inT = 0 #does it pass the keyword test? 0 is no, 1 is yes
        inR = 0 #does it pass the repeat test?
        while tchecks < len(Tkeys):
            if Tkeys[tchecks] in check:
                inT = 1
            tchecks+=1
        #print(lnum)
        if inT == 1:
            if len(pages[i]) > 0:
                rcheck = 0 #index of repeat check
                while rcheck < len(pages[i]):
                    if pages[i][rcheck] in check:
                        rcheck = len(pages[i])
                        inR = 0
                    else:
                        if 'http://' in check:
                            inR = 0
                        else:
                            inR = 1
                    rcheck+=1
            else:
                inR = 1
        if inR == 1:
            pages[i].insert(0, link.get('href'))

    print(pages[i])
    print(len(pages[i]),end='')
    print(" matched objects")
    i+=1

z = 0 #index of website writing

urlhtml = urls[0]
x = 0 #index of webpage writing

pagehtml = pages[0][0]
html = urlhtml + pagehtml
texthtml = ur.urlopen(html).read()
Psoup = BeautifulSoup(texthtml, 'html.parser')
Ptitle = Psoup.title.string
Pcontent = Psoup.find_all('p')
print(Pcontent)
print("Written new file: " + Ptitle)

path = '/Users/OZ/PycharmProjects/Webscraper/Articles/' + urlhtml[7:]
if not os.path.exists(path):
    os.makedirs(path)

filename = Ptitle + '.html'
with open(os.path.join(path, filename), 'w') as write_file:
    write_file.write(str(Pcontent))

x+=1
z+=1