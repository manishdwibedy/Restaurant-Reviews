from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from util import saveSoupToFile, saveToFile
from os.path import join
from time import sleep
import os

class ScrapeTrip(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_search')
        self.url = 'https://www.tripadvisor.com/Restaurants-g32655-Los_Angeles_California.html'

    def getSearchResults(self):
        webpage = urlopen(self.url).read().decode('utf-8')
        soup = BeautifulSoup(webpage)
        saveSoupToFile(soup, join(self.directory, '1.txt'))

        for pageIndex in range(2, 50):
            sleep(0.5)
            links = soup.findAll('div', attrs={'class': 'pageNumbers'})[0]
            page = links.findAll('a', attrs={'data-page-number': pageIndex})[0]

            for attr, value in page.attrs:
                if attr == 'href':
                    pageURL = self.baseURL + value
                    break
            if pageURL:
                webpage = urlopen(pageURL).read().decode('utf-8')
                soup = BeautifulSoup(webpage)
                saveSoupToFile(soup, join(self.directory, str(pageIndex) + '.txt'))

if __name__ == '__main__':
    ScrapeTrip().getSearchResults()




