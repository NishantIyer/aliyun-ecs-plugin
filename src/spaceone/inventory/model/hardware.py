from schematics import Model
from schematics.types import IntType, FloatType, StringType


class Hardware(Model):
    serial_number = StringType(serialize_when_none=False)
    core = IntType(default=0)
    memory = FloatType(default=0.0)
