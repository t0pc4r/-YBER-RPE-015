class Labeler:

    @staticmethod
    def label(rabbitmq_config, topic, data):
        stix_data = Labeler.get_stix_data(topic, data)
        Labeler.send_to_rabbitmq(rabbitmq_config, topic, stix_data)

    @staticmethod
    def send_to_rabbitmq(rabbitmq_config, topic, data):
        print("TODO let's pretend this actual send")
    



    @staticmethod
    def get_stix_data(topic, data):
        raise Exception("Not implemented")