import base64
import pika

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
    def send_to_rabbitmq(cls, rabbitmq_config, topic, data):
        # Taken from https://github.com/OpenCTI-Platform/client-python/blob/master/pycti/connector/opencti_connector_helper.py
        # Should probably use pycti library to do all of this
        rabbit_cxn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_config["host"],
                port=rabbitmq_config["port"],
                # credentials are from .env
                credentials=pika.PlainCredentials("admin", "password"),
            )
        )
        channel = rabbit_cxn.channel()

        message = {
            "applicant_id": "",
            "action_sequence": 0,
            "entities_types": [],
            "content": base64.b64encode(data.encode("utf-8")).decode("utf-8"),
            "update": False,
        }

        channel.basic_publish(
            exchange=self.config["push_exchange"],
            routing_key="push_routing_" + self.connector_id,
            body=json.dumps(message),
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
