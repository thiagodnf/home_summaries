from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from ..GroupBinarySensor import GroupBinarySensor

class WindowStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.WINDOW, "Window Status"
    )
