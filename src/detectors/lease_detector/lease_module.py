from module import Module

class LeaseModule(Module):

    def check_ssid(self, data):
        return data

    def get_labeler_name(self):
        return "lease_labeler"

    def get_topic(self):
        return "lease"

    def get_query(self):

        return {"query": {
                "query_string": {
                  "query": f"zeek.dhcp.address.client:[{self.module_config['subnet_start']} TO {self.module_config['subnet_end']}]"
                        }
                    }
                }
                
