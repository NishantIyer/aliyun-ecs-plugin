from spaceone.core.manager import BaseManager

from spaceone.inventory.model.metadata.metadata import ServerMetadata
from spaceone.inventory.model.metadata.metadata_dynamic_field import (
    TextDyField,
    EnumDyField,
    ListDyField,
    DateTimeDyField,
    SizeField,
)
from spaceone.inventory.model.metadata.metadata_dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout,
    ListDynamicLayout,
)

ecs_instance = ItemDynamicLayout.set_fields(
    "ECS Instance",
    fields=[
        TextDyField.data_source("Instance ID", "data.compute.instance_id"),
        TextDyField.data_source("Instance Name", "data.compute.instance_name"),
        EnumDyField.data_source(
            "Instance State",
            "data.compute.instance_state",
            default_state={
                "safe": ["RUNNING"],
                "warning": ["STARTING", "PENDING", "STOPPING"],
                "alert": ['STOPPED']
            },
        ),
        TextDyField.data_source("Key Pair", "data.compute.keypair"),
        TextDyField.data_source("Instance Type", "data.compute.instance_type"),
        TextDyField.data_source("Resource Group", "data.aliyun.resource_group_id"),
        TextDyField.data_source("Availability Zone", "data.compute.az"),
        TextDyField.data_source("Public IP", "data.compute.tags.primary_public_ip"),
        ListDyField.data_source(
            "IP Addresses",
            "ip_addresses",
            options={'delimiter': '<br>'}
        ),
        ListDyField.data_source(
            "Affected Rules",
            "data.compute.security_groups",
            options={"delimiter": "<br>"},
        ),
        DateTimeDyField.data_source("Launched At", "data.compute.launched_at"),
        DateTimeDyField.data_source(
            "Auto Release Time", "data.aliyun.auto_release_time"
        ),
    ],
)

vpc = ItemDynamicLayout.set_fields(
    "VPC",
    fields=[
        TextDyField.data_source("VPC ID", "data.vpc.vpc_id"),
        TextDyField.data_source("VPC Name", "data.vpc.vpc_name"),
        TextDyField.data_source("Subnet ID", "data.subnet.subnet_id"),
        TextDyField.data_source("Subnet Name", "data.subnet.subnet_name"),
    ],
)

scaling_group = ItemDynamicLayout.set_fields(
    "Scaling Group",
    fields=[
        TextDyField.data_source("Scaling Group Name", "data.scaling_group.name"),
        TextDyField.data_source("Scaling Group ID", "data.scaling_group.id"),
        TextDyField.data_source(
            "Auto Scaling Configuration ID", "data.scaling_group.active_scaling_configuration_id"
        ),
        TextDyField.data_source("Launch Template ID", "data.scaling_group.launch_template.id"),
    ],
)

ecs = ListDynamicLayout.set_layouts(
    "Alibaba ECS", layouts=[ecs_instance, vpc, scaling_group]
)

disk = TableDynamicLayout.set_fields(
    "Disk",
    root_path="disks",
    fields=[
        TextDyField.data_source("Index", "device_index"),
        TextDyField.data_source("Name", "device"),
        SizeField.data_source("Size(GB)", "size"),
        TextDyField.data_source("Disk ID", "tags.disk_id"),
        TextDyField.data_source("Disk Type", "disk_type"),
        TextDyField.data_source("Read IOPS", "tags.read_iops"),
        TextDyField.data_source("Write IOPS", "tags.write_iops"),
        EnumDyField.data_source(
            "Encrypted",
            "tags.encrypted",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
    ],
)

nic = TableDynamicLayout.set_fields(
    "NIC",
    root_path="nics",
    fields=[
        TextDyField.data_source("Index", "device_index"),
        TextDyField.data_source("MAC Address", "mac_address"),
        ListDyField.data_source(
            "IP Addresses", "ip_addresses", options={"delimiter": "<br>"}
        ),
        TextDyField.data_source("CIDR", "cidr"),
        TextDyField.data_source("Public IP", "public_ip_address"),
    ],
)

security_group = TableDynamicLayout.set_fields(
    "Security Groups",
    root_path="data.security_group",
    fields=[
        EnumDyField.data_source(
            "Direction",
            "direction",
            default_badge={"indigo.500": ["inbound"], "coral.600": ["outbound"]},
        ),
        TextDyField.data_source(
            "Name",
            "security_group_name",
            reference={
                "resource_type": "inventory.CloudService",
                "reference_key": "data.group_name",
            },
        ),
        EnumDyField.data_source(
            "Protocol", "protocol", default_outline_badge=["ALL", "TCP", "UDP", "ICMP"]
        ),
        TextDyField.data_source("Port Rage", "port"),
        TextDyField.data_source("Remote", "remote"),
        TextDyField.data_source("Description", "description"),
    ],
)

slb = TableDynamicLayout.set_fields(
    "SLB",
    root_path="data.load_balancer",
    fields=[
        TextDyField.data_source(
            "Name",
            "name",
            reference={
                "resource_type": "inventory.CloudService",
                "reference_key": "data.load_balancer_name",
            },
        ),
        TextDyField.data_source("Endpoint", "endpoint"),
        ListDyField.data_source("Protocol", "protocol", options={"delimiter": "<br>"}),
        ListDyField.data_source("Port", "port", options={"delimiter": "<br>"}),
        EnumDyField.data_source(
            "Scheme",
            "scheme",
            default_badge={
                "indigo.500": ["internet-facing"],
                "coral.600": ["internal"],
            },
        ),
        TextDyField.data_source("ID", "tags.load_balancer_id"),
    ],
)

tags = TableDynamicLayout.set_fields(
    "Alibaba Cloud Tags",
    root_path="data.aliyun.tags",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

metadata = ServerMetadata.set_layouts([ecs, tags, disk, nic, security_group, slb])


class MetadataManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata
