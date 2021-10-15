from threading import Thread
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

class Module(Thread):

    def __init__(self, elastic_config, module_config, worker_pool):
        super().__init__()
        self.elastic_config = elastic_config
        self.worker_pool = worker_pool
        self.module_config = module_config
    
    def run(self):
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

    def send_to_labeler(self, labeler, topic, data):
        self.worker_pool.add_data(labeler, topic, data)

    def start_getting_data(self, es):
        query = self.get_query()
        topic = self.get_topic()
        labeler = self.get_labeler()
        for data in scan(es, query):
            self.send_to_labeler(labeler, topic, data)

    def get_labeler(self):
        return self.module_config["labler"]

    def get_topic(self):
        return self.module_config["topic"]




    def get_query(self):
        raise Exception("Not implemented")
        