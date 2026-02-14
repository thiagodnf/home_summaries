import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .core.utils.Device import get_or_create_device

from .core.binary_sensors.DoorStatus import DoorStatus
from .core.binary_sensors.WindowStatus import WindowStatus
from .core.binary_sensors.MoistureStatus import MoistureStatus
from .core.binary_sensors.MotionStatus import MotionStatus

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
  """Set up binary sensors from a config entry."""

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(device)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [binary_sensor] entities")

async def set_up_area_id(device) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  sensors = []

  sensors.append(DoorStatus(device))
  sensors.append(WindowStatus(device))
  sensors.append(MotionStatus(device))
  sensors.append( MoistureStatus(device))

  return sensors
