import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_all_entities_by_label_id, filter_entries_by_area_id, filter_entries_by_device_class
from .core.utils.Area import get_all_target_area_ids

from .core.binary_sensors.DoorStatus import DoorStatus
from .core.binary_sensors.WindowsStatus import WindowsStatus
from .core.binary_sensors.WaterLeak import WaterLeak
from .core.binary_sensors.MotionStatus import MotionStatus

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
  """Set up binary sensors from a config entry."""

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  entries = get_all_entities_by_label_id(hass, label_id)

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(hass, device, entries)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [binary_sensor] entities")

async def set_up_area_id(hass: HomeAssistant, device, entries: list) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  target_area_ids = get_all_target_area_ids(hass, device.area_id)

  target_entries = []

  for target_area_id in target_area_ids:
    target_entries += filter_entries_by_area_id(hass, entries, target_area_id)

  onlyDoorSensors = filter_entries_by_device_class(hass, target_entries, BinarySensorDeviceClass.DOOR)
  onlyWindowSensors = filter_entries_by_device_class(hass, target_entries, BinarySensorDeviceClass.WINDOW)
  onlyMotionSensors = filter_entries_by_device_class(hass, target_entries, BinarySensorDeviceClass.MOTION)
  onlyWaterLeakSensors = filter_entries_by_device_class(hass, target_entries, BinarySensorDeviceClass.MOISTURE)

  door_entity_ids = [entry.entity_id for entry in onlyDoorSensors]
  window_entity_ids = [entry.entity_id for entry in onlyWindowSensors]
  motion_entity_ids = [entry.entity_id for entry in onlyMotionSensors]
  water_leak_entity_ids = [entry.entity_id for entry in onlyWaterLeakSensors]

  sensors = []

  # if door_entity_ids:
  doorStatus = DoorStatus(device)
  sensors.append(doorStatus)

  # if window_entity_ids:
  tempSensor = WindowsStatus(hass, device, window_entity_ids)
  sensors.append(tempSensor)

  # if motion_entity_ids:
  tempSensor = MotionStatus(hass, device, motion_entity_ids)
  sensors.append(tempSensor)

  # if water_leak_entity_ids:
  tempSensor = WaterLeak(hass, device, water_leak_entity_ids)
  sensors.append(tempSensor)

  return sensors
