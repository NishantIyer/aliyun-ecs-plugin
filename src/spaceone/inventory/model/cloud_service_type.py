from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, BooleanType


class CloudServiceType(Model):
    name = StringType(default="Instance")
    provider = StringType(default="alibaba_cloud")
    group = StringType(default="ECS")
    labels = ListType(StringType(), serialize_when_none=False, default=["Compute"])
    tags = DictType(StringType, serialize_when_none=False)
    is_primary = BooleanType(default=True)
    is_major = BooleanType(default=True)
    service_code = StringType(default="ecs")
    resource_type = StringType(default="inventory.Server")
