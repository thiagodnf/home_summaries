import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

  _LOGGER.debug("Setting up entry %s", entry)

  # Forward the setup to the sensor platform
  await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor"])

  return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):

  _LOGGER.debug("Unloading entry %s", entry)

  return await hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor"])
