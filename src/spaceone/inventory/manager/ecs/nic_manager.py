from spaceone.core.manager import BaseManager

from spaceone.inventory.model.nic import NIC


class NICManager(BaseManager):
    def __init__(self, params, ecs_connector=None):
        self.params = params
        self.ecs_connector = ecs_connector

    def get_nic_info(self, nic_ids, nics, subnet_vo, public_ips):
        """
        nic_data = {
            "device_index": 0,
            "nic_type": "Primary" || "Secondary",
            "ip_addresses": [],
            "cidr": "",
            "mac_address": "",
            "public_ip_address": "",
            "tags": {
                "eni_id":""
            }
        }
        """

        matched_nics = self.get_matched_nics(nic_ids, nics)
        nics_data = []
        account_id = ""
        index = 0
        for nic_cnt, matched_nic in enumerate(matched_nics):
            nic_data = {
                "device_index": index
                if matched_nic.get("Type", "") == "Secondary"
                else 0,
                "nic_type": matched_nic.get("Type", ""),
                "ip_addresses": self.get_private_ips(
                    matched_nic.get("PrivateIpSets", {}).get("PrivateIpSet", [])
                ),
                "cidr": subnet_vo.cidr,
                "mac_address": matched_nic.get("MacAddress"),
                "public_ip_address": matched_nic.get("AssociatedPublicIp", "").get(
                    "PublicIpAddress", None
                ),
                "tags": {
                    "eni_id": matched_nic.get("NetworkInterfaceId", ""),
                },
            }
            if len(public_ips) > 0:
                nic_data["public_ip_address"] = public_ips[nic_cnt]
            account_id = matched_nic.get("OwnerId", "")
            index += 1

            nics_data.append(NIC(nic_data, strict=False))

        return nics_data, account_id

    @staticmethod
    def get_private_ips(private_ips):
        return [
            ip.get("PrivateIpAddress")
            for ip in private_ips
            if ip.get("PrivateIpAddress") is not None
        ]

    @staticmethod
    def get_matched_nics(nic_ids, nics):
        matched_nics = []
        for nic in nics:
            if nic.get("NetworkInterfaceId", "") in nic_ids:
                matched_nics.append(nic)
        return matched_nics
