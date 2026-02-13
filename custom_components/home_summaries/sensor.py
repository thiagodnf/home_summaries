import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorDeviceClass

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_all_entities_by_label_id, filter_entries_by_area_id, filter_entries_by_device_class
from .core.utils.Area import get_all_target_area_ids

from .core.sensors.AverageHumidity import AverageHumidity
from .core.sensors.AverageTemperature import AverageTemperature
from .core.sensors.DewPoint import DewPoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  entries = get_all_entities_by_label_id(hass, label_id)

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(hass, device, entries)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [sensor] entities")

async def set_up_area_id(hass: HomeAssistant, device, entries: list) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  target_area_ids = get_all_target_area_ids(hass, device.area_id)

  target_entries = []

  for target_area_id in target_area_ids:
    target_entries += filter_entries_by_area_id(hass, entries, target_area_id)

  onlyHumidSensors = filter_entries_by_device_class(hass, target_entries, SensorDeviceClass.HUMIDITY)
  onlyTempSensors = filter_entries_by_device_class(hass, target_entries, SensorDeviceClass.TEMPERATURE)

  humid_entity_ids = [entry.entity_id for entry in onlyHumidSensors]
  temp_entity_ids = [entry.entity_id for entry in onlyTempSensors]

  sensors = []

  # if humid_entity_ids:
  humidSensor = AverageHumidity(hass, device, humid_entity_ids)
  sensors.append(humidSensor)

  # if temp_entity_ids:
  tempSensor = AverageTemperature(hass, device, temp_entity_ids)
  sensors.append(tempSensor)

  # if tempSensor and humidSensor:
  dewPointSensor = DewPoint(hass, device, tempSensor, humidSensor)
  sensors.append(dewPointSensor)

  return sensors
