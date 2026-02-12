from homeassistant.core import HomeAssistant
from homeassistant.helpers.area_registry import async_get as get_area_registry

def get_all_area_ids(hass: HomeAssistant) -> list:
  area_reg = get_area_registry(hass)
  return [area.id for area in area_reg.async_list_areas()]

def get_all_area_ids_except(hass: HomeAssistant, excludes: list[str]):
  return [area_id for area_id in get_all_area_ids(hass) if area_id not in excludes]
