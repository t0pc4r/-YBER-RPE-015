class Labeler:

    @classmethod
    def label(cls, rabbitmq_config, topic, data):
        stix_data = cls.get_stix_data(topic, data)
        Labeler.send_to_rabbitmq(rabbitmq_config, topic, stix_data)

    @classmethod
    def send_to_rabbitmq(cls, rabbitmq_config, topic, data):
        print("TODO let's pretend this actual send")
        print("Sending %s : %s" % (topic, data))




    @classmethod
    def get_stix_data(cls, topic, data):
        raise Exception("Not implemented")
