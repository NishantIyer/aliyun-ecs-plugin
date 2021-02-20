from schematics import Model
from schematics.types import serializable, ModelType, ListType, StringType
from spaceone.inventory.model import (
    OS,
    Aliyun,
    Hardware,
    SecurityGroup,
    Compute,
    LoadBalancer,
    VPC,
    Subnet,
    ScalingGroup,
    NIC,
    Disk,
    ServerMetadata,
)


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class Tags(Model):
    key = StringType(deserialize_from="TagKey")
    value = StringType(deserialize_from="TagValue")


class ServerData(Model):
    os = ModelType(OS)
    aliyun = ModelType(Aliyun)
    hardware = ModelType(Hardware)
    security_group = ListType(ModelType(SecurityGroup))
    compute = ModelType(Compute)
    load_balancer = ListType(ModelType(LoadBalancer))
    vpc = ModelType(VPC)
    subnet = ModelType(Subnet)
    scaling_group = ModelType(ScalingGroup, serialize_when_none=False)


class Server(Model):
    name = StringType()
    region_code = StringType()
    data = ModelType(ServerData)
    tags = ListType(ModelType(Tags))
    nics = ListType(ModelType(NIC))
    disks = ListType(ModelType(Disk))
    primary_ip_address = StringType(default="")
    ip_addresses = ListType(StringType())
    server_type = StringType(default="VM")
    os_type = StringType(choices=("LINUX", "WINDOWS"))
    provider = StringType(default="alibaba_cloud")
    cloud_service_type = StringType(default="Instance")
    cloud_service_group = StringType(default="ECS")
    _metadata = ModelType(ServerMetadata, serialized_name="metadata")
    reference = ModelType(ReferenceModel)
