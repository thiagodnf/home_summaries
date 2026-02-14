import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass)
from homeassistant.const import UnitOfTemperature
from math import log

from ..utils.Entity import get_state_value_as_float
from ..HSSensorEntity import HSSensorEntity

_LOGGER = logging.getLogger(__name__)

FEELS_LIKE = {
  0: {"emoji": "⚪️", "text": "Very Pleasant"},
  1: {"emoji": "🔵", "text": "Pleasant"},
  2: {"emoji": "🟢", "text": "Comfortable"},
  3: {"emoji": "🟡", "text": "Getting Sticky"},
  4: {"emoji": "🟠", "text": "Uncomfortable"},
  5: {"emoji": "🔴", "text": "Very Humid"},
  6: {"emoji": "🟣", "text": "Dangerously Humid"},
}

class DewPoint(HSSensorEntity):

  _attr_device_class = SensorDeviceClass.TEMPERATURE
  _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
  _attr_state_class = SensorStateClass.MEASUREMENT

  def __init__(self, device, tempSensor, humSensor):
    super().__init__(device, "Dew Point")

    self.tempSensor = tempSensor
    self.humSensor = humSensor

  async def async_get_entity_ids(self):
    return [self.tempSensor.entity_id, self.humSensor.entity_id]

  @property
  def extra_state_attributes(self):

    attrs = super().extra_state_attributes or {}

    return {
        **attrs,
        "feels_like": self.get_feels_like("text"),
        "feels_like_as_emoji": self.get_feels_like("emoji"),
    }

  def get_level(self, dp: float):

    if dp is None: return None
    elif dp < 50: return 0
    elif dp < 55: return 1
    elif dp < 60: return 2
    elif dp < 65: return 3
    elif dp < 70: return 4
    elif dp < 75: return 5
    else: return 6

  def get_feels_like(self,info:str = "text"):

    dp = self._attr_native_value

    if not dp:
      return None

    level = self.get_level(dp)

    if level not in FEELS_LIKE:
      return None

    return FEELS_LIKE[level][info]

  def async_calculate_state(self):

    T = get_state_value_as_float(self.hass, self.tempSensor.entity_id)
    H = get_state_value_as_float(self.hass, self.humSensor.entity_id)

    if not T or not H:
      return None

    try:

      T_c = (T - 32.0) * 5.0 / 9.0
      b, c = 17.625, 243.04
      gamma = (b * T_c) / (c + T_c) + log(H / 100.0)
      dew_c = (c * gamma) / (b - gamma)

      return (dew_c * 9.0 / 5.0) + 32.0
    except (ValueError, ZeroDivisionError):
      return None
