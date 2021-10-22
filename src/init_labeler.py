from labeler import Labeler

from stix2 import Bundle,  ThreatActor

class InitLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        actor =  ThreatActor(
            name=data["name"],
            threat_actor_types=["hacker"],
            id="threat-actor--9a685afb-894d-4eb8-8243-66da88161295"
        )

        return Bundle(objects=[actor])