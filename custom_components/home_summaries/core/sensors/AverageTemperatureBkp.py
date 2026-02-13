import logging

from homeassistant.components.group.sensor import SensorGroup
from homeassistant.util import slugify
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EVENT_HOMEASSISTANT_START, STATE_UNKNOWN, STATE_UNAVAILABLE

from ..utils.Device import get_or_create_device
from ..utils.Entity import get_all_entities_by_label_id, filter_entries_by_area_id, filter_entries_by_device_class
from ..utils.Area import get_all_target_area_ids


_LOGGER = logging.getLogger(__name__)

class AverageTemperature(SensorGroup):

  def __init__(self, hass, device, entity_ids: list):

    self._device = device
    self._entity_ids = entity_ids
    name = f"{device.name} Average Temperature"

    # We call super() but we do NOT pass hass here.
    # The base SensorGroup will handle hass once added to the system.
    super().__init__(
      hass = hass,
      entity_ids=entity_ids,
      name=name,
      sensor_type="mean",
      unique_id=slugify(name),
      ignore_non_numeric=True,
      unit_of_measurement=None,
      state_class=None,
      device_class=SensorDeviceClass.TEMPERATURE,
    )
  # def __init__(self, hass, device, entity_ids: list):

  #   name = f"{device.name} Average Temperature"

  #   """Initialize using the parent Group constructor."""
  #   super().__init__(
  #       hass = hass,
  #       entity_ids = entity_ids,
  #       name = name,
  #       sensor_type = "mean",
  #       unique_id = slugify(name),
  #       ignore_non_numeric=True,
  #       unit_of_measurement=None,
  #       state_class=None,
  #       device_class=SensorDeviceClass.TEMPERATURE,
  #   )

  #   self._device = device

  #   _LOGGER.debug("Setup complete for %s", self._attr_name)

  @property
  def device_info(self):
    """Associate this entity with a device in the device registry."""
    return {
        "identifiers": self._device.identifiers,
        "name": self._device.name,
        "manufacturer": self._device.manufacturer,
        "model": self._device.model
    }

  async def async_added_to_hass(self) -> None:
    """Run when entity about to be added to hass."""
    await super().async_added_to_hass()

    # This solves the "Unavailable on Restart" problem.
    # We force a state calculation 5 seconds after startup
    # or immediately if the system is already running.
    if self.hass.is_running:
        self.async_schedule_update_ha_state(True)
    else:
        self.hass.bus.async_listen_once("homeassistant_start",self._update_after_boot)

  async def _update_after_boot(self, _):
    """Force an update once HASS has finished starting up."""
    _LOGGER.debug("HASS started, refreshing group sensor: %s", self.name)
    self.async_schedule_update_ha_state(True)

  # async def async_added_to_hass(self) -> None:
  #   """Handle entity which is about to be added to Home Assistant."""
  #   await super().async_added_to_hass()

  #   # This is where we ensure the group updates once the system is ready.
  #   _LOGGER.debug("Entity %s added to HASS, members: %s", self.entity_id, self._entity_ids)
  #   self.async_schedule_update_ha_state(True)

  # async def _update_at_start(self, _):
  #   """Force an update once HASS has fully started."""
  #   self.async_schedule_update_ha_state(True)

  # async def async_added_to_hass(self):
  #   """Run when entity about to be added to hass."""
  #   await super().async_added_to_hass()

  #   self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self._update_at_start)

    # entries = get_all_entities_by_label_id(self.hass, "summary")

    # entries = filter_entries_by_area_id(self.hass, entries, self._device.area_id)

    # entries = filter_entries_by_device_class(self.hass, entries, SensorDeviceClass.TEMPERATURE)

    # self._entity_ids = [a.entity_id for a in entries]

    # self.async_schedule_update_ha_state(True)
    # _LOGGER.debug("entries %s", [a.entity_id for a in entries])
