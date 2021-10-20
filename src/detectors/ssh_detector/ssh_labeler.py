from labeler import Labeler

from stix2 import Bundle, NetworkTraffic, IPv4Address

class SSHLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        source_ip = IPv4Address(value=data["_source"]["source"]["ip"])
        destination_ip = IPv4Address(value=data["_source"]["destination"]["ip"])

        network_traffic = NetworkTraffic(
            src_ref=source_ip,
            dst_ref=destination_ip,
            src_port=data["_source"]["source"]["port"],
            dst_port=data["_source"]["destination"]["port"],
            protocols=["ipv4, tcp"],
        )

        bundle = Bundle(objects=[source_ip, destination_ip, network_traffic]).serialize()
        return bundle
