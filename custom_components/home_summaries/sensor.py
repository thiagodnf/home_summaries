import logging

from homeassistant.helpers.area_registry import async_get as get_area_registry
from homeassistant.helpers.device_registry import async_get as get_device_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN, MANUFACTURER, INTEGRATION_NAME

from .sensors.AverageHumiditySensor import AverageHumiditySensor
from .sensors.AverageTemperatureSensor import AverageTemperatureSensor
from .sensors.DoorsOpenSensor import DoorsOpenSensor

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:

  area_registry = get_area_registry(hass)
  device_registry = get_device_registry(hass)

  area_ids = entry.data.get("area_ids")
  label_id = entry.data.get("label_id")

  sensors = []

  for area_id in area_ids:

    area = area_registry.async_get_area(area_id)

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, area_id)},
        name=f"{area.name} Summary Sensor",
        manufacturer=MANUFACTURER,
        model=INTEGRATION_NAME
    )

    # Assign area separately (Just a pre selection. The user can change it later)
    device_registry.async_update_device(device.id, area_id=area_id)

    # Create sensors
    sensors.append(AverageTemperatureSensor(hass, device, label_id))
    sensors.append(AverageHumiditySensor(hass, device, label_id))
    sensors.append(DoorsOpenSensor(hass, device, label_id))

  async_add_entities(sensors, update_before_add=True)

  _LOGGER.info("Setup complete for %s", device.name)
