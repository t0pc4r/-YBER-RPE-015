from threading import Thread
from queue import Queue, Empty

import time
import pika
import utils

class Worker(Thread):

    def __init__(self, rabbitmq_config, queue, timeout=5):
        super().__init__()
        self.rabbitmq_config = rabbitmq_config
        self.queue = queue
        self.timeout = timeout
        self.keep_running = True
        self.has_finished = False

    def run(self):
        rabbitmq_cxn = None
        for _ in range(60):
            print("Trying to get conn")
            try:
                rabbit_cxn = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.rabbitmq_config["host"],
                        port=self.rabbitmq_config["port"],
                        # credentials are from .env
                        credentials=pika.PlainCredentials("admin", "password"),
                    )
                )
                break
            except pika.exceptions.AMQPConnectionError as e:
                time.sleep(1)
                raise e
        else:
            print("Could not get conn")
            self.has_finished = True
            return
        print("Got conn")
        while self.keep_running or not self.queue.empty():
            try:
                labeler_name, topic, data = self.queue.get(timeout=self.timeout)
            except Empty:
                continue
            labeler = utils.get_class_from_name(labeler_name)
            if labeler is None:
                print("Error, labeler: %s is not found" % labeler_name)
                continue
            labeler.label(rabbit_cxn, topic, data)
        self.rabbit_cxn.close()
        self.has_finished = True

    def join(self):
        self.keep_running = False
        while self.has_finished == False:
            pass



class WorkerPool:

    def __init__(self, rabbitmq_config, max_workers=20):
        self.queue = Queue()
        self.workers = []
        for _ in range(max_workers):
            self.workers.append(Worker(rabbitmq_config, self.queue))

    def start(self):
        for worker in self.workers:
            worker.start()

    def join(self):
        for worker in self.workers:
            worker.join()

    def add_data(self, labeler, topic, data):
        self.queue.put((labeler, topic, data))
