import logging

from homeassistant.components.group.sensor import SensorGroup
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event

from homeassistant.helpers.entity_registry import EVENT_ENTITY_REGISTRY_UPDATED
from homeassistant.helpers.device_registry import async_get as get_device_registry

_LOGGER = logging.getLogger(__name__)

class GroupSensor(SensorGroup):

  def __init__(
      self, hass: HomeAssistant,
      device,
      label_id,
      group_device_class,
      name: str,
      sensor_type
  ):
    """Initialize using the parent Group constructor."""
    super().__init__(
        hass=hass,
        entity_ids=[],
        name=f"{device.name} {name}",
        sensor_type=sensor_type,
        unique_id=f"{device.name} {name}".lower().replace(" ", "_"),
        ignore_non_numeric=True,
        unit_of_measurement=None,
        state_class=None,
        device_class=None,
    )

    self._group_device_class = group_device_class
    self._area_id = device.area_id
    self._device = device

    self.target_label = label_id

  @property
  def device_info(self):
    """Associate this entity with a device in the device registry."""
    return {
        "identifiers": self._device.identifiers,
        "name": self._device.name,
        "manufacturer": self._device.manufacturer,
        "model": self._device.model
    }

  async def async_added_to_hass(self):
    """Handle entity being added to Home Assistant."""
    await super().async_added_to_hass()

    # 1. Initial population of the group
    self._update_member_list()

    # 1. Define the callback for when any member changes
    async def _async_on_state_change(event):
        self._refresh_state()

    # 2. Listen for changes in the Entity Registry (labels, area moves, etc.)
    self.async_on_remove(
        self.hass.bus.async_listen(
            EVENT_ENTITY_REGISTRY_UPDATED, self._handle_registry_update
        )
    )

    self.async_on_remove(
        async_track_state_change_event(
            self.hass, self._entity_ids, _async_on_state_change
        )
    )

  @callback
  async def _handle_registry_update(self, event):
    """Update member list when registry changes."""

    entity_id = event.data.get("entity_id")
    action = event.data.get("action")

    _LOGGER.info("Entity_id %s got changed", event.data)

    ent_reg = er.async_get(self.hass)
    entry = ent_reg.async_get(entity_id)

    isGrouped = self.is_part_of_the_group(entry)

    if isGrouped and entity_id not in self._entity_ids:
      self._entity_ids.append(entity_id)
    elif not isGrouped and entity_id in self._entity_ids:
      self._entity_ids.remove(entity_id)

    _LOGGER.info("isGrouped %s", isGrouped)

    self._refresh_state()

  @callback
  def _update_member_list(self):
    """Find entities matching label and area, then update group."""

    ent_reg = er.async_get(self.hass)

    new_member_ids = []

    # Find all entities with your specific label
    for entry in er.async_entries_for_label(ent_reg, self.target_label):
    # for entry in ent_reg.entities.values():

      isGrouped = self.is_part_of_the_group(entry)

      if isGrouped:
        new_member_ids.append(entry.entity_id)

    # Update the group sensor if the new member
    # list is different from the previous one
    if set(self._entity_ids) != set(new_member_ids):
      self._entity_ids = new_member_ids
      self._refresh_state()

  def _refresh_state(self):
      # 1. Recalculate the mathematical state (mean/sum/etc)
    self.async_update_group_state()

    # 3. Push the update to the UI
    self.async_write_ha_state()

  def get_device_class(self, entry):

    # Check for device_class on the entity itself
    if entry.device_class:
        return entry.device_class

    state = self.hass.states.get(entry.entity_id)

    if state:
      return state.attributes.get("device_class")

    # Return None because the sensor does not
    # have any device_class associated to
    return None

  def get_device_from_registry(self, device_id):
    device_registry = get_device_registry(self.hass)
    return device_registry.async_get(device_id)

  def get_area_id(self, entry) -> str | None:

    # Check for area_id on the entity itself
    if entry.area_id:
      return entry.area_id

    # If not on entity, check the device it belongs to
    if entry.device_id:

      device = self.get_device_from_registry(entry.device_id)

      if device and device.area_id:
          return device.area_id

    # Return None because the sensor does not
    # have any area_id associated to
    return None

  def is_part_of_the_group(self, entry):

    # Ignore if entry does not exist
    if not entry:
      return False

    # Ignore itself to avoid infinite loops
    if entry.entity_id == self.entity_id:
      return False

    # Ignore if the sensor has a different device class
    if self._group_device_class != self.get_device_class(entry):
      return False

    # Ignore if the sensor does not have the target label
    if self.target_label not in entry.labels:
      return False

    # Ignore if the sensor has a different area id
    if self._device.area_id != self.get_area_id(entry):
      return False

    return True
