from threading import Thread
from queue import Queue, Empty
from pycti import OpenCTIConnectorHelper


import time
import pika
import utils

class Worker(Thread):

    def __init__(self, opencti_config, queue, timeout=5):
        super().__init__()
        self.opencti_config = opencti_config
        self.queue = queue
        self.timeout = timeout
        self.keep_running = True
        self.has_finished = False

    def run(self):
        opencti_helper = None
        for _ in range(20):
            try:
                opencti_helper = OpenCTIConnectorHelper(
                    {
                        "opencti": {
                            "url": "http://%s:%d" % (self.opencti_config["host"], self.opencti_config["port"]),
                            "token": "537e583b-6e9a-4754-bafd-ba81038bdc35",
                        },
                        "connector": {
                             "id": "ssh_connector_id",
                            "type": "EXTERNAL_IMPORT",
                            "name": "ssh_connector_name",
                            "scope": "ssh_scope",
                            "confidence_level": 0,
                            "update_existing_data": False,
                            "log_level": "info",
                        }
                    }
                )
                break
            except ValueError:
                time.sleep(1)
        else:
            self.has_finished = True
            return


        while self.keep_running or not self.queue.empty():
            try:
                labeler_name, topic, data = self.queue.get(timeout=self.timeout)
            except Empty:
                continue
            labeler = utils.get_class_from_name(labeler_name)
            if labeler is None:
                print("Error, labeler: %s is not found" % labeler_name)
                continue
            labeler.label(opencti_helper, topic, data)
        opencti_helper.close()
        self.has_finished = True

    def join(self):
        self.keep_running = False
        while self.has_finished == False:
            pass



class WorkerPool:

    def __init__(self, opencti_config, max_workers=20):
        self.queue = Queue()
        self.workers = []
        for _ in range(max_workers):
            self.workers.append(Worker(opencti_config, self.queue))

    def start(self):
        for worker in self.workers:
            worker.start()

    def join(self):
        for worker in self.workers:
            worker.join()

    def add_data(self, labeler, topic, data):
        self.queue.put((labeler, topic, data))
