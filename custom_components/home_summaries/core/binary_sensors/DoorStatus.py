import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.group.binary_sensor import BinarySensorGroup

_LOGGER = logging.getLogger(__name__)

from ..GroupBinarySensor import GroupBinarySensor

class DoorStatus(GroupBinarySensor):

  def __init__(self, device):
    super().__init__(
        device, BinarySensorDeviceClass.DOOR, "Door Status"
    )

    _LOGGER.debug("Setup complete for %s", self._attr_name)






  # _attr_device_class = BinarySensorDeviceClass.DOOR

  # def __init__(self, device):
  #   super().__init__(device, "Door Status")

  #   self.mode = all

  #   # if mode:
  #     # self.mode = any

  # def async_calculate_state(self):
  #   """Perform the mean calculation."""

  #   states = [
  #     state.state
  #     for entity_id in self._entity_ids
  #     if (state := self.hass.states.get(entity_id)) is not None
  #   ]

  #   # Set group as unavailable if all members are unavailable or missing
  #   self._attr_available = any(state != STATE_UNAVAILABLE for state in states)

  #   valid_state = self.mode(
  #     state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) for state in states
  #   )
  #   if not valid_state:
  #     # Set as unknown if any / all member is not unknown or unavailable
  #     return None
  #   else:
  #     # Set as ON if any / all member is ON
  #     self._attr_is_on = self.mode(state == STATE_ON for state in states)









# class DoorStatus(BinarySensorGroup):

#   def __init__(self, hass, device, entity_ids: list):

#     name = f"{device.name} Door Status"

#     super().__init__(
#         entity_ids = entity_ids,
#         device_class = BinarySensorDeviceClass.DOOR,
#         name = name,
#         mode = False,
#         unique_id = slugify(name)
#     )

#     self._device = device

#     _LOGGER.debug("Setup complete for %s", self._attr_name)

#   @property
#   def device_info(self):
#     """Associate this entity with a device in the device registry."""
#     return {
#         "identifiers": self._device.identifiers,
#         "name": self._device.name,
#         "manufacturer": self._device.manufacturer,
#         "model": self._device.model
#     }
