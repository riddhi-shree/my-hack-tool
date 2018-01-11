#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler():
    url = ''
    driver = None
    expectedPageTitle = ''

    mybrowsers = {
        1: 'FIREFOX',
        2: 'CHROME',
    }

    def __init__(self, browsername, target_url, expectedPageTitle):
        self.url = target_url
        self.expectedPageTitle = expectedPageTitle
        self.initializeWebdriver(browsername)


    def initializeWebdriver(self, browsername):
        if browsername in self.mybrowsers.values():
            if browsername in ['CHROME', 'chrome']:
                self.driver = webdriver.Chrome()
            elif browsername in ['FIREFOX', 'firefox']:
                self.driver = webdriver.Firefox()
        else:
            print("Invalid Browser! Please select one of the following options:\n1. FIREFOX\n2. CHROME\n")
            self.driver = webdriver.Firefox()


    def startCrawling(self):
        self.driver.get(self.url)
        assert self.expectedPageTitle in self.driver.title, "\n\nExpected Value:\t %s\nActual Value:\t %s\n\n" % (self.expectedPageTitle, self.driver.title)


    def cleanup(self):
        self.driver.close()


    def action(self):
        self.startCrawling()
        self.cleanup()


obj = Crawler('FIREFOX', 'http://www.google.com', 'Google')
obj.action()
