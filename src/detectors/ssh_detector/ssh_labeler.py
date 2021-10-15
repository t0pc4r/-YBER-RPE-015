from labeler import Labeler

class SSHLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        return data