from threading import Thread
from queue import Queue

import utils

class Worker(Thread):

    def __init__(self, rabbitmq_config, queue, timeout=5):
        super().__init__()
        self.rabbitmq_config = rabbitmq_config
        self.queue = queue
        self.timeout = timeout
        self.keep_running = True

    def run(self):
        while self.keep_running or not self.queue.empty():
            labeler_name, topic, data = self.queue.get(timeout=self.timeout)
            labeler = utils.get_class_from_name(labeler_name)
            if labeler is None:
                print("Error, labeler: %s is not found" % labeler_name)
                continue
            labeler.label(self.rabbitmq_config, topic, data)

    def stop(self):
        self.keep_running = False



class WorkerPool:

    def __init__(self, rabbitmq_config, max_workers=20):
        self.queue = Queue()
        self.workers = []
        for _ in range(max_workers):
            self.workers.append(Worker(rabbitmq_config, self.queue))

    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        for worker in self.workers:
            worker.stop()

    def add_data(self, labeler, topic, data):
        self.queue.put((labeler, topic, data))