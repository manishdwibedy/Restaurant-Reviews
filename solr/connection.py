from solrcloudpy import SolrConnection

def get_connection():
    '''
    Get the solr connection.
    :return:
    '''
    connection = SolrConnection(["localhost:8983"])

    return connection


if __name__ == '__main__':
    connection = get_connection()
    print connection





