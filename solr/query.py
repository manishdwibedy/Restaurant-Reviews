import connection, constant, json

def get(connection, collection, query, rows = -1):
    """
    Getting the data from collection matching the query
    :param connection: the Solr Connection
    :param collection: the Solr Collection
    :param query: Solr Query
    :param rows: number of rows to return
    :return: the list of documents returned by Solr
    """
    if rows == -1:
        return connection[collection].search({'q':query})
    else:
        return connection[collection].search({'q':query,'rows': rows})

def getCount(connection, collection, query):
    """
    Get only the number of documents from the collection matching the query
    :param connection: the Solr Connection
    :param collection: the Solr Collection
    :param query: Solr Query
    :return: the number of documents matched
    """
    docs = connection[collection].search({'q':query, 'rows': 0})
    return docs.result.response.numFound

def getAll(connection, collection, query):
    count = getCount(connection, collection, query)
    return get(connection, collection, query, count)

if __name__ == '__main__':
    solr = connection.get_connection()
    response = getAll(solr, constant.RESTAURANTS_COLLECTION,'contact:[* TO *]')
    docs = response.result.response.docs
    print docs
    with open('data.txt', 'w') as outfile:
        json.dump(docs, outfile)
    # json.dumps()


