from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

from .AverageSensorEntity import AverageSensorEntity

class AverageTemperature(AverageSensorEntity):

  _attr_device_class = SensorDeviceClass.TEMPERATURE
  _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
  _attr_state_class = SensorStateClass.MEASUREMENT

  def __init__(self, device):
    super().__init__(device, "Average Temperature")
