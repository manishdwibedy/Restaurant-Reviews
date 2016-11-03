import connection
import constant
import index

def updateUnique(connection, collection, document):
    """
    Getting the data from collection matching the query
    :param connection: the Solr Connection
    :param collection: the Solr Collection
    :param query: Solr Query
    :param rows: number of rows to return
    :return: the list of documents returned by Solr
    """

    query = 'id:' + document['id']
    index.index(connection, collection, [document])

if __name__ == '__main__':
    solr = connection.get_connection()
    print updateUnique(solr, constant.RESTAURANTS_COLLECTION,'id:1')


