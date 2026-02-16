from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .GroupBinarySensor import GroupBinarySensor

class DoorStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.DOOR, "Door Status"
    )

class MoistureStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.MOISTURE, "Moisture Status"
    )

class MotionStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.MOTION, "Motion Status"
    )

class WindowStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
      device, BinarySensorDeviceClass.WINDOW, "Window Status"
    )
