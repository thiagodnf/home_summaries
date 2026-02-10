import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.util import slugify
from math import log

from ..utils.Entity import get_state_value

_LOGGER = logging.getLogger(__name__)

class DewPoint(SensorEntity):

  _attr_device_class = SensorDeviceClass.TEMPERATURE
  _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
  _attr_state_class = SensorStateClass.MEASUREMENT

  def __init__(self, hass, device, tempSensor, humSensor):

    self.tempSensor = tempSensor
    self.humSensor = humSensor

    self._hass = hass
    self._attr_name = f"{device.name} Dew Point"
    self._attr_unique_id = slugify(self._attr_name)

    self._device = device

    self._feels_like = {
      0: {"emoji": "⚪️", "description": "Very Pleasant"},
      1: {"emoji": "🔵", "description": "Pleasant"},
      2: {"emoji": "🟢", "description": "Comfortable"},
      3: {"emoji": "🟡", "description": "Getting Sticky"},
      4: {"emoji": "🟠", "description": "Uncomfortable"},
      5: {"emoji": "🔴", "description": "Very Humid"},
      6: {"emoji": "🟣", "description": "Dangerously Humid"},
    }

  @property
  def device_info(self):
    """Associate this entity with a device in the device registry."""
    return {
      "identifiers": self._device.identifiers,
      "name": self._device.name,
      "manufacturer": self._device.manufacturer,
      "model": self._device.model
    }

  @property
  def extra_state_attributes(self):
    return {
      "feels_like": self.get_feels_like(),
      "feels_like_as_emoji": self.get_feels_like_as_emoji()
    }

  @property
  def native_value(self):
    """Calculate the dew point on the fly."""
    T = get_state_value(self._hass, self.tempSensor.entity_id)
    H = get_state_value(self._hass, self.humSensor.entity_id)

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

  async def async_added_to_hass(self):
    """Register listeners to trigger updates."""
    self.async_on_remove(
      async_track_state_change_event(
        self._hass,[
          self.tempSensor.entity_id,
          self.humSensor.entity_id
        ],self._update_callback
      )
    )

  async def _update_callback(self, event):
    self.async_write_ha_state()

  def get_level(self):

    dp = get_state_value(self._hass, self.entity_id)

    if dp is None:
      return None
    elif dp < 50:
      return 0
    elif dp < 55:
      return 1
    elif dp < 60:
      return 2
    elif dp < 65:
      return 3
    elif dp < 70:
      return 4
    elif dp < 75:
      return 5
    else:
      return 6

  def get_feels_like(self):

    level = self.get_level()

    if level not in self._feels_like:
      return None

    return self._feels_like[level]["description"]

  def get_feels_like_as_emoji(self):

    level = self.get_level()

    if level not in self._feels_like:
      return None

    return self._feels_like[level]["emoji"]
