from threading import Thread
from queue import Queue, Empty
from pycti import OpenCTIConnectorHelper


import time
import pika
import utils

class Worker(Thread):

    MAX_TRIES = 100

    def __init__(self, opencti_config, queue, timeout=5):
        super().__init__()
        self.opencti_config = opencti_config
        self.queue = queue
        self.timeout = timeout
        self.keep_running = True
        self.has_finished = False

    def run(self):
        opencti_helper = None
        for _ in range(Worker.MAX_TRIES):
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
                            "log_level": "warn",
                        }
                    }
                )
                break
            except ValueError:
                time.sleep(1)
        else:
            print("Could not connect to OpenCTI after %d seconds" % Worker.MAX_TRIES)
            self.has_finished = True
            return
        print("Got OpenCTI Connection")

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
            print("Starting worker: %s" % worker)
            worker.start()

    def join(self):
        print("Beginning to stop worker pool with queue size: %d" % self.queue.qsize())
        for worker in self.workers:
            worker.join()
            print("Finished worker: %s" % worker)

    def add_data(self, labeler, topic, data):
        self.queue.put((labeler, topic, data))
