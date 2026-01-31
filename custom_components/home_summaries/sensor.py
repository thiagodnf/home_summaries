import logging

from homeassistant.helpers.device_registry import async_get as get_device_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN, MANUFACTURER, INTEGRATION_NAME

from .sensors.AverageHumiditySensor import AverageHumiditySensor
from .sensors.AverageTemperatureSensor import AverageTemperatureSensor
        
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    
    device_registry = get_device_registry(hass)
    
    areas = entry.data.get("areas")
    
    for area in areas:
        
        area_id = area["id"]
        area_name = area.get("name")

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, area_id)},
            name=f"{area_name} Summary Sensor",
            manufacturer=MANUFACTURER,
            model=INTEGRATION_NAME
        )
        
        # Assign area separately (Just a pre selection. The user can change it later)
        device_registry.async_update_device(
            device.id,
            area_id=area_id
        )
        
        # Create sensors
        sensors = [
            AverageTemperatureSensor(hass, device),
            AverageHumiditySensor(hass, device)
        ]
    
        async_add_entities(sensors, update_before_add=True)

    _LOGGER.info("Setup complete for %s", device.name)