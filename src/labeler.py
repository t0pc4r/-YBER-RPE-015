import base64
import pika
import json

from pycti import (
    OpenCTIConnectorHelper,
    get_config_variable,
    SimpleObservable,
    OpenCTIStix2Utils,
)

class Labeler:

    @classmethod
    def label(cls, rabbitmq_config, topic, data):
        stix_data = cls.get_stix_data(topic, data)
        Labeler.send_to_rabbitmq(rabbitmq_config, topic, stix_data)

    @classmethod
    def send_to_rabbitmq(cls, rabbitmq_cxn, topic, data):
        channel = rabbitmq_cxn.channel()

        message = {
            "applicant_id": "",
            "action_sequence": 0,
            "entities_types": [],
            "content": base64.b64encode(data.encode("utf-8")).decode("utf-8"),
            "update": False,
        }

        channel.basic_publish(
            exchange="topic",
            routing_key="push_routing_5dc128b8-d3f4-4562-9885-1b80cabdf5b2",
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )

        channel.close()

        print("TODO let's pretend this actual send")
        print("Sending %s : %s" % (topic, data))




    @classmethod
    def get_stix_data(cls, topic, data):
        raise Exception("Not implemented")
