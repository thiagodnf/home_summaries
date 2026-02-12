import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.area_registry import async_get as get_area_registry

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_entities_by_area_id_and_label_id
from .core.utils.Entity import filter_entities_by

from .core.sensors.AverageHumidity import AverageHumidity
from .core.sensors.AverageTemperature import AverageTemperature
from .core.sensors.DewPoint import DewPoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:
    sensors += await set_up_area_id(hass, entry, area_id, label_id)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all sensors")

async def set_up_area_id(hass: HomeAssistant, entry: ConfigEntry, area_id: str, label_id) -> list:

  area_reg = get_area_registry(hass)

  device = get_or_create_device(hass, entry, area_id)

  entries = []

  if area_id == "home":
    for area in area_reg.async_list_areas():
      if area.id != "home":
        entries += get_entities_by_area_id_and_label_id(hass, area.id, label_id)
  else:
    entries = get_entities_by_area_id_and_label_id(hass, area_id, label_id)

  humidity_entity_ids = filter_entities_by(hass, entries, SensorDeviceClass.HUMIDITY)
  temperature_entity_ids = filter_entities_by(hass, entries, SensorDeviceClass.TEMPERATURE)

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

