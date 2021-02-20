from schematics import Model
from schematics.types import StringType, IntType, BooleanType, ModelType


class DiskTags(Model):
    disk_id = StringType()
    disk_name = StringType(serialize_when_none=False)
    encrypted = BooleanType()
    iops_read = IntType(serialize_when_none=False)
    iops_write = IntType(serialize_when_none=False)
    performance_level = StringType(serialize_when_none=False)
    disk_charge_type = StringType(choices=("PrePaid", "PostPaid"))


class Disk(Model):
    device_index = IntType()
    device = StringType()
    disk_type = StringType(default="all")
    size = IntType()
    tags = ModelType(DiskTags, default={})
