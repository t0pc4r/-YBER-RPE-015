from module import Module

class TCPNMapModule(Module):

    def get_labeler_name(self):
        return "tcp_nmap_labeler"

    def get_topic(self):
        return "tcp_nmap"
    
    def start_getting_data(self, es):
        topic = self.get_topic()
        labeler = self.get_labeler()

        fields = [
            ("source.ip", "destination.ip", "destination.port"),
            ("id.orig_h", "id.resp_h", "id.resp_p"),
            ("client_addr", "server_addr", "server_port"),
        ]
        for field in fields:
            query = self.get_dsts_query(*field)
            results = es.search(body=query, size=10000)
            for source_results in results["aggregations"]["sources"]["buckets"]:
                for dates_results in source_results["dates"]["buckets"]:
                    for destinations_results in dates_results["destinations"]["buckets"]:
                        num_unique = destinations_results["ports"]["value"]
                        if num_unique > 512:
                            data = {
                                "src_ip": source_results["key"],
                                "dst_ip": destinations_results["key"],
                                "start_time": dates_results["key"],
                                "end_Tme": dates_results["key"] + 300000,
                            }
                            self.send_to_labeler(labeler, topic, data)

    def get_dsts_query(self, source_field, destination_field, destination_port_field):
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
                                    "terms": {
                                        "field": destination_field
                                    },
                                    "aggs": {
                                        "ports": {
                                            "cardinality": {
                                                "field": destination_port_field
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
            