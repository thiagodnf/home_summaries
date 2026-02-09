import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .core.utils.Device import get_or_create_device
from .core.utils.Entity import get_entities_by_area_id_and_label_id

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

    entries = get_entities_by_area_id_and_label_id(hass, area_id, label_id)

    humSensor = AverageHumidity(hass, device, entries)
    tempSensor = AverageTemperature(hass, device, entries)

    sensors.append(humSensor)
    sensors.append(tempSensor)
    sensors.append(DewPoint(hass, device, tempSensor, humSensor))

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for all sensors")
