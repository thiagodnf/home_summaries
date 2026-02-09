import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_entities_by_area_id_and_label_id
from .core.utils.Entity import filter_entities_by

from .core.binary_sensors.DoorStatus import DoorStatus
from .core.binary_sensors.WindowsStatus import WindowsStatus
from .core.binary_sensors.WaterLeak import WaterLeak
from .core.binary_sensors.MotionStatus import MotionStatus

_LOGGER = logging.getLogger(__name__)

SENSOR_MAP = {
    BinarySensorDeviceClass.DOOR: DoorStatus,
    BinarySensorDeviceClass.WINDOW: WindowsStatus,
    BinarySensorDeviceClass.MOISTURE: WaterLeak,
    BinarySensorDeviceClass.MOTION: MotionStatus,
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
  """Set up binary sensors from a config entry."""

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    entries = get_entities_by_area_id_and_label_id(hass, area_id, label_id)

    for device_class, cls in SENSOR_MAP.items():
        entity_ids = filter_entities_by(hass, entries, device_class)
        if entity_ids:
            sensors.append(cls(hass, device, entity_ids))

    # door_entity_ids = filter_entities_by(hass, entries, BinarySensorDeviceClass.DOOR)
    # windows_entity_ids = filter_entities_by(hass, entries, BinarySensorDeviceClass.WINDOW)
    # water_leak_entity_ids = filter_entities_by(hass, entries, BinarySensorDeviceClass.MOISTURE)
    # motion_entity_ids = filter_entities_by(hass, entries, BinarySensorDeviceClass.MOTION)

    # if door_entity_ids:
    #   sensors.append(DoorStatus(hass, device, door_entity_ids))
    # if windows_entity_ids:
    #   sensors.append(WindowsStatus(hass, device, windows_entity_ids))
    # if water_leak_entity_ids:
    #   sensors.append(WaterLeak(hass, device, water_leak_entity_ids))
    # if motion_entity_ids:
    #   sensors.append(MotionStatus(hass, device, motion_entity_ids))

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all binary sensors")

# def
