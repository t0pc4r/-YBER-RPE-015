from pycti import OpenCTIConnectorHelper

class Labeler:

    @classmethod
    def label(cls, rabbitmq_config, topic, data):
        stix_data = cls.get_stix_data(topic, data)
        Labeler.send_to_rabbitmq(rabbitmq_config, topic, stix_data)

    @classmethod
    def send_to_rabbitmq(cls, rabbitmq_config, topic, data):
        helper = OpenCTIConnectorHelper(
            {
                "opencti": {
                    "url": "http://opencti:8000",
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

        helper.send_stix2_bundle(data)

        print("TODO let's pretend this actual send")
        print("Sending %s : %s" % (topic, data))




    @classmethod
    def get_stix_data(cls, topic, data):
        raise Exception("Not implemented")
