import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_entities_by_area_id_and_label_id

from .core.binary_sensors.DoorStatus import DoorStatus
from .core.binary_sensors.WindowsStatus import WindowsStatus
from .core.binary_sensors.WaterLeak import WaterLeak

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
  """Set up binary sensors from a config entry."""

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    entries = get_entities_by_area_id_and_label_id(hass, area_id, label_id)

    sensors.append(DoorStatus(hass, device, entries))
    sensors.append(WindowsStatus(hass, device, entries))
    sensors.append(WaterLeak(hass, device, entries))

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all binary sensors")
