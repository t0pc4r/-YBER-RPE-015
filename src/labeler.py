class Labeler:

    @classmethod
    def label(cls, opencti_helper, topic, data):
        stix_data = cls.get_stix_data(topic, data)
        Labeler.send_to_opencti(opencti_helper, topic, stix_data)

    @classmethod
    def send_to_opencti(cls,opencti_helper, topic, data):
        opencti_helper.send_stix2_bundle(data)

        print("Sending %s : %s" % (topic, data))




    @classmethod
    def get_stix_data(cls, topic, data):
        raise Exception("Not implemented")
