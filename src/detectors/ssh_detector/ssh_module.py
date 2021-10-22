from module import Module

class SSHModule(Module):

    def get_labeler_name(self):
        return "ssh_labeler"

    def get_topic(self):
        return "ssh"

    def get_query(self):
        return {
            'query': {
               'bool': {
                  'must': [{
                        'match': {
                            'destination.ip': self.module_config["dst"]
                      }
                    }, {
                        'match': {
                            'source.ip': self.module_config["src"]
                      }
                    }, {
                        'match': {
                           'destination.port': 22
                        }
                    }]
                }
            }
        }
        