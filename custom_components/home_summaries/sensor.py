import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .utils.Device import get_or_create_device

from .entities.sensors.DewPoint import DewPoint
from .entities.sensors.MaxSensor import MaxHumidity, MaxTemperature
from .entities.sensors.MinSensor import MinHumidity, MinTemperature
from .entities.sensors.AverageSensor import AverageHumidity, AverageTemperature

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    device = get_or_create_device(hass, entry, area_id)

    sensors += await set_up_area_id(hass, device)

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all [sensor] entities")

async def set_up_area_id(hass: HomeAssistant, device) -> list:

  _LOGGER.info("Setting up %s", device.area_id)

  sensors = []

  humidSensor = AverageHumidity(hass, device)
  sensors.append(humidSensor)

  tempSensor = AverageTemperature(hass, device)
  sensors.append(tempSensor)

  dewPointSensor = DewPoint(device, tempSensor, humidSensor)
  sensors.append(dewPointSensor)

  sensors.append(MaxHumidity(hass, device))
  sensors.append(MaxTemperature(hass, device))
  sensors.append(MinHumidity(hass, device))
  sensors.append(MinTemperature(hass, device))

  return sensors
