import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.area_registry import async_get as get_area_registry

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_entities_by_area_id_and_label_id
from .core.utils.Entity import filter_entities_by
from .core.utils.Entity import get_all_entities_by_label_id, filter_entries_by_area_id, filter_entries_by_device_class
from .core.utils.Area import get_all_area_ids, get_all_area_ids_except

from .core.sensors.AverageHumidity import AverageHumidity
from .core.sensors.AverageTemperature import AverageTemperature
from .core.sensors.DewPoint import DewPoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  all_area_ids = get_all_area_ids(hass)
  entries = get_all_entities_by_label_id(hass, label_id)

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(hass, device, entries)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [sensor] entities")

async def set_up_area_id(hass: HomeAssistant, device, ent) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  target_area_ids = [device.area_id]

  if device.area_id == "home":
    target_area_ids = get_all_area_ids_except(hass, ["home"])

  entries = []

  for area_id in target_area_ids:
    entries += filter_entries_by_area_id(hass, ent, area_id)

  return await set_up_sensors(hass, device, entries)

async def set_up_sensors(hass: HomeAssistant, device, entries) -> list:

  onlyHumidSensors = filter_entries_by_device_class(hass, entries, SensorDeviceClass.HUMIDITY)
  onlyTempSensors = filter_entries_by_device_class(hass, entries, SensorDeviceClass.TEMPERATURE)

  humidity_entity_ids = [entry.entity_id for entry in onlyHumidSensors]
  temperature_entity_ids = [entry.entity_id for entry in onlyTempSensors]

  sensors = []
  humidSensor = None
  tempSensor = None

  if humidity_entity_ids:
    humidSensor = AverageHumidity(hass, device, humidity_entity_ids)
    sensors.append(humidSensor)

  if temperature_entity_ids:
    tempSensor = AverageTemperature(hass, device, temperature_entity_ids)
    sensors.append(tempSensor)

  if tempSensor and humidSensor:
    dewPointSensor = DewPoint(hass, device, tempSensor, humidSensor)
    sensors.append(dewPointSensor)

  return sensors
