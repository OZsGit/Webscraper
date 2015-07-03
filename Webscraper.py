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

    def do_scrape(self, aurl):
        htmltext = ur.urlopen(aurl).read()
        soup = BeautifulSoup(htmltext, 'html.parser')
        for link in soup.find_all('a'):
            check_page = link.get('href') #this is a list of every link on the webpage, it looks for the <a href=> tag

            self.check1 = 0 #does it pass the keyword test? 0 is no, 1 is yes
            self.check2 = 0 #does it pass the repeat test?
            self.check3 = 0 #does it pass the http test?
            self.check_keys(check_page)
            self.check_repeat(check_page)
            self.check_Xurl(check_page)
            if self.check1==1 and self.check2==1 and self.check3==1:
                self.pages.insert(0, link.get('href')) #if a link passes all previous checks, it is written into an array
        print(self.pages)

    def check_keys(self, check_page):
        for akey in self.keywords:
            if akey in check_page: #checks if any of the keywords appear in the list of links
                self.check1 = 1

    def check_repeat(self, check_page):
        if len(self.pages) > 0:
            repeat_check_counter = 0 #index of repeat check
            while repeat_check_counter < len(self.pages):
                if self.pages[repeat_check_counter] in check_page: #sometimes there are duplicate links, this checks if there is already registered an identical link
                    repeat_check_counter = len(self.pages)
                    self.check2 = 0
                else:
                    self.check2 = 1
                repeat_check_counter+=1
        else:
            self.check2 = 1

    def check_Xurl(self, check_page):
        if 'http://' in check_page: #if the link begins with 'http://' it links away from the website so isn't necessary
            self.check3 = 0
        else:
            self.check3 = 1

    def write_tofile(self, aurl):
        for wpage in self.pages:
            html = aurl + wpage
            texthtml = ur.urlopen(html).read()
            self.Psoup = BeautifulSoup(texthtml, 'html.parser')
            self.Ptitle = self.Psoup.title.string
            Pcontent = self.prettify()
            print("Written new file: " + self.Ptitle)

            path = os.path.join(self.path + aurl[7:]) #Set write directory
            if not os.path.exists(path):
                os.makedirs(path)

            filename = self.Ptitle + '.html'
            with open(os.path.join(path, filename), 'w') as write_file:
                write_file.write(Pcontent)

    def prettify(self):
        text = '<head><meta charset="UTF-8"></head> <body style = "margin:10%"><body> <h1>{:s}</h1>'.format(self.Ptitle)
        for para in self.Psoup.find_all('p'):
            text_para = str(para)
            #print(text_para)
            text+=text_para
        return text

    def main(self):
        for aurl in self.urls:
            self.pages = []
            self.do_scrape(aurl)
            self.write_tofile(aurl)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print ("please provide a configuration file")
        print("Usage:  %s path2configfile" % sys.argv[0])
        sys.exit(1)

    configfile= sys.argv[1]
    #configfile = "Configuration.cfg"
    myobj = Webscraper(configfile)
    myobj.main()