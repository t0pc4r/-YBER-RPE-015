from module import Module

class TrafficModule(Module):

    def get_query(self):
        return {
            "query": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {
                                        "exists": {
                                            "field": "destination.ip"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "source.ip"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "destination.port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "source.port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "network.transport"
                                        }
                                    }
                                ]
                            }
                        }, {
                            "bool": {
                                "must": [
                                    {
                                        "exists": {
                                            "field": "zeek.notice.id.resp_h"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "zeek.notice.id.orig_h"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "zeek.notice.id.resp_p"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "zeek.notice.id.orig_p"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "zeek.notice.id.note"
                                        }
                                    }
                                ]
                            }
                        }, {
                            "bool": {
                                "must": [
                                    {
                                        "exists": {
                                            "field": "netflow.destination_ipv4_address"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "netflow.source_ipv4_address"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "netflow.destination_transport_port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "netflow.source_transport_port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "netflow.protocol_identifier"
                                        }
                                    }
                                ]
                            }
                        }, {
                            "bool": {
                                "must": [
                                    {
                                        "exists": {
                                            "field": "suricata.eve.dst_ip"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "suricata.eve.src_ip"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "suricata.eve.dst_port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "suricata.eve.src_port"
                                        }
                                    }, {
                                        "exists": {
                                            "field": "suricata.eve.proto"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        