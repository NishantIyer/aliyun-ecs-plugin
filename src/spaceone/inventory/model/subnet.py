from schematics import Model
from schematics.types import StringType


class Subnet(Model):
    subnet_id = StringType(deserialize_from="VSwitchId")
    cidr = StringType(deserialize_from="CidrBlock")
    subnet_name = StringType(deserialize_from="VSwitchName")
