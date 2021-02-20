from spaceone.core.manager import BaseManager

from spaceone.inventory.connector import ECSConnector
from spaceone.inventory.model.load_balancer import LoadBalancer


class LoadBalancerManager(BaseManager):
    def __init__(self, params, ecs_connector=None, **kwargs):
        self.params = params
        self.ecs_connector: ECSConnector = ecs_connector

    def get_load_balancer_info(self, instance_id, lbs):
        """
        load_balancer_data_list = [{
                "endpoint": "0.0.0.0",
                "type": "classic" | "vpc",
                "scheme": 'internet-facing'|'internal,
                "name": "",
                "port": [
                    50051
                ],
                "protocol": [
                    "TCP"
                ],
                 "tags": {
                    "load_balancer_id": "",
                    "load_balancer_spec": ""
                 },
            },
            ...
        ]
        """
        if lbs is None:
            return []

        load_balancer_data_list = []

        for lb in lbs:
            lb_attributes = self.ecs_connector.list_load_balancer_attributes(
                lb.get("LoadBalancerId")
            )
            lb_servers = lb_attributes.get("BackendServers", {}).get(
                "BackendServer", []
            )
            for lb_server in lb_servers:
                if instance_id == lb_server.get("ServerId", ""):
                    load_balancer_data_list.append(
                        self.get_refined_load_balancer_data(lb, lb_attributes)
                    )
        return load_balancer_data_list

    def get_refined_load_balancer_data(self, load_balancer, its_attributes):
        load_balancer_data = {
            "endpoint": load_balancer.get("Address", ""),
            "type": load_balancer.get("NetworkType", ""),
            "scheme": self.get_scheme(load_balancer.get("AddressType")),
            "name": load_balancer.get("LoadBalancerName", ""),
            "protocol": self.get_protocol(
                its_attributes.get("ListenerPortsAndProtocol", {}).get(
                    "ListenerPortAndProtocol", []
                )
            ),
            "port": its_attributes.get("ListenerPorts", {}).get("ListenerPort", []),
            "tags": {
                "load_balancer_id": its_attributes.get("LoadBalancerId"),
                "load_balancer_spec": its_attributes.get("LoadBalancerSpec"),
            },
        }
        return LoadBalancer(load_balancer_data, strict=False)

    @staticmethod
    def get_scheme(address_type):
        if address_type == "intranet":
            return "internal"
        elif address_type == "internet":
            return "internet-facing"
        else:
            return ""

    @staticmethod
    def get_protocol(listeners):
        return [
            listener.get("ListenerProtocol")
            for listener in listeners
            if listener.get("ListenerProtocol") is not None
        ]
