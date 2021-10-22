from labeler import Labeler

class TCPNMapLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        print(data)
        return data