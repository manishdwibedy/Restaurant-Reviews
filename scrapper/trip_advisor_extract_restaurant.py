import os
from os.path import join
from BeautifulSoup import BeautifulSoup
from util import saveToFile
from solr import connection, query, constant, index, delete
from urllib import urlopen

class ExtractRestaurantLinks(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_search')
        self.conn = connection.get_connection()

    def extractLinksFile(self):
        resLinks = []
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                with open(file_path) as file:
                    webpage = file.read().decode('utf-8')
                soup = BeautifulSoup(webpage)

                # Link to the restaurant
                links = soup.findAll('a', attrs={'class': 'property_title'})

                # Number of reviews
                reviewCountSpan = soup.findAll('span', attrs={'class': 'reviewCount'})

                #
                ratingImage = soup.findAll('img', attrs={'class': 'sprite-ratings'})
                price_range = soup.findAll('span', attrs={'class': 'price_range'})
                cuisines = soup.findAll('div', attrs={'class': 'cuisines'})

                for link in links:
                    resLinks.append(link.attrMap['href'])
        saveToFile('\n'.join(resLinks), join('raw_data', 'res_links.txt'))

    def extractLinks(self):
        searchResults = query.getAll(self.conn, constant.SEARCHES_COLLECTION, '*:*')

        searchResultLinks = []

        for searchResult in searchResults.result.dict['response']['docs']:
            if 'url' in searchResult:
                searchResultLinks.append(searchResult['url'][0])

        for link in searchResultLinks:
            restaurant_data = self.extractRestaurantLink(link)
            index.index(self.conn, constant.RESTAURANTS_COLLECTION, restaurant_data)

            print 'Adding ' + str(len(restaurant_data)) + ' restaurants'


    def extractRestaurantLink(self, URL):
        webpage = urlopen(URL).read().decode('utf-8')
        soup = BeautifulSoup(webpage)

        results = soup.findAll('div', attrs={'id': 'EATERY_SEARCH_RESULTS'})[0]

        restaurant_info = []

        for restaurant in results.findAll('div'):
            if 'listing' in restaurant.attrMap['class']:

                # Link to the restaurant
                linkAnchor = restaurant.findAll('a', attrs={'class': 'property_title'})[0]

                #name
                name = str(linkAnchor.contents[0]).strip()

                link = str(self.baseURL + linkAnchor.attrMap['href'])

                # Number of reviews
                try:
                    reviewCountSpan = restaurant.findAll('span', attrs={'class': 'reviewCount'})
                    reviewCount = str(reviewCountSpan[0].findAll('a')[0].contents[0]).strip()
                except:
                    reviewCount = 'N.A.'

                # Rating
                try:
                    ratingImage = restaurant.findAll('img', attrs={'class': 'sprite-ratings'})[0]
                    rating = str(ratingImage.attrMap['alt'])
                except:
                    rating = 'N.A.'

                #Price Range
                try:
                    price_range_span = restaurant.findAll('span', attrs={'class': 'price_range'})[0].findAll('span')[0]
                    price_range = str(price_range_span.contents[0])
                except:
                    price_range = 'N.A.'

                #Cuisines
                cuisines_list = restaurant.findAll('div', attrs={'class': 'cuisines'})
                cuisines = []
                if len(cuisines_list) > 0:
                    for cuisine in cuisines_list[0].findAll('a', attrs={'class': 'cuisine'}):
                        cuisines.append(str(cuisine.contents[0]))
                    cuisine = ', '.join(cuisines)
                else:
                    cuisine = 'N.A.'

                restaurant_info.append({
                    'name': name,
                    'link': link,
                    'reviewCount': reviewCount,
                    'res_rating': rating,
                    'price_range': price_range,
                    'cuisines': cuisine
                })
                pass

        return restaurant_info


if __name__ == '__main__':
    # delete.deleteRestaurants()
    ExtractRestaurantLinks().extractLinks()