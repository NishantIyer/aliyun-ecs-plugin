from spaceone.core.manager import BaseManager

from spaceone.inventory.model.subnet import Subnet
from spaceone.inventory.model.vpc import VPC


class VPCManager(BaseManager):
    def __init__(self, params, ecs_connector=None):
        self.params = params
        self.ecs_connector = ecs_connector

    def get_vpc_info(self, vpc_id, subnet_id, vpcs, subnets):
        """
        vpc_data = {
            "vpc_name": "",
            "vpc_id": "",
            "cidr": "",
        }

        subnet_data = {
            "subnet_name": "",
            "subnet_id": "",
            "cidr": ""
        }
        """

        matched_vpc = self.get_matched_vpc(vpc_id, vpcs)
        matched_subnet = self.get_matched_subnet(subnet_id, subnets)

        return VPC(matched_vpc, strict=False), Subnet(matched_subnet, strict=False)

    @staticmethod
    def get_matched_vpc(vpc_id, vpcs):
        for vpc in vpcs:
            if vpc_id == vpc["VpcId"]:
                return vpc
        return None

    @staticmethod
    def get_matched_subnet(subnet_id, subnets):
        for subnet in subnets:
            if subnet_id == subnet["VSwitchId"]:
                return subnet
        return None
