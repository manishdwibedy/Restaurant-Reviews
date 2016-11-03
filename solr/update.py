import connection
import constant
import index

def updateUnique(connection, collection, query):
    """
    Getting the data from collection matching the query
    :param connection: the Solr Connection
    :param collection: the Solr Collection
    :param query: Solr Query
    :param rows: number of rows to return
    :return: the list of documents returned by Solr
    """
    response = connection[collection].search({'q':query})

    data = response.result.dict['response']['docs']

    if len(data) == 1:
        data[0]['temp'] = 1
        index.index(connection, collection, data)

if __name__ == '__main__':
    solr = connection.get_connection()
    print updateUnique(solr, constant.RESTAURANTS_COLLECTION,'id:1')


