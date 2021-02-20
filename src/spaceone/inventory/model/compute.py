from schematics import Model
from schematics.types import StringType, DateTimeType, ListType, ModelType, DictType


class ComputeTags(Model):
    primary_public_ip = StringType(serialize_when_none=False)


class Compute(Model):
    keypair = StringType()
    az = StringType()
    instance_state = StringType(
        choices=("PENDING", "RUNNING", "STARTING", "STOPPING", "STOPPED")
    )
    instance_type = StringType()
    launched_at = DateTimeType()
    instance_id = StringType(default="")
    instance_name = StringType(default="")
    security_groups = ListType(StringType())
    region_name = StringType()
    image = StringType()
    account = StringType()
    tags = ModelType(ComputeTags, default={})
