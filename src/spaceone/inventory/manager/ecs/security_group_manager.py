from spaceone.core.manager import BaseManager

from spaceone.inventory.model import SecurityGroup


class SecurityGroupManager(BaseManager):
    def __init__(self, params, ecs_connector=None):
        self.params = params
        self.ecs_connector = ecs_connector

    def get_security_group_info(self, sg_ids, sgs):
        """
        "data.security_group" = [
                    {
                        "priority": "",
                        "protocol": "",
                        "remote": "",
                        "remote_id": "",
                        "remote_cidr": "",
                        "security_group_name": "",
                        "security_group_id": "",
                        "port_range_min": 0,
                        "port_range_max": 65535,
                        "description": "",
                        "direction": "inbound" || "outbound",
                        "port": "",
                        "action": "allow" || "deny"
                    }
                ],
        """

        sg = []
        if sg_ids is None:
            return sg
        matched_sgs = self.get_matched_sgs_from_ids(sg_ids, sgs)
        for matched_sg in matched_sgs:
            sg_data = self.set_sg_base_data(matched_sg)
            for permission in matched_sg.get("Permissions", {}).get("Permission", []):
                sg.append(self.get_refined_sg_data(sg_data, permission))
        return sg

    @staticmethod
    def get_matched_sgs_from_ids(sg_ids, sgs):
        sgs_data = []
        for sg in sgs:
            if sg.get("SecurityGroupId", "") in sg_ids:
                sgs_data.append(sg)
        return sgs_data

    @staticmethod
    def set_sg_base_data(matched_sg):
        sg_data = {
            "security_group_name": matched_sg.get("SecurityGroupName", ""),
            "security_group_id": matched_sg.get("SecurityGroupId"),
            "direction": "inbound"
            if matched_sg.get("Direction", "") == "ingress"
            else "outbound",
            "action": "allow" if matched_sg.get("Policy", "") == "Accept" else "deny",
        }
        return sg_data

    def get_refined_sg_data(self, sg_data, permission):
        port, port_range_min, port_range_max = self.get_refined_port_info(
            permission.get("PortRange", "")
        )
        sg_data.update(
            {
                "priority": permission.get("Priority", 1),
                "protocol": permission.get("IpProtocol", ""),
                "remote": self.get_refined_remote(permission.get("DestGroupName", "")),
                "remote_id": self.get_refined_remote(permission.get("DestGroupId", "")),
                "remote_cidr": self.get_refined_remote(
                    permission.get("DestCidrIp", "")
                ),
                "port_range_min": port_range_min,
                "port_range_max": port_range_max,
                "port": port,
                "description": permission.get("Description", ""),
            }
        )
        return SecurityGroup(sg_data, strict=False)

    @staticmethod
    def get_refined_remote(remote):
        return "*" if remote == "" else remote

    @staticmethod
    def get_refined_port_info(port_str):
        try:
            port_range_min = port_str.split("/")[0]
            port_range_max = port_str.split("/")[1]
        except IndexError:
            port_range_min = 0
            port_range_max = 65535
        port = (
            port_range_min
            if port_range_min == port_range_max
            else f"{port_range_min} - {port_range_max}"
        )
        return port, port_range_min, port_range_max
