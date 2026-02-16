from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

from .GroupSensor import GroupSensor

class MinHumidity(GroupSensor):

  def __init__(self, hass, device):
    super().__init__(
      hass = hass,
      device = device,
      name = "Min Humidity",
      state_class = SensorStateClass.MEASUREMENT,
      device_class = SensorDeviceClass.HUMIDITY,
      unit_of_measurement = PERCENTAGE,
      sensor_type = "min"
    )

class MinTemperature(GroupSensor):

  def __init__(self, hass, device):
    super().__init__(
      hass,
      device,
      "Min Temperature",
      state_class = SensorStateClass.MEASUREMENT,
      device_class = SensorDeviceClass.TEMPERATURE,
      unit_of_measurement = UnitOfTemperature.FAHRENHEIT,
      sensor_type = "min"
    )
