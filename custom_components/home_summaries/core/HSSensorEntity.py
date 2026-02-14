import logging

from homeassistant.components.group.sensor import SensorEntity
from homeassistant.util import slugify
from homeassistant.const import EVENT_HOMEASSISTANT_START
from homeassistant.helpers.event import async_track_state_change_event

from .utils.Entity import get_entity_ids

_LOGGER = logging.getLogger(__name__)

class HSSensorEntity(SensorEntity):

  def __init__(self, device, name):
    self._device = device
    self._entity_ids = []
    self._attr_name = f"{device.name} {name}"
    self._attr_unique_id = slugify(self._attr_name)
    self._attr_native_value = None

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

    self._entity_ids = get_entity_ids(self.hass, self._device.area_id, self._attr_device_class)

    # _LOGGER.info("Found entities after boot: %s", self._entity_ids)

    if self._entity_ids:
      # Start tracking state changes now that we have the IDs
      self.async_on_remove(
          async_track_state_change_event(self.hass, self._entity_ids, self.async_on_state_change)
      )
      # Trigger an immediate initial calculation
      await self.async_on_state_change()

  async def async_on_state_change(self, event = None):
    """Handle child state changes."""
    self._attr_native_value = self.async_calculate_state()
    self.async_write_ha_state()

  def async_calculate_state(self):
    """Must be implemented by subclass."""
    pass
