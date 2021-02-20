from schematics import Model
from schematics.types import StringType, IntType


class SecurityGroup(Model):
    protocol = StringType()
    remote = StringType(serialize_when_none=False)
    remote_id = StringType(serialize_when_none=False)
    remote_cidr = StringType(serialize_when_none=False)
    security_group_name = StringType(serialize_when_none=False)
    port_range_min = IntType(serialize_when_none=False)
    port_range_max = IntType(serialize_when_none=False)
    security_group_id = StringType()
    description = StringType(default="")
    direction = StringType(choices=("inbound", "outbound"))
    port = StringType(serialize_when_none=False)
    action = StringType(choices=("allow", "deny"))
