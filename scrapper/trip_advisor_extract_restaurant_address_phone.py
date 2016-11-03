from os.path import join
from BeautifulSoup import BeautifulSoup
from solr import query, constant, connection, update
from urllib import urlopen

class ExtractRestaurantReviews(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_restaurant')
        self.conn = connection.get_connection()

    def extractAddressPhone(self):
        resLinks = []

        restaurants = query.getAll(self.conn, constant.RESTAURANTS_COLLECTION, '*:*')

        restaurants = restaurants.result.dict['response']['docs']

        for restaurant in restaurants:
            name = restaurant['name'][0].encode('ascii', 'ignore')
            res_link = restaurant['link'][0]

            webpage = urlopen(res_link).read().decode('utf-8')
            soup = BeautifulSoup(webpage)

            street = soup.findAll('span', attrs={'class': 'street-address'})[0]
            address = soup.findAll('span', attrs={'property': 'addressLocality'})[0]
            region = soup.findAll('span', attrs={'property': 'addressRegion'})[0]
            postal = soup.findAll('span', attrs={'property': 'postalCode'})[0]
            telephone = soup.findAll('div', attrs={'class': 'fl phoneNumber'})[0]
            restaurant['address'] = str(street.contents[0] + ', ' + address.contents[0] + ', ' + region.contents[0] + ' ' + postal.contents[0]).strip()
            restaurant['contact'] = str(telephone.contents[0]).strip()

            print "Adding data for restaurant : " + name

            update.updateUnique(self.conn, constant.RESTAURANTS_COLLECTION, restaurant)
        pass



if __name__ == '__main__':
    # delete.deleteReviews()
    ExtractRestaurantReviews().extractAddressPhone()