from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as get_device_registry
from homeassistant.helpers import entity_registry as er
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

def get_device_class(hass: HomeAssistant, entry):

    # Check for device_class on the entity itself
    if entry.device_class:
        return entry.device_class

    state = hass.states.get(entry.entity_id)

    if state:
      return state.attributes.get("device_class")

    # Return None because the sensor does not
    # have any device_class associated to
    return None

def get_area_id(hass: HomeAssistant, entry) -> str | None:

  # Check for area_id on the entity itself
  if entry.area_id:
    return entry.area_id

  # If not on entity, check the device it belongs to
  if entry.device_id:

    device_registry = get_device_registry(hass)
    device = device_registry.async_get(entry.device_id)

    if device and device.area_id:
        return device.area_id

  # Return None because the sensor does not
  # have any area_id associated to
  return None

def get_entities_by_area_id_and_label_id(hass: HomeAssistant, area_id: str, label_id: str):

  ent_reg = er.async_get(hass)

  return [
    entry
    for entry in er.async_entries_for_label(ent_reg, label_id)
    if get_area_id(hass, entry) == area_id
  ]

def filter_entities_by(hass: HomeAssistant, entries: list, device_class: BinarySensorDeviceClass):

  return [
    entry.entity_id
    for entry in entries
    if get_device_class(hass, entry) == device_class
  ]
