import logging

from homeassistant.components.group.sensor import SensorGroup, SensorEntity
from homeassistant.util import slugify
from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EVENT_HOMEASSISTANT_START, STATE_UNKNOWN, STATE_UNAVAILABLE
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er, device_registry as dr
from homeassistant.components.sensor import SensorDeviceClass

import statistics

from ..utils.Device import get_or_create_device
from ..utils.Entity import get_all_entities_by_label_id, filter_entries_by_area_id, filter_entries_by_device_class
from ..utils.Area import get_all_target_area_ids


_LOGGER = logging.getLogger(__name__)

class AverageTemperature(SensorEntity):

  def __init__(self, hass, device, entity_ids: list):
    self._hass = hass
    self._device = device
    self._entity_ids = []
    self._attr_name = f"{device.name} Average Temperature"
    self._attr_unique_id = slugify(self._attr_name)
    self._attr_device_class = SensorDeviceClass.TEMPERATURE
    self._attr_state_class = SensorStateClass.MEASUREMENT
    self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT # Or pull from HASS config
    self._attr_native_value = None

  @property
  def device_info(self):
    return {
      "identifiers": self._device.identifiers,
      "name": self._device.name,
      "manufacturer": self._device.manufacturer,
      "model": self._device.model
    }

  @property
  def extra_state_attributes(self):
    return {
      "entity_id": self._entity_ids,
    }

  async def async_added_to_hass(self) -> None:
    """Handle entity which is about to be added to Home Assistant."""

    self._entity_ids = await self.async_get_entities()

    # 1. Listen for ANY change in the member entities
    # This is "reactive"—it works even if the entities appear 5 minutes late.
    self.async_on_remove(
      async_track_state_change_event(
        self.hass, self._entity_ids, self._async_on_state_change
      )
    )

    # 2. Trigger an immediate initial calculation
    self._async_calculate_average()

    _LOGGER.info("called async_added_to_hass %s", self._entity_ids)

  async def async_get_entities(self):

    entries = get_all_entities_by_label_id(self.hass, "summary")

    entries = filter_entries_by_area_id(self.hass, entries, self._device.area_id)
    entries = filter_entries_by_device_class(self.hass, entries, SensorDeviceClass.TEMPERATURE)

    _LOGGER.info("[a.entity_id for a in entries] %s", [a.entity_id for a in entries])

    return [a.entity_id for a in entries]

  async def _async_on_state_change(self, event):
    """Handle child state changes."""
    self._async_calculate_average()
    self.async_write_ha_state()

    _LOGGER.info("called _async_on_state_change %s", self._entity_ids)

  def _async_calculate_average(self):
    """Perform the mean calculation."""
    values = []

    for entity_id in self._entity_ids:
      state = self.hass.states.get(entity_id)
      if state and state.state not in ("unavailable", "unknown"):
        try:
          values.append(float(state.state))
        except (ValueError, TypeError):
          continue

    if not values:
      _LOGGER.info("_attr_native_value %s", self._attr_native_value)
      self._attr_native_value = None
      return

    # Simple mean calculation: $$ \text{mean} = \frac{\sum v_i}{n} $$
    self._attr_native_value = round(statistics.mean(values), 2)

    _LOGGER.info("_attr_native_value %s", self._attr_native_value)
