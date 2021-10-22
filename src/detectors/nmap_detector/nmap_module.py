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
            ("source.ip", "destination.ip", "network.transport"),
            ("zeek.notice.id.orig_h ", "zeek.notice.id.resp_h", "zeek.notice.id.note"), # no proto field was observed and no instances of zeek.notice have been observed anyway
            ("netflow.source_ipv4_address", "netflow.destination_ipv4_address", "netflow.protocol_identifier"),
            ("suricata.eve.src_ip", "suricata.eve.dst_ip", "suricata.eve.proto"),
        ]
        min_ips_polled = self.module_config["min_ips_polled"]
        for field in fields:
            query = self.get_dsts_query(*field)
            results = es.search(body=query, size=10000)
            for source_results in results["aggregations"]["sources"]["buckets"]:
                for protocols_results in source_results["protocols"]["buckets"]:
                    for dates_results in protocols_results["dates"]["buckets"]:
                        num_unique = dates_results["destinations"]["value"]
                        if num_unique >= min_ips_polled:
                            data = {
                                "src_ip": source_results["key"],
                                "ip_range": self.module_config["destination_block"],
                                "protocol": protocols_results["key"],
                                "start_time": dates_results["key"],
                                "end_time": dates_results["key"] + self.module_config["time_window_minutes"] * 60000,
                            }
                            self.send_to_labeler(labeler, topic, data)

    def get_dsts_query(self, source_field, destination_field, protocol_field):
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                destination_field: self.module_config["destination_block"]
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
                        "protocols": {
                            "terms": {
                                "field": protocol_field
                            },
                            "aggs": {
                                "dates": {
                                    "date_histogram": {
                                        "field": "@timestamp",
                                        "interval": "%dm" % self.module_config["time_window_minutes"]
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
            }
        }
            