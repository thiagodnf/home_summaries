import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .core.utils.Device import get_or_create_device

from .core.sensors.AverageHumidity import AverageHumidity
from .core.sensors.AverageTemperature import AverageTemperature
from .core.sensors.DewPoint import DewPoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(device)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [sensor] entities")

async def set_up_area_id(device) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  sensors = []

  # if humid_entity_ids:
  humidSensor = AverageHumidity(device)
  sensors.append(humidSensor)

  # if temp_entity_ids:
  tempSensor = AverageTemperature(device)
  sensors.append(tempSensor)

  # if tempSensor and humidSensor:
  dewPointSensor = DewPoint(device, tempSensor, humidSensor)
  sensors.append(dewPointSensor)

  return sensors
