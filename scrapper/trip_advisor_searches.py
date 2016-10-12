from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from util import saveSoupToFile
from os.path import join
from time import sleep
from solr import connection, index
from solr import constant

class ScrapeTrip(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_search')
        self.url = 'https://www.tripadvisor.com/Restaurants-g32655-Los_Angeles_California.html'
        self.saveToFile = False
        self.conn = connection.get_connection()

    def getSearchResults(self):
        webpage = urlopen(self.url).read().decode('utf-8')
        soup = BeautifulSoup(webpage)
        if self.saveToFile:
            saveSoupToFile(soup, join(self.directory, '1.txt'))

        self.searches = []
        self.searches.append(self.url)

        for pageIndex in range(2, 50):
            sleep(0.5)
            links = soup.findAll('div', attrs={'class': 'pageNumbers'})[0]
            page = links.findAll('a', attrs={'data-page-number': pageIndex})[0]

            for attr, value in page.attrs:
                if attr == 'href':
                    pageURL = self.baseURL + value
                    break
            if pageURL:
                self.searches.append(pageURL)
                webpage = urlopen(pageURL).read().decode('utf-8')
                soup = BeautifulSoup(webpage)
                if self.saveToFile:
                    saveSoupToFile(soup, join(self.directory, str(pageIndex) + '.txt'))
        self.saveSearchResults()

    def saveSearchResults(self):
        documents = []
        for link in self.searches:
            documents.append({
                'site': 'Trip Advisor',
                'url': link
            })
        index.index(connection=self.conn, collection=constant.SEARCHES_COLLECTION,document=documents)

if __name__ == '__main__':
    ScrapeTrip().getSearchResults()




