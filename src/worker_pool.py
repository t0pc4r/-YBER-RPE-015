from threading import Thread
from queue import Queue

import .utils

class Worker(Thread):

    def __init__(self, rabbitmq_config, queue, timeout=5):
        self.rabbitmq_config = rabbitmq_config
        self.queue = queue
        self.timeout = timeout
        self.keep_running = True

    def run(self):
        super.run()
        while self.keep_running:
            labeler_name, topic, data = self.queue.get(timeout=self.timeout)
            labeler = utils.get_class_from_name(labeler_name)
            labeler.label(self.rabbitmq_config, topic, data)

    def stop(self):
        self.keep_running = False



class WorkerPool:

    def __init__(self, rabbitmq_config, max_workers=20):
        self.queue = Queue()
        self.workers = [Worker(rabbitmq_config, self.queue)] * max_workers

    def stop(self):
        for worker in self.workers:
            worker.stop()

    def send_to_labeler(self, labeler, topic, data):
        self.queue.put((labeler, topic, data))