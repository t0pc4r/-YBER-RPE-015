import uuid

from labeler import Labeler

from stix2 import Bundle, NetworkTraffic, IPv4Address, Tool, Relationship
from init_labeler import ThreatActorLabeler

class LeaseLabeler(Labeler):

    lease_id = "tool--%s" % uuid.uuid4()

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
            protocols=["ipv4, udp, dhcp"],
            id=traffic_id
        )

        dhcp_tool = Tool(
            tool_types=["network"],
            name="DHCP",
            id=LeaseLabeler.lease_id
        )

        uses_network_traffic = Relationship(
            source_ref=traffic_id,
            target_ref=LeaseLabeler.lease_id,
            relationship_type="uses",
        )

        uses_dhcp = Relationship(
           source_ref=ThreatActorLabeler.actor_id,
            target_ref=LeaseLabeler.lease_id,
            relationship_type="uses",
        )

        return Bundle(objects=[source_ip, destination_ip, network_traffic, dhcp_tool, uses_network_traffic, uses_dhcp])
