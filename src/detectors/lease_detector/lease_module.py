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
                  "query": "zeek.dhcp.address.client:[192.168.51.0 TO 192.168.51.255]"
                        }
                    }
                }


        # return {
        #       "query": {
        #         "bool": {
        #           "must": [],
        #           "filter": [
        #             {
        #               "bool": {
        #                 "should": [
                          
        #                   {
        #                     "exist":{
        #                         "field" : "zeek.dhcp.address.client"
        #                     }
        #                   }
        #                 ],
        #                 "minimum_should_match": 1
        #               }
        #             },
        #             {
        #               "match_all": {}
        #             },
        #             {
        #               "range": {
        #                 "@timestamp": {
        #                   "gte": "2021-09-10T14:00:00.000Z",
        #                   "lte": "2021-09-10T15:00:00.000Z",
        #                   "format": "strict_date_optional_time"
        #                 }
        #               }
        #             }
        #           ],
        #           "should": [],
        #           "must_not": []
        #         }
        #       }
        #     }

        # return {
        #     'query': {
        #        'bool': {
        #           'should': [{
        #                 'match': {
        #                     'zeek.dhcp.client_address': '192.168.51.138'
        #                 }
                      
        #             }]
        #         }
        #     }
        # }
