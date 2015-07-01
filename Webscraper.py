import urllib.request as ur
from bs4 import BeautifulSoup
import os

urls = ["http://www.afr.com","http://www.abc.net.au/news"] #urls for the websites to be searched (main pages)
Tkeys = ["greece","telstra","greek","mafia"] #keywords; it looks for these in the links. This won't work if the links don't have the article titles in them

url0 = []
url1 = []
url2 = []
url3 = []
url4 = []
pages = [url0, url1, url2, url3, url4] #If more than five websites are to be searched, add more empty arrays

i = 0 #website number

while i<len(urls): #checks each website in urls
    htmltext = ur.urlopen(urls[i]).read()
    soup = BeautifulSoup(htmltext, 'html.parser')
    text = soup.get_text()
    tree = soup.prettify()
    #print(tree)
    #print(text)


    for link in soup.find_all('a'):
        check = link.get('href') #this is a list of every link on the webpage, it looks for the <a href=> tag

        tchecks = 0 #number of the keyword being checked
        inT = 0 #does it pass the keyword test? 0 is no, 1 is yes
        inR = 0 #does it pass the repeat test?
        while tchecks < len(Tkeys):
            if Tkeys[tchecks] in check: #checks if any of the keywords appear in the list of links
                inT = 1
            tchecks+=1
        #print(lnum)
        if inT == 1:
            if len(pages[i]) > 0:
                rcheck = 0 #index of repeat check
                while rcheck < len(pages[i]):
                    if pages[i][rcheck] in check: #sometimes there are duplicate links, this checks if there is already registered an identical link
                        rcheck = len(pages[i])
                        inR = 0
                    else:
                        if 'http://' in check: #if the link begins with 'http://' it links away from the website so isn't necessary
                            inR = 0
                        else:
                            inR = 1
                    rcheck+=1
            else:
                inR = 1
        if inR == 1:
            pages[i].insert(0, link.get('href')) #if a link passes all previous checks, it is written into an array

    print(pages[i])
    print(len(pages[i]),end='')
    print(" matched objects")
    i+=1

z = 0 #index of website writing

while z < len(urls):
    urlhtml = urls[z]
    x = 0 #index of webpage writing
    while x < len(pages[z]):
        pagehtml = pages[z][x]
        html = urlhtml + pagehtml
        texthtml = ur.urlopen(html).read()
        Psoup = BeautifulSoup(texthtml, 'html.parser')
        Ptitle = Psoup.title.string
        Pcontent = Psoup.find_all('p')
        print("Written new file: " + Ptitle)

        #path = '/Users/OZ/PycharmProjects/Webscraper/Articles/' + urlhtml[7:] #Set write directory
        dest_dir='/home/fzhang/webscrape/'
        path = dest_dir + urlhtml[7:] #Set write directory
        if not os.path.exists(path):
            os.makedirs(path)

        filename = Ptitle + '.html'
        with open(os.path.join(path, filename), 'w') as write_file:
            write_file.write(str(Pcontent))

        x+=1
    z+=1
