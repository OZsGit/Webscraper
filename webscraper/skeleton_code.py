#! /bin/env/ python3

"""
Objected-Oriented Programming using class
Modular codes using small functions, each of which can be unit-tested

The functions should be designed to be a coherent logical unit. not too complex, for readability and maitence,
"""

import urllib.request as ur
from bs4 import BeautifulSoup
import os, sys



class Webscraper:
    def __init__(self, configfile):
        """
        get parameters from a configuration file
        :param configfile: path2config file
        :return:
        """

        self.urls = self.get_urls(configfile)
        self.keywords = self.get_keywords(configfile)


    def get_urls(self, conffile):
        # research use python lib to parse yaml,Or json formatted configure file

        return a_list_of_web_url


    def get_keywords(self, conffile):
        # research use python lib to parse yaml,Or json formatted configure file

        return a_list_ofkeywords


    def main(self):

        for aurl in self.urls:
            pages = do_scrape(aurl, self.keywords)  # define do_scraper

            for each_page in pages:
                # write_tofile()

                pass

#######################################
# script execution entry  point
######################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print ("please provide a configuration file")
        print("Usage:  %s path2configfile" % sys.argv[0])
        sys,exit(1)

    myobj = Webscraper(sys.argv[1])
    myobj.main()
