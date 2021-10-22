from module import Module

class SSHModule(Module):

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
        