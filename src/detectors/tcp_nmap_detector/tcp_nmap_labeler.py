from labeler import Labeler
from stix2 import Bundle, Tool, Relationship, AttackPattern
from init_labeler import ThreatActorLabeler

import uuid
import json

class TCPNMapLabeler(Labeler):

    tcp_nmap_id = "tool--%s" % uuid.uuid4()

    @classmethod
    def get_stix_data(cls, topic, data):
        attack_pattern_id = "attack-pattern--%s" % uuid.uuid4()
        nmap_pattern = AttackPattern(
            name="Port Scan",
            description=json.dumps(data),
            id=attack_pattern_id
        )
        nmap_tool = Tool(
            tool_types=["vulnerability-scanning", "information-gathering"],
            name="NMap Port Scan",
            id=TCPNMapLabeler.tcp_nmap_id
        )
        uses_port_scan = Relationship(
            source_ref=attack_pattern_id,
            target_ref=TCPNMapLabeler.tcp_nmap_id,
            relationship_type="derived_from",
        )
        uses_nmap = Relationship(
            source_ref=ThreatActorLabeler.actor_id,
            target_ref=TCPNMapLabeler.tcp_nmap_id,
            relationship_type="uses",
        )
        return Bundle(objects=[nmap_pattern, nmap_tool, uses_nmap, uses_port_scan])