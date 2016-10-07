from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from util import saveSoupToFile
from os.path import join
from os import path, makedirs

class ExtractReviewLinks(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'

    def saveRestaurantPages(self):
        with open('raw_data/res_links.txt') as file:
            res_links = file.readlines()

        for link in res_links:
            print 'working on ' + link
            link = self.baseURL + link

            webpage = urlopen(link).read().decode('utf-8')
            soup = BeautifulSoup(webpage)

            res_name_h1 = soup.findAll('h1', attrs={'id': 'HEADING'})[0]

            res_name = str(res_name_h1.contents[2]).strip()

            directory_location = join('raw_data', 'trip_restaurant', res_name)

            if not path.exists(directory_location):
                makedirs(directory_location)

            saveSoupToFile(soup, join(directory_location, '1.txt'))

            pageIndex = 2
            while True:

                try:
                    links = soup.findAll('div', attrs={'class': 'pageNumbers'})[0]
                    page = links.findAll('a', attrs={'data-page-number': pageIndex})[0]

                    for attr, value in page.attrs:
                        if attr == 'href':
                            pageURL = self.baseURL + value
                            break
                    if pageURL:
                        webpage = urlopen(pageURL).read().decode('utf-8')
                        soup = BeautifulSoup(webpage)
                        saveSoupToFile(soup, join(directory_location, str(pageIndex) + '.txt'))
                        pageIndex+=1
                except:
                    print 'Completed index ' + str(pageIndex)
                    break



if __name__ == '__main__':
    ExtractReviewLinks().saveRestaurantPages()