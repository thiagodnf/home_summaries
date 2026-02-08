import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.group.binary_sensor import BinarySensorGroup

from ..utils.Entity import filter_entities_by

_LOGGER = logging.getLogger(__name__)

class MotionStatus(BinarySensorGroup):

  def __init__(self, hass, device, entities: list):

    name = f"{device.name} Motion Status"
    entity_ids = filter_entities_by(hass, entities, BinarySensorDeviceClass.MOTION)

    super().__init__(
        entity_ids = entity_ids,
        device_class = BinarySensorDeviceClass.MOTION,
        name = name,
        mode = False,
        unique_id = name.lower().replace(" ", "_")
    )

    self._device = device

    _LOGGER.debug("Setup complete for %s", self._attr_name)

  @property
  def device_info(self):
    """Associate this entity with a device in the device registry."""
    return {
        "identifiers": self._device.identifiers,
        "name": self._device.name,
        "manufacturer": self._device.manufacturer,
        "model": self._device.model
    }
