import logging

from homeassistant.components.group.sensor import SensorGroup
from homeassistant.components.sensor import SensorDeviceClass

from ..utils.Entity import filter_entities_by

_LOGGER = logging.getLogger(__name__)

class AverageHumidity(SensorGroup):

  def __init__(self, hass, device, entity_ids: list):

    name = f"{device.name} Average Humidity"

    """Initialize using the parent Group constructor."""
    super().__init__(
        hass = hass,
        entity_ids = entity_ids,
        name = name,
        sensor_type = "mean",
        unique_id = name.lower().replace(" ", "_"),
        ignore_non_numeric=True,
        unit_of_measurement=None,
        state_class=None,
        device_class=None,
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
