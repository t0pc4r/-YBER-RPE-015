from labeler import Labeler

from stix2 import Bundle, Identity

class InitLabeler(Labeler):

    @classmethod
    def get_stix_data(cls, topic, data):
        actor = Identity(
            name=data["name"],
            identity_class="individual",
            description="A person",
        )

        return Bundle(objects=[actor]).serialize()