from schematics import Model
from schematics.types import (
    ModelType,
    StringType,
    BooleanType,
    ListType,
    IntType,
    FloatType,
    DateTimeType,
)


class Tags(Model):
    key = StringType(deserialize_from="TagKey")
    value = StringType(deserialize_from="TagValue")


class Aliyun(Model):
    resource_group_id = StringType(serialize_when_none=False)
    instance_type_family = StringType()
    instance_network_type = StringType(choices=("classic", "vpc"))
    instance_charge_type = StringType(choices=("PostPaid", "PrePaid"))
    internet_charge_type = StringType(choices=("PayByBandwidth", "PayByTraffic"))
    internet_max_bandwidth_in = IntType(serialize_when_none=False)
    internet_max_bandwidth_out = IntType(serialize_when_none=False)
    io_optimized = BooleanType()
    gpu_spec = StringType()
    gpu_amount = IntType()
    recyclable = BooleanType()
    stopped_mode = StringType(
        choices=("KeepCharging", "StopCharging", "Not-applicable")
    )
    credit_specification = StringType(choices=("Standard", "Unlimited"))
    spot_duration = IntType(serialize_when_none=False)
    spot_price_limit = FloatType()
    spot_strategy = StringType(
        choices=("no_spot", "spot_with_price_limit", "spot_as_price_go")
    )
    auto_release_time = DateTimeType(serialize_when_none=False)
    tags = ListType(ModelType(Tags), serialize_when_none=False)
