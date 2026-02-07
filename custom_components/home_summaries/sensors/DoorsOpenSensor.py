from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .BinaryGroupSensor import BinaryGroupSensor

class DoorsOpenSensor(BinaryGroupSensor):

  def __init__(self, hass, device, label_id):
    super().__init__(
      hass,
      device,
      label_id,
      BinarySensorDeviceClass.DOOR,
      "Doors Opened",
      False
    )
