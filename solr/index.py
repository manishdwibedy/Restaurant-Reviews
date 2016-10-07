import connection
import query

def index(connection, collection, document):
    """
    Add the documents to the collection using the Solr connection.
    :param connection: the solr connection
    :param collection: the solr collection
    :param document: the documents to be index
    :return: Nothing
    """
    connection[collection].add(document)
    connection[collection].commit()

if __name__ == '__main__':
    connection = connection.get_connection()
    docs = [{"id":"1", "name":"a"},{"id":"2","name":"b"}]

    index(connection, 'zomato_reviews',docs)
    # op = query.get(connection, '*:*')
    # print op

