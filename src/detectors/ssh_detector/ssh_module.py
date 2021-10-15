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
                  'should': [{
                        'match': {
                            'destination.ip': '192.168.51.135'
                      }
                    }, {
                        'match': {
                            'source.ip': '192.168.51.138'
                      }
                    }, {
                        'match': {
                           'destination.port': 22
                        }
                    }]
                }
            }
        }
        