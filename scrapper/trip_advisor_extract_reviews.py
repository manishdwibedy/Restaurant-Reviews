import os
from os.path import join
from BeautifulSoup import BeautifulSoup
from util import saveToFile
from solr import query, constant, connection, index, delete
from urllib import urlopen

class ExtractRestaurantReviews(object):
    def __init__(self):
        self.baseURL = 'http://www.tripadvisor.com'
        self.directory = join('raw_data', 'trip_restaurant')
        self.conn = connection.get_connection()

    def extractReviewsFile(self):
        resLinks = []
        for root, dirs, files in os.walk(self.directory, topdown=True):
            for dir in dirs:
                path = join(self.directory, dir)
                for root, dirs, files in os.walk(path, topdown=True):
                    for name in files:
                        file_path = os.path.join(root, name)
                        with open(file_path) as file:
                            webpage = file.read().decode('utf-8')
                        soup = BeautifulSoup(webpage)

                        links = soup.findAll('a', attrs={'class': 'property_title'})

                        for link in links:
                            resLinks.append(link.attrMap['href'])
            saveToFile('\n'.join(resLinks), join('raw_data', 'res_links.txt'))

    def extractReviews(self):
        resLinks = []

        restaurants = query.getAll(self.conn, constant.RESTAURANTS_COLLECTION, '*:*')

        restaurants = restaurants.result.dict['response']['docs']

        for restaurant in restaurants:
            name = str(restaurant['name'][0])
            print "Restaurant : " + name
            res_link = restaurant['link'][0]
            link = res_link

            count = query.getCount(self.conn, constant.REVIEWS_COLLECTION,'restaurant_name:'+name)
            if count == 0:
                pageIndex = 2
                while True:
                    reviews = []
                    webpage = urlopen(link).read().decode('utf-8')
                    soup = BeautifulSoup(webpage)

                    review_wrapper_list = soup.findAll('div', attrs={'class': 'innerBubble'})

                    for review_wrapper in review_wrapper_list:
                        wrapped_review = review_wrapper.findAll('div', attrs={'class': 'wrap'})

                        if len(wrapped_review) > 0:
                            quote = wrapped_review[0].findAll('div', attrs={'class': 'quote'})

                            # If the review is a new review
                            if len(quote) == 0:
                                quote = wrapped_review[0].findAll('div', attrs={'class': 'quote isNew'})
                                # Otherwise, skip it
                                if len(quote) == 0:
                                    continue

                            review_anchor = quote[0].findAll('a')[0]
                            for attr, value in review_anchor.attrs:
                                if attr == 'href':
                                    review_link = value
                                    break

                            reviews.append({
                                'restaurant_name': name,
                                'restaurant_id': str(restaurant['id']),
                                'restaurant_link': res_link,
                                'review_link': self.baseURL + str(review_link)
                            })
                    index.index(self.conn, constant.REVIEWS_COLLECTION, reviews)
                    print 'Added ' + str(len(reviews)) + ' reviews'



                    try:
                        links = soup.findAll('div', attrs={'class': 'pageNumbers'})[0]
                        page = links.findAll('a', attrs={'data-page-number': pageIndex})

                        if len(page) > 0:
                            page = page[0]

                        pageURL = self.baseURL + str(page.attrMap['href'])
                        # for attr, value in page.attrs:
                        #     if attr == 'href':
                        #         pageURL = self.baseURL + value
                        #         break
                        if pageURL:
                            link = pageURL
                            pageIndex+=1
                    except:
                        print 'Completed index ' + str(pageIndex)
                        break
                break
        pass



if __name__ == '__main__':
    # delete.deleteReviews()
    ExtractRestaurantReviews().extractReviews()