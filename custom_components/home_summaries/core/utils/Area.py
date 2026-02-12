from homeassistant.core import HomeAssistant
from homeassistant.helpers.area_registry import async_get as get_area_registry

def get_all_area_ids(hass: HomeAssistant) -> list:
  area_reg = get_area_registry(hass)
  return [area.id for area in area_reg.async_list_areas()]

def get_all_area_ids_except(hass: HomeAssistant, excludes: list[str]) -> list:
  return [area_id for area_id in get_all_area_ids(hass) if area_id not in excludes]

def get_all_target_area_ids(hass: HomeAssistant, area_id: str) -> list:
  """
    If `area_id` is "home", all area _ids except "home" are returned.
    Otherwise, a list containing only the specified `area_id` is returned.
  """
  if area_id == "home":
    return get_all_area_ids_except(hass, ["home"])
  else:
    return [area_id]
