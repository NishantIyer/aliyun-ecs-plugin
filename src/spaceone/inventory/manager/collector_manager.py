__all__ = ["CollectorManager"]

import logging
import time

from spaceone.core.manager import BaseManager

from spaceone.inventory.connector import ECSConnector
from spaceone.inventory.manager.ecs import (
    ECSInstanceManager,
    VPCManager,
    NICManager,
    SecurityGroupManager,
)
from spaceone.inventory.manager.ecs import (
    ScalingGroupManager,
    LoadBalancerManager,
    DiskManager,
)
from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.cloud_service_type import CloudServiceType
from spaceone.inventory.model.region import Region
from spaceone.inventory.model.server import Server, ReferenceModel

_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):
    def __init__(self, transaction):
        super().__init__(transaction)

    def verify(self, secret_data, region_name):
        """Check connection"""
        ecs_connector = self.locator.get_connector("ECSConnector")
        r = ecs_connector.verify(secret_data, region_name)
        return r

    def list_regions(self, secret_data, region_name):
        ecs_connector: ECSConnector = self.locator.get_connector("ECSConnector")
        ecs_connector.set_client(secret_data, region_name)

        return ecs_connector.list_regions()

    def list_instances(self, params):
        server_vos = []
        ecs_connector: ECSConnector = self.locator.get_connector("ECSConnector")
        ecs_connector.set_client(params["secret_data"], params["region_name"])

        instance_filter = {}
        if "instance_ids" in params and len(params["instance_ids"]) > 0:
            instance_filter["InstanceIds"] = params["instance_ids"]

        instances = ecs_connector.list_instances(**instance_filter)

        print(f'===== [{params["region_name"]}]  /  INSTANCE COUNT : {len(instances)}')

        if len(instances) > 0:
            ins_manager: ECSInstanceManager = ECSInstanceManager(
                params, ecs_connector=ecs_connector
            )
            asg_manager: ScalingGroupManager = ScalingGroupManager(params)
            lb_manager: LoadBalancerManager = LoadBalancerManager(
                params, ecs_connector=ecs_connector
            )
            disk_manager: DiskManager = DiskManager(params)
            vpc_manager: VPCManager = VPCManager(params)
            nic_manager: NICManager = NICManager(params)
            sg_manager: SecurityGroupManager = SecurityGroupManager(
                params, ecs_connector=ecs_connector
            )
            meta_manager: MetadataManager = MetadataManager()

            scaling_groups = ecs_connector.list_scaling_groups()
            scaling_instances = ecs_connector.list_scaling_instances()
            load_balancers = ecs_connector.list_load_balancers()
            disks = ecs_connector.list_disks()
            vpcs = ecs_connector.list_vpcs()
            subnets = ecs_connector.list_subnets()
            nics = ecs_connector.list_nics()
            sgs = ecs_connector.list_security_groups()

            for instance in instances:
                instance_id = instance.get("InstanceId")
                public_ips = instance.get("PublicIpAddress", {}).get("IpAddress", [])
                eip = instance.get("EipAddress", {}).get("IpAddress", "")
                instance_ip, nic_ids = self.get_network_info(
                    instance.get("NetworkInterfaces", {}).get("NetworkInterface", [])
                )
                sg_ids = instance.get("SecurityGroupIds", {}).get("SecurityGroupId", [])
                vpc_id = instance.get("VpcAttributes", {}).get("VpcId", "")
                vswitch_id = instance.get("VpcAttributes", {}).get("VSwitchId", "")
                server_data = ins_manager.get_server_info(instance, self.get_primary_public_ip(public_ips, eip))
                scaling_group_vo = asg_manager.get_scaling_info(
                    instance_id, scaling_groups, scaling_instances
                )
                load_balancer_vos = lb_manager.get_load_balancer_info(
                    instance_id, load_balancers
                )
                disk_vos = disk_manager.get_disk_info(instance_id, disks)
                vpc_vo, subnet_vo = vpc_manager.get_vpc_info(
                    vpc_id, vswitch_id, vpcs, subnets
                )
                nic_vos, account_id = nic_manager.get_nic_info(
                    nic_ids, nics, subnet_vo, public_ips
                )
                sg_rules_vos = sg_manager.get_security_group_info(sg_ids, sgs)

                server_data.update(
                    {
                        "nics": nic_vos,
                        "disks": disk_vos,
                        "region_code": params.get("region_name", ""),
                        "tags": instance.get("Tags", {}).get("Tag", []),
                    }
                )

                server_data["data"].update(
                    {
                        "load_balancer": load_balancer_vos,
                        "vpc": vpc_vo,
                        "subnet": subnet_vo,
                        "security_group": sg_rules_vos,
                    }
                )

                if scaling_group_vo:
                    server_data["data"].update({"scaling_group": scaling_group_vo})

                server_data.update(
                    {
                        "ip_addresses": self.merge_ip_addresses(
                            server_data["nics"], public_ips
                        ),
                        "primary_ip_address": instance_ip,
                    }
                )

                server_data["data"]["compute"]["account"] = account_id

                server_data.update(
                    {
                        "_metadata": meta_manager.get_metadata(),
                        "reference": ReferenceModel(
                            {
                                "resource_id": server_data["data"]["compute"][
                                    "instance_id"
                                ],
                                "external_link": f"https://ecs.console.aliyun.com/#/server/{server_data['data']['compute']['instance_id']}/detail?regionId={params.get('region_name')}",
                            }
                        ),
                    }
                )

                server_vos.append(Server(server_data, strict=False))
        return server_vos

    def list_resources(self, params):
        start_time = time.time()
        try:
            resources = self.list_instances(params)
            print(
                f'   [{params["region_name"]}] Finished {time.time() - start_time} Seconds'
            )
            return resources
        except Exception as e:
            print(f'[ERROR: {params["region_name"]}] : {e}')
            raise e

    @staticmethod
    def list_cloud_service_types():
        cloud_service_type = {
            "tags": {
                "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/alibaba_cloud/ecs.svg",
            }
        }
        return [CloudServiceType(cloud_service_type, strict=False)]

    @staticmethod
    def get_network_info(nics):
        nic_ids = []
        instance_ip = ""
        for nic in nics:
            if nic.get("Type", "") == "Primary":
                instance_ip = nic.get("PrimaryIpAddress", "")
            nic_ids.append(nic.get("NetworkInterfaceId", ""))
        return instance_ip, nic_ids

    @staticmethod
    def get_primary_public_ip(public_ips, eip):
        if eip:
            return eip
        if len(public_ips) > 0:
            return public_ips[0]
        return None

    @staticmethod
    def merge_ip_addresses(nics, public_ips):
        merge_ip_address = []
        for nic in nics:
            merge_ip_address.extend(nic.ip_addresses)
            if nic.public_ip_address:
                merge_ip_address.append(nic.public_ip_address)
        merge_ip_address.extend(public_ips)
        return list(set(merge_ip_address))

    @staticmethod
    def get_region_from_result(result):
        REGION_INFO = {
            "cn-qingdao": {
                "name": "China (Qingdao)",
                "tags": {
                    "latitude": "36.081218214171784",
                    "longitude": "120.3628877928574",
                },
            },
            "cn-beijing": {
                "name": "China (Beijing)",
                "tags": {
                    "latitude": "39.94834292935469",
                    "longitude": "116.4060768268714",
                },
            },
            "cn-zhangjiakou": {
                "name": "China (Zhangjiakou)",
                "tags": {
                    "latitude": "40.84584053414792",
                    "longitude": "114.87072549694297",
                },
            },
            "cn-huhehaote": {
                "name": "China (Hohhot)",
                "tags": {
                    "latitude": "40.847546612171755",
                    "longitude": "111.74407264424472",
                },
            },
            "cn-wulanchabu": {
                "name": "China (Ulanqab)",
                "tags": {
                    "latitude": "40.99525035257898",
                    "longitude": "113.12965231297925",
                },
            },
            "cn-shanghai": {
                "name": "China (Shanghai)",
                "tags": {
                    "latitude": "31.602081881372037",
                    "longitude": "121.7667292823462",
                },
            },
            "cn-shenzhen": {
                "name": "China (Shenzhen)",
                "tags": {
                    "latitude": "22.547439315725928",
                    "longitude": "114.05768428043767",
                },
            },
            "cn-heyuan": {
                "name": "China (Heyuan)",
                "tags": {
                    "latitude": "23.749439500376305",
                    "longitude": "114.72066115956231",
                },
            },
            "cn-chengdu": {
                "name": "China (Chengdu)",
                "tags": {
                    "latitude": "30.57381902273429",
                    "longitude": "104.05420761032428",
                },
            },
            "cn-hongkong": {
                "name": "China (Hong Kong)",
                "tags": {
                    "latitude": "22.3247181577869",
                    "longitude": "114.155844453261",
                },
            },
            "ap-southeast-1": {
                "name": "Singapore (Singapore)",
                "tags": {
                    "latitude": "1.3558701301937892",
                    "longitude": "103.86758728272277",
                },
            },
            "ap-southeast-2": {
                "name": "Australia (Sydney)",
                "tags": {
                    "latitude": "-33.84624551606316",
                    "longitude": "151.25600021645818",
                },
            },
            "ap-southeast-3": {
                "name": "Malaysia (Kuala Lumpur)",
                "tags": {
                    "latitude": "3.144383484139312",
                    "longitude": "101.67825446230306",
                },
            },
            "ap-southeast-5": {
                "name": "Indonesia (Jakarta)",
                "tags": {
                    "latitude": "-6.209605070636339",
                    "longitude": "106.84633866469763",
                },
            },
            "ap-south-1": {
                "name": "India (Mumbai)",
                "tags": {
                    "latitude": "19.08998463456083",
                    "longitude": "72.87499814036964",
                },
            },
            "ap-northeast-1": {
                "name": "Japan (Tokyo)",
                "tags": {
                    "latitude": "35.759272758953585",
                    "longitude": "139.7850855561631",
                },
            },
            "us-west-1": {
                "name": "US (Silicon Valley)",
                "tags": {"latitude": "37.3875", "longitude": "122.0575"},
            },
            "us-east-1": {
                "name": "US East (N. Virginia)",
                "tags": {"latitude": "39.028760", "longitude": "-77.458263"},
            },
            "eu-central-1": {
                "name": "Germany (Frankfurt)",
                "tags": {
                    "latitude": "50.13178191975637",
                    "longitude": "8.707738873275808",
                },
            },
            "eu-west-1": {
                "name": "UK (London)",
                "tags": {
                    "latitude": "51.5563393266161",
                    "longitude": "-0.158378833868658",
                },
            },
            "me-east-1": {
                "name": "UAE (Dubai)",
                "tags": {
                    "latitude": "25.335725641664382",
                    "longitude": "55.29667430453258",
                },
            },
        }

        match_region_info = REGION_INFO.get(
            getattr(result.data.compute, "region_name", None)
        )

        if match_region_info :
            region_info = match_region_info.copy()
            region_info.update({"region_code": result.data.compute.region_name})

            return Region(region_info, strict=False)

        return None
