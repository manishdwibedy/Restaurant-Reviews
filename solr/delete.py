import connection
import constant

def delete(connection, collection, query):
    """
    Deleting the documents from the collection matching the query
    :param connection: the Solr Connection
    :param collection: the Solr Collection
    :param query: Query
    :return: Nothing
    """
    connection[collection].delete({'q':query})
    connection[collection].commit()

def deleteAll():
    conn = connection.get_connection()
    queryString = 'id:*'
    delete(conn, constant.SEARCHES_COLLECTION,queryString)
    delete(conn, constant.REVIEWS_COLLECTION,queryString)
    delete(conn, constant.REVIEWS_COLLECTION,queryString)

def deleteReviews():
    conn = connection.get_connection()
    queryString = 'id:*'
    delete(conn, constant.REVIEWS_COLLECTION,queryString)

def deleteRestaurants():
    conn = connection.get_connection()
    queryString = 'id:*'
    delete(conn, constant.RESTAURANTS_COLLECTION,queryString)

def deleteSearches():
    conn = connection.get_connection()
    queryString = 'id:*'
    delete(conn, constant.SEARCHES_COLLECTION,queryString)

if __name__ == '__main__':
    # deleteRestaurants()
    delete(connection.get_connection(), constant.RESTAURANTS_COLLECTION, 'id:2')

