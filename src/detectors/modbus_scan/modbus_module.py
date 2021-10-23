from module import Module

class ModbusModule(Module):

    def get_labeler_name(self):
        return "modbus_labeler"

    def get_topic(self):
        return "modbus"

    def get_query(self):
        return {
            'query': {
               'bool': {
                  'must': [{
                        'range': {
                            'destination.bytes': {"gte": 0}
                      }
                    }, {
                        'match': {
                            'source.ip': '192.168.50.115'
                      }
                    }, {
                        'match': {
                           'destination.port': 502
                        }
                    }]
                }
            }
        }
        