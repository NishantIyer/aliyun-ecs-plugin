from schematics import Model
from schematics.types import StringType, IntType, ListType, ModelType


class LoadBalancerTags(Model):
    load_balancer_id = StringType()
    load_balancer_spec = StringType()


class LoadBalancer(Model):
    type = StringType(choices=("classic", "vpc"))
    endpoint = StringType()
    port = ListType(IntType())
    name = StringType()
    protocol = ListType(StringType())
    scheme = StringType(choices=("internet-facing", "internal"))
    tags = ModelType(LoadBalancerTags, default={})
