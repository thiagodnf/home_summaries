import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.util import slugify
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





  # def __init__(self, hass, device, tempSensor, humSensor):

  #   self.tempSensor = tempSensor
  #   self.humSensor = humSensor

  #   self._hass = hass
  #   self._attr_name = f"{device.name} Dew Point"
  #   self._attr_unique_id = slugify(self._attr_name)

  #   self._device = device

  #   self.FEELS_LIKE = {
  #     0: {"emoji": "⚪️", "description": "Very Pleasant"},
  #     1: {"emoji": "🔵", "description": "Pleasant"},
  #     2: {"emoji": "🟢", "description": "Comfortable"},
  #     3: {"emoji": "🟡", "description": "Getting Sticky"},
  #     4: {"emoji": "🟠", "description": "Uncomfortable"},
  #     5: {"emoji": "🔴", "description": "Very Humid"},
  #     6: {"emoji": "🟣", "description": "Dangerously Humid"},
  #   }

  #   self._feels_like = None
  #   self._feels_like_emoji = None

  #   _LOGGER.debug("Setup complete for %s", self._attr_name)

  # @property
  # def device_info(self):
  #   """Associate this entity with a device in the device registry."""
  #   return {
  #     "identifiers": self._device.identifiers,
  #     "name": self._device.name,
  #     "manufacturer": self._device.manufacturer,
  #     "model": self._device.model
  #   }

  # async def async_update(self):

  #   dewPoint = self._calculate_dew_point()

  #   self._attr_native_value = dewPoint
  #   self._feels_like = self.get_feels_like(dewPoint, "description")
  #   self._feels_like_emoji = self.get_feels_like(dewPoint, "emoji")

  # @property
  # def extra_state_attributes(self):

  #   return {
  #     "feels_like": self._feels_like,
  #     "feels_like_as_emoji": self._feels_like_emoji
  #   }

  # def _calculate_dew_point(self):
  #   """Calculate the dew point on the fly."""

  #   T = get_state_value_as_float(self._hass, self.tempSensor.entity_id)
  #   H = get_state_value_as_float(self._hass, self.humSensor.entity_id)

  #   if not T or not H:
  #     return None

  #   try:

  #     T_c = (T - 32.0) * 5.0 / 9.0
  #     b, c = 17.625, 243.04
  #     gamma = (b * T_c) / (c + T_c) + log(H / 100.0)
  #     dew_c = (c * gamma) / (b - gamma)

  #     return (dew_c * 9.0 / 5.0) + 32.0
  #   except (ValueError, ZeroDivisionError):
  #     return None

  # async def async_added_to_hass(self):
  #   """Register listeners to trigger updates."""
  #   self.async_on_remove(
  #     async_track_state_change_event(
  #       self._hass,[
  #         self.tempSensor.entity_id,
  #         self.humSensor.entity_id
  #       ],self._update_callback
  #     )
  #   )

  # async def _update_callback(self, event):
  #   self.async_schedule_update_ha_state(True)

  # def get_level(self, dp: float):

  #   if dp is None: return None
  #   elif dp < 50: return 0
  #   elif dp < 55: return 1
  #   elif dp < 60: return 2
  #   elif dp < 65: return 3
  #   elif dp < 70: return 4
  #   elif dp < 75: return 5
  #   else: return 6

  # def get_feels_like(self, dp:float, info:str = "description"):

  #   if not dp:
  #     return None

  #   level = self.get_level(dp)

  #   if level not in self.FEELS_LIKE:
  #     return None

  #   return self.FEELS_LIKE[level][info]
