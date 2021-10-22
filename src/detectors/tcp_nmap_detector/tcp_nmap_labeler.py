from labeler import Labeler
from stix2 import Bundle, Tool, Relationship

class TCPNMapLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        nmap_tool = Tool(
            tool_types=["vulnerability-scanning", "information-gathering"],
            name="NMap Port Scan",
            id="tool--f26511e6-ca10-467c-9af3-292fa1dc7dea"
        )
        uses_nmap = Relationship(
            source_ref="threat-actor--9a685afb-894d-4eb8-8243-66da88161295",
            target_ref="tool--f26511e6-ca10-467c-9af3-292fa1dc7dea",
            relationship_type="uses",
        )
        return Bundle(objects=[nmap_tool, uses_nmap])