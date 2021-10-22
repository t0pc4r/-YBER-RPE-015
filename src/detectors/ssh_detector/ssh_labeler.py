import uuid

from labeler import Labeler

from stix2 import Bundle, NetworkTraffic, IPv4Address, Tool, Relationship

class SSHLabeler(Labeler):

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

        ssh_tool = Tool(
            tool_types=["remote-access"],
            name="SSH",
            id="tool--760ba490-f154-4dbb-a45c-b47115a907a6"
        )

        uses_network_traffic = Relationship(
           source_ref="tool--760ba490-f154-4dbb-a45c-b47115a907a6",
            target_ref=traffic_id,
            relationship_type="derived_From",
        )

        uses_ssh = Relationship(
           source_ref="threat-actor--9a685afb-894d-4eb8-8243-66da88161295",
            target_ref="tool--760ba490-f154-4dbb-a45c-b47115a907a6",
            relationship_type="uses",
        )

        return Bundle(objects=[source_ip, destination_ip, network_traffic, ssh_tool, uses_network_traffic, uses_ssh])