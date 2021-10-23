import uuid

from labeler import Labeler

from stix2 import Bundle, NetworkTraffic, IPv4Address, Tool, Relationship

class TrafficLabeler(Labeler):
    
    @classmethod
    def get_stix_data(cls, topic, data):
        source_ip = IPv4Address(value=data["_source"]["source"]["ip"])
        destination_ip = IPv4Address(value=data["_source"]["destination"]["ip"])

        traffic_id = "network-traffic--%s" % uuid.uuid4()

        network_traffic = NetworkTraffic(
            src_ref=source_ip,
            dst_ref=destination_ip,
            src_port=data["_source"]["source"]["port"],
            dst_port=data["_source"]["destination"]["port"],
            protocols=["ipv4, tcp"],
            id=traffic_id
        )

        return Bundle(objects=[source_ip, destination_ip, network_traffic])