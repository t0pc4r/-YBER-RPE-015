from threading import Thread
from elasticsearch import Elasticsearch

class Module(Thread):

    def __init__(self, elastic_config, module_config, worker_pool):
        self.elastic_config = elastic_config
        self.worker_pool = worker_pool
        self.module_config = module_config
    
    def run(self):
        super.run()
        es = self.connect()
        self.start_getting_data(es)
        es.close()

    def connect(self):
        protocol = "https" if self.elastic_config["use_secure"] else "http"
        return Elasticsearch(
            [self.elastic_config["elastic_host"]],
            http_auth=(self.elastic_config["username"], self.elastic_config["password"]),
            scheme=protocol,
            port=self.elastic_config["elastic_port"],
        )

    def get_data(self, es, query, max_size=1024):
        query_result = es.search(query, size=max_size)
        return query_result["hits"]["hits"]

    def send_to_labeler(self, labeler, topic, data):
        self.worker_pool.add_data(labeler, topic, data)

    def start_getting_data(self, es):
        while True:
            data = self.get_data(es, self.get_query())
            if len(data) == 0:
                break
            self.send_to_labeler(self.get_labeler(), self.get_topic(), data)




    def get_labeler(self):
        raise Exception("Not implemented")

    def get_topic(self):
        raise Exception("Not implemented")

    def get_query(self):
        raise Exception("Not implemented")
        