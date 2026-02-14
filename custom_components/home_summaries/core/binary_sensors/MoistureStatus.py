from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from ..GroupBinarySensor import GroupBinarySensor

class MoistureStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.MOISTURE, "Moisture Status"
    )
