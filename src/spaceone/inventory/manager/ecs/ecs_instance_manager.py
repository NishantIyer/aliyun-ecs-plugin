from pprint import pprint

from spaceone.core.manager import BaseManager

from spaceone.inventory.connector.ecs_connector import ECSConnector
from spaceone.inventory.model.aliyun import Aliyun
from spaceone.inventory.model.compute import Compute
from spaceone.inventory.model.hardware import Hardware
from spaceone.inventory.model.os import OS


class ECSInstanceManager(BaseManager):
    def __init__(self, params, ecs_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.ecs_connector: ECSConnector = ecs_connector

    def get_server_info(self, instance, primary_public_ip):
        """
        server_data = {
            "os_type": "LINUX" | "WINDOWS"
            "name": ""
            "ip_addresses": [],
            "primary_ip_address": "",
            "data":  {
                "os": {
                    "os_distro": "",
                    "os_arch": "",
                },
            "aliyun":{
                "instance_type_family": "",
                "instance_network_type": "",
                "instance_charge_type": "",
                "internet_charge_type": "",
                "internet_max_bandwidth_in": "",
                "internet_max_bandwidth_out": "",
                "io_optimized": "",
                "gpu_spec": "",
                "gpu_amount": "",
                "recyclable": "",
                "stopped_mode": "",
                "credit_specification": "",
                "spot_duration": "",
                "spot_price_limit": "",
                "spot_strategy": "",
                "tags": {},
            },
            "hardware": {
                "core": 0,
                "memory": 0
            },
            "compute": {
                "keypair": "",
                "availability_zone": "",
                "instance_state": "",
                "instance_type": "",
                "launched_at": "datetime",
                "instance_id": "",
                "instance_name": "",
                "sgs": [
                    {
                        "id": "",
                        "name": "",
                        "display": ""
                    },
                    ...
                ],
                "image": "",
                "account": "",
            },
            }
        }
        """

        server_dic = self.get_server_dic(instance)
        os_data = self.get_os_data(instance.get("OSNameEn", ""), instance.get("OSType"))
        aliyun_data = self.get_aliyun_data(instance)
        hardware_data = self.get_hardware_data(instance)
        compute_data = self.get_compute_data(instance, primary_public_ip)

        server_dic.update(
            {
                "data": {
                    "os": os_data,
                    "aliyun": aliyun_data,
                    "hardware": hardware_data,
                    "compute": compute_data,
                },
            }
        )
        return server_dic

    @staticmethod
    def get_server_dic(instance):
        server_data = {
            "name": instance.get("InstanceName"),
            "os_type": instance.get("OSType").upper(),
            "region_code": instance.get("RegionId"),
        }
        return server_data

    def get_os_data(self, os_name_en, os_type):
        os_data = {
            "os_distro": self.get_os_distro(os_name_en, os_type),
            "os_arch": self.get_os_arch(os_name_en),
            "details": os_name_en,
        }
        return OS(os_data, strict=False)

    def get_aliyun_data(self, instance):
        aliyun_data = {
            "resource_group_id": "default"
            if instance.get("ResourceGroupId") == ""
            else instance.get("ResourceGroupId"),
            "instance_type_family": instance.get("InstanceTypeFamily"),
            "instance_network_type": instance.get("InstanceNetworkType"),
            "internet_charge_type": None if instance.get("InternetChargeType") == "" else instance.get(
                "InternetChargeType", None),
            "internet_max_bandwidth_in": instance.get("InternetMaxBandwidthIn"),
            "internet_max_bandwidth_out": instance.get("InternetMaxBandwidthOut"),
            "io_optimized": instance.get("IoOptimized"),
            "gpu_spec": None if instance.get("GPUSpec") == "" else instance.get("GPUSpec", None),
            "gpu_amount": instance.get("GPUAmount"),
            "recyclable": instance.get("Recyclable"),
            "stopped_mode": instance.get("StoppedMode"),
            "credit_specification": instance.get("CreditSpecification"),
            "spot_duration": instance.get("SpotDuration"),
            "spot_price_limit": instance.get("SpotPriceLimit"),
            "spot_strategy": instance.get("SpotStrategy"),
            "tags": instance.get("Tags", {}).get("Tag", []),
        }
        if instance.get("AutoReleaseTime"):
            aliyun_data.update({"auto_release_time": instance.get("AutoReleaseTime")})
        return Aliyun(aliyun_data, strict=False)

    def get_hardware_data(self, instance):
        hardware_data = {
            "core": instance.get("CpuOptions", {}).get("CoreCount", 0),
            "memory": round(float((instance.get("Memory", 0)) / 1024), 2),
        }

        return Hardware(hardware_data, strict=False)

    @staticmethod
    def get_compute_data(instance, primary_public_ip):
        compute_data = {
            "keypair": instance.get("KeyPairName", ""),
            "az": instance.get("ZoneId", ""),
            "instance_state": instance.get("Status").upper(),
            "instance_type": instance.get("InstanceType", ""),
            "launched_at": instance.get("CreationTime"),
            "instance_id": instance.get("InstanceId"),
            "instance_name": instance.get("InstanceName"),
            "region_name": instance.get("RegionId"),
            "security_groups": instance.get("SecurityGroupIds", {}).get(
                "SecurityGroupId", []
            ),
            "image": instance.get("ImageId")
        }
        if primary_public_ip:
            compute_data.update({
                "tags": {
                    "primary_public_ip": primary_public_ip
                }
            })
        return Compute(compute_data, strict=False)

    @staticmethod
    def get_os_arch(os_name_en):
        if "bit" in os_name_en:
            if "64" in os_name_en:
                return "x86_64"
            elif "32" in os_name_en:
                return "x86_32"
        return ""

    def get_os_distro(self, os_name_en, os_type):
        return (
            os_type.lower()
            if os_name_en == ""
            else self.extract_os_distro(os_name_en.lower(), os_type)
        )

    @staticmethod
    def extract_os_distro(os_name_en, os_type):
        if os_type == "linux":
            os_map = {
                "suse": "suse",
                "red hat": "redhat",
                "centos": "centos",
                "fedora": "fedora",
                "ubuntu": "ubuntu",
                "debian": "debian",
                "alibaba cloud linux": "aliyunlinux",
                "coreos": "coreos",
                "freebsd": "freebsd",
            }

            for key in os_map:
                if key in os_name_en:
                    return os_map[key]

            return os_type

        elif os_type == "windows":

            version_cmp = [
                int(word)
                for word in os_name_en.split()
                if word.isdigit() and len(word) == 4
            ][0]
            os_distro_string = f"win{version_cmp}"
            if "R2" in os_name_en:
                os_distro_string += "r2"
            if "data" in os_name_en and "center" in os_name_en:
                os_distro_string += "dc"
            if "enterprise" in os_name_en:
                os_distro_string += "ent"
            if os_distro_string is None:
                os_distro_string = os_type

            return os_distro_string
