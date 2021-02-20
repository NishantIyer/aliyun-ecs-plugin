from schematics import Model
from schematics.types import StringType, IntType, ListType, ModelType


class NICTags(Model):
    eni_id = StringType(serialize_when_none=False)


class NIC(Model):
    device_index = IntType()
    device = StringType(default="")
    nic_type = StringType(choices=("Primary", "Secondary"))
    ip_addresses = ListType(StringType())
    cidr = StringType()
    mac_address = StringType()
    public_ip_address = StringType(serialize_when_none=False)
    tags = ModelType(NICTags, default={})
