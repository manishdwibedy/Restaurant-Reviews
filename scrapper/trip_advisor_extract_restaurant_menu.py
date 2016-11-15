from os.path import join
from BeautifulSoup import BeautifulSoup
from solr import query, constant, connection, update
from urllib import urlopen

class ExtractRestaurantReviews(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_restaurant')
        self.conn = connection.get_connection()

    def extractMenu(self):
        resLinks = []

        restaurants = query.getAll(self.conn, constant.RESTAURANTS_COLLECTION, '*:*')

        restaurants = restaurants.result.dict['response']['docs']

        for restaurant in restaurants:
            name = restaurant['name'][0].encode('ascii', 'ignore')
            res_link = restaurant['link'][0]

            print "Working on restaurant : " + name

            webpage = urlopen(res_link).read().decode('utf-8')
            soup = BeautifulSoup(webpage)


            menuWrapper = soup.findAll('div', attrs={'class': 'menuItemLHS'})

            if len(menuWrapper) > 0:
                menuList = []
                for menu in menuWrapper:
                    menuTitle = menu.findAll('div', attrs={'class': 'menuItemTitle'})
                    menuList.append(str(menuTitle[0].contents[0]).strip())
                restaurant["menu"] = menuList
            else:
                restaurant["menu"] = "N.A."


            # update.updateUnique(self.conn, constant.RESTAURANTS_COLLECTION, restaurant)
        pass



if __name__ == '__main__':
    # delete.deleteReviews()
    ExtractRestaurantReviews().extractMenu()