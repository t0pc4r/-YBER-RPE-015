from labeler import Labeler
from stix2 import Bundle, Tool, Relationship

class NMapLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        nmap_tool = Tool(
            tool_types=["vulnerability-scanning"],
            name = "NMap Host Scan",
            id="tool--d6a56586-2299-44d8-97fe-f3c360fd65c9"
        )
        uses_nmap = Relationship(
            source_ref="threat-actor--9a685afb-894d-4eb8-8243-66da88161295",
            target_ref="tool--d6a56586-2299-44d8-97fe-f3c360fd65c9",
            relationship_type="uses",
        )
        return Bundle(objects=[nmap_tool, uses_nmap])