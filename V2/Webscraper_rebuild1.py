import urllib.request as ur
from bs4 import BeautifulSoup
import os, sys
import configparser as conf
import ast

#configfile = input("Please enter the name of your configuration file: ") + ".cfg"

class Webscraper:
    def __init__(self, configfile):
        self.pages = []
        config = conf.ConfigParser()
        config.read(configfile)
        self.urls = self.get_urls(configfile)
        self.keywords = self.get_keywords(configfile)
        self.path = self.get_path(configfile)

    def get_urls(self, configfile):
        config = conf.ConfigParser()
        config.read(configfile)
        return config.get('Websites', 'web').split(',')

    def get_keywords(self, configfile):
        config = conf.ConfigParser()
        config.read(configfile)
        return config.get('Keywords', 'keywords').split(',')

    def get_path(self, configfile):
        config = conf.ConfigParser()
        config.read(configfile)
        return config.get('Path', 'path')

    def write_tofile(self):
        for wpage in self.pages:
            html = aurl + wpage
            texthtml = ur.urlopen(html).read()
            Psoup = BeautifulSoup(texthtml, 'html.parser')
            Ptitle = Psoup.title.string
            Pcontent = Psoup.find_all('p')
            print("Written new file: " + Ptitle)

            path = self.path + aurl[7:] #Set write directory
            if not os.path.exists(path):
                os.makedirs(path)

            filename = Ptitle + '.html'
            with open(os.path.join(path, filename), 'w') as write_file:
                write_file.write(str(Pcontent))

    def main(self):
        for aurl in self.urls:
            self.pages = []
            htmltext = ur.urlopen(aurl).read()
            soup = BeautifulSoup(htmltext, 'html.parser')
            for link in soup.find_all('a'):
                check = link.get('href') #this is a list of every link on the webpage, it looks for the <a href=> tag

                inT = 0 #does it pass the keyword test? 0 is no, 1 is yes
                inR = 0 #does it pass the repeat test?
                inH = 0 #does it pass the http test?
                for akey in self.keywords:
                    if akey in check: #checks if any of the keywords appear in the list of links
                        inT = 1
                if inT == 1:
                    if len(self.pages) > 0:
                        rcheck = 0 #index of repeat check
                        while rcheck < len(self.pages):
                            if self.pages[rcheck] in check: #sometimes there are duplicate links, this checks if there is already registered an identical link
                                rcheck = len(self.pages)
                                inR = 0
                            else:
                                inR = 1
                            rcheck+=1
                    else:
                        inR = 1
                if inR == 1:
                    if 'http://' in check: #if the link begins with 'http://' it links away from the website so isn't necessary
                        inH = 0
                    else:
                        inH = 1
                if inH == 1:
                    self.pages.insert(0, link.get('href')) #if a link passes all previous checks, it is written into an array
            print(self.pages)
            for wpage in self.pages:
                html = aurl + wpage
                texthtml = ur.urlopen(html).read()
                Psoup = BeautifulSoup(texthtml, 'html.parser')
                Ptitle = Psoup.title.string
                Pcontent = Psoup.find_all('p')
                print("Written new file: " + Ptitle)

                path = self.path + aurl[7:] #Set write directory
                if not os.path.exists(path):
                    os.makedirs(path)

                filename = Ptitle + '.html'
                with open(os.path.join(path, filename), 'w') as write_file:
                    write_file.write(str(Pcontent))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print ("please provide a configuration file")
        print("Usage:  %s path2configfile" % sys.argv[0])
        sys.exit(1)

    configfile= sys.argv[1]
    myobj = Webscraper(configfile)
    myobj.main()