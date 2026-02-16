from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as get_device_registry
from homeassistant.helpers.area_registry import async_get as get_area_registry

from ..const import DOMAIN, MANUFACTURER, INTEGRATION_NAME

def get_or_create_device(hass: HomeAssistant, entry: ConfigEntry, area_id: str):

  area_registry = get_area_registry(hass)
  device_registry = get_device_registry(hass)

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

  return device
