from ...labeler import Labeler

class SSHLabeler(Labeler):

    @staticmethod
    def get_stix_data(topic, data):
        return data