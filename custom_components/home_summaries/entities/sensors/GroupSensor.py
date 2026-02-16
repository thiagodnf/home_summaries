import logging

from homeassistant.util import slugify
from homeassistant.components.group.sensor import SensorGroup
from homeassistant.const import EVENT_HOMEASSISTANT_START
from homeassistant.helpers.event import async_track_state_change_event

from ...utils.Entity import get_entity_ids

_LOGGER = logging.getLogger(__name__)

class GroupSensor(SensorGroup):

  def __init__(self, hass, device, name, device_class, state_class, unit_of_measurement, sensor_type):

    name = f"{device.name} {name}"

    super().__init__(
      hass = hass,
      entity_ids = [],
      name = name,
      sensor_type = sensor_type,
      device_class = device_class,
      state_class = state_class,
      unit_of_measurement = unit_of_measurement,
      ignore_non_numeric = True,
      unique_id = slugify(name)
    )

    self._device = device

    _LOGGER.debug("Setup complete for %s", self._attr_name)

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

    await super().async_added_to_hass()

    if self.hass.is_running:
        # The user just used the reload custom integration
        await self._setup_entity_ids()
    else:
        # Home Assistant just started
        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self._setup_entity_ids)

  async def _setup_entity_ids(self, _event=None):
    """The actual logic to find entities and start listeners."""

    self._entity_ids = await self.async_get_entity_ids()

    if self._entity_ids:
      # Start tracking state changes now that we have the IDs
      self.async_on_remove(
          async_track_state_change_event(self.hass, self._entity_ids, self.async_on_state_change)
      )
      # Trigger an immediate initial calculation
      await self.async_on_state_change()

  async def async_on_state_change(self, event = None):
    """Handle child state changes."""
    self.async_update_group_state()
    self.async_write_ha_state()

  async def async_get_entity_ids(self):
    return get_entity_ids(self.hass, self._device.area_id, self._attr_device_class )
