from schematics import Model
from schematics.types import StringType


class VPC(Model):
    vpc_id = StringType(deserialize_from="VpcId")
    cidr = StringType(deserialize_from="CidrBlock")
    vpc_name = StringType(deserialize_from="VpcName")
