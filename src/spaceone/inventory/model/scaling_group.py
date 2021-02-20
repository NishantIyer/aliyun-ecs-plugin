from schematics import Model
from schematics.types import StringType, ModelType


class LaunchTemplate(Model):
    id = StringType(deserialize_from="LaunchTemplateId")
    version = StringType(deserialize_from="Version")


class ScalingGroup(Model):
    id = StringType()
    name = StringType()
    active_scaling_configuration_id = StringType(serialize_when_none=False)
    launch_template = ModelType(LaunchTemplate, serialize_when_none=False)
