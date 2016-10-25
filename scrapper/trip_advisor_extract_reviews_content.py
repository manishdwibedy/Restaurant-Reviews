import os
from os.path import join
from BeautifulSoup import BeautifulSoup
from util import saveToFile, extractAlt
from solr import query, constant, connection, index, delete
from urllib import urlopen
# REVIEWS_APPEND = reviews.append(
#     {'restaurant_name': name, 'restaurant_id': str(restaurant['id']), 'restaurant_link': res_link,
#      'review_link': self.baseURL + str(review_link)})


class ExtractRestaurantReviewsContent(object):
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
        review_list = []

        reviews = query.getAll(self.conn, constant.REVIEWS_COLLECTION, '*:*')

        reviews = reviews.result.dict['response']['docs']

        for review in reviews:
            restaurant_id = review['restaurant_id'][0]
            restaurant_name = review['restaurant_name'][0]
            restaurant_link = review['restaurant_link'][0]
            review_link = review['review_link'][0]

            review_list.append({
                'restaurant_id': restaurant_id,
                'restaurant_name': restaurant_name,
                'restaurant_link': restaurant_link,
                'review_link': review_link
            })

        for review in review_list:
            review_data = {}

            url = review['review_link']
            webpage = urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(webpage)

            review_wrapper = soup.findAll('div', attrs={'class': 'innerBubble'})[0]

            review_title = review_wrapper.findAll('div', attrs={'class': 'quote'})[0]
            if review_title:
                review_title = str(review_title.contents[0]).strip()
            else:
                review_title = 'N.A.'
            review_data['title'] = review_title

            rating_image = review_wrapper.findAll('img')[0]
            review_rating = str(extractAlt(rating_image)).strip()
            review_data['rating'] = review_rating

            rating_date = review_wrapper.findAll('span',attrs={'class': 'ratingDate'})[0]
            rating_date = str(rating_date.contents[0]).strip()
            review_data['date'] = rating_date

            review_text = review_wrapper.findAll('p',attrs={'property':'reviewBody'})[0]
            review_text = str(review_text.contents[0]).strip()
            review_data['text'] = review_text

            recommend = review_wrapper.findAll('ul', attrs={'class': 'recommend'})[0]
            recommend = recommend.findAll('li')[0]

            ratings = recommend.findAll('li')

            ratings_list = {}
            for rating in ratings:
                rating_text = extractAlt(rating.findAll('img')[0])
                rating_title = rating.findAll('div', attrs={'class': 'recommend-description'})[0]
                rating_title = str(rating_title.contents[0]).strip()
                ratings_list[rating_title] = rating_text
            review_data['sub_rating'] = ratings_list
            pass




if __name__ == '__main__':
    # delete.deleteReviews()
    ExtractRestaurantReviewsContent().extractReviews()