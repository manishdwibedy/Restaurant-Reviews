import os
from os.path import join
from BeautifulSoup import BeautifulSoup
from util import saveToFile

class ExtractRestaurantLinks(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_search')

    def extractLinks(self):
        resLinks = []
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                with open(file_path) as file:
                    webpage = file.read().decode('utf-8')
                soup = BeautifulSoup(webpage)

                links = soup.findAll('a', attrs={'class': 'property_title'})

                for link in links:
                    resLinks.append(link.attrMap['href'])
        saveToFile('\n'.join(resLinks), join('raw_data', 'res_links.txt'))



if __name__ == '__main__':
    ExtractRestaurantLinks().extractLinks()