from homeassistant.const import PERCENTAGE
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

from .AverageSensorEntity import AverageSensorEntity

class AverageHumidity(AverageSensorEntity):

  _attr_device_class = SensorDeviceClass.HUMIDITY
  _attr_native_unit_of_measurement = PERCENTAGE
  _attr_state_class = SensorStateClass.MEASUREMENT

  def __init__(self, device):
    super().__init__(device, "Average Humidity")
