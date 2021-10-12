import argparse
from elasticsearch import Elasticsearch

def connect(username, password, elastic_host, elastic_port, use_secure):
    protocol = "https" if use_secure else "http"
    return Elasticsearch(
        [elastic_host],
        http_auth=(username, password),
        scheme=protocol,
        port=elastic_port,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--username", default="peraton")
    parser.add_argument("--password", required=True)
    parser.add_argument("--elastic-host", default="127.0.0.1")
    parser.add_argument("--elastic-port", default=9200, type=int)
    parser.add_argument("--use-secure", default=False, action='store_true')
    args = parser.parse_args()

    es = connect(args.username, args.password, args.elastic_host, args.elastic_port, args.use_secure)
    query = {
        "query": {
            "match": {
                "destination.address": "8.8.8.8"
            }
        }
    }
    # query syntax: https://www.elastic.co/guide/en/elasticsearch/reference/7.15/query-dsl.html
    # search fields: https://elasticsearch-py.readthedocs.io/en/v7.15.0/api.html#elasticsearch.Elasticsearch.search
    # other ways to get info (count, etc): https://elasticsearch-py.readthedocs.io/en/v7.15.0/api.html#elasticsearch.Elasticsearch
    query_result = es.search(query, size=5)
    results = query_result["hits"]["hits"]
    print(results)