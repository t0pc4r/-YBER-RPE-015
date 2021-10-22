from module import Module

class NMapModule(Module):

    def get_labeler_name(self):
        return "nmap_labeler"

    def get_topic(self):
        return "nmap"
    
    def start_getting_data(self, es):
        topic = self.get_topic()
        labeler = self.get_labeler()

        fields = [
            ("source.ip", "destination.ip"),
            ("source.ip", "destination.ip"),
            ("id.orig_h", "id.resp_h"),
            ("client_addr", "server_addr"),
        ]
        for field in fields:
            query = self.get_dsts_query(*field)
            results = es.search(body=query, size=10000)
            for source_results in results["aggregations"]["sources"]["buckets"]:
                for dates_results in source_results["dates"]["buckets"]:
                    num_unique = dates_results["destinations"]["value"]
                    if num_unique > 200:
                        data = {
                            "src_ip": source_results["key"],
                            "ip_range": "192.168.51.0/24",
                            "start_time": dates_results["key"],
                            "end_Tme": dates_results["key"] + 1800000,
                        }
                        self.send_to_labeler(labeler, topic, , data)

    def get_dsts_query(self, source_field, destination_field):
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                destination_field: "192.168.51.0/24"
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "sources": {
                    "terms": {
                        "field": source_field
                    },
                    "aggs": {
                        "dates": {
                            "date_histogram": {
                                "field": "@timestamp",
                                "interval": "30m"
                            },
                            "aggs": {
                                "destinations": {
                                    "cardinality": {
                                        "field": destination_field
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
            