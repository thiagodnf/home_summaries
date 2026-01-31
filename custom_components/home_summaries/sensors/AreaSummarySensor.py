import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as get_device_registry
from homeassistant.helpers.entity_registry import async_get as get_entity_registry
from homeassistant.helpers.entity_registry import EVENT_ENTITY_REGISTRY_UPDATED
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

class AreaSummarySensor():
    
    def __init__(self, hass: HomeAssistant, device,  name):
        
        name = f"{device.name} {name}"
        
        self._hass = hass
        self._area_id = device.area_id
        self._device = device
        self._attr_name = name
        self._attr_unique_id = name.lower().replace(" ", "_")
        self._state = None
        self._member_entity_ids = []
        
        # Get all the registries
        self.device_registry = get_device_registry(hass)
        self.entity_registry = get_entity_registry(hass)
    
    def get_state_value(self, entity_id: str):
        
        state_object = self._hass.states.get(entity_id)
        
        return state_object.state if state_object else None
    
    async def get_member_entity_ids(self) -> list[str]:
        
        member_entity_ids = []
        
        for entity in self._hass.states.async_all("sensor"):
            
            entity_id = entity.entity_id
            device_class = entity.attributes.get("device_class")
            
            if entity_id == self.entity_id:
                continue
            
            if device_class != self._attr_device_class:
                continue
            
            entry = self.entity_registry.async_get(entity_id)
            
            if not entry.labels:
                continue
            
            if "summary" not in entry.labels:
                continue
            
            sensor_area_id = self.get_area_id(entity_id)
            
            if sensor_area_id == self._area_id:
                member_entity_ids.append(entity_id)
            
        return member_entity_ids
    
    def get_area_id(self, entity_id: str) -> str | None:
        
        # 2. Look up the entity entry
        entry = self.entity_registry.async_get(entity_id)
        
        if not entry:
            raise ValueError(f"Entity {entity_id} not found in registry")

        # 3. Check for area_id on the entity itself
        if entry.area_id:
            return entry.area_id
            
        # 4. If not on entity, check the device it belongs to
        if entry.device_id:
            
            device = self.device_registry.async_get(entry.device_id)
            
            if device and device.area_id:
                return device.area_id

        # 5. Return None because the sensor does not have any area_id associated to
        return None
    
    @property
    def extra_state_attributes(self):
        """These show up in the 'More Info' dialog."""
        return {
            "entity_id": self._member_entity_ids,
        }
        
    @property
    def device_info(self):
        """Associate this entity with a device in the device registry."""
        return {
            "identifiers": self._device.identifiers,
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model
        }
    
    async def async_refresh_sensor(self):
        
        _LOGGER.info("Refreshing group and state for %s", self.entity_id)
        
        self._member_entity_ids = await self.get_member_entity_ids()
        
        await self.async_update_group_state()
         
    async def async_set_disable(self, state=False):
        
        entry = self.entity_registry.async_get(self.entity_id)
        
        if not entry:
            return

        if state and entry.disabled_by is None:
            self.entity_registry.async_update_entity(
                self.entity_id,
                disabled_by=RegistryEntryDisabler.INTEGRATION,
            )
    
        # Enable only once
        if not state and entry.disabled_by == RegistryEntryDisabler.INTEGRATION:
            self.entity_registry.async_update_entity(
                self.entity_id,
                disabled_by=None,
            )
            
    async def async_added_to_hass(self):
        """
        Run when the entity is added to Home Assistant.
        """
        
        await self.async_refresh_sensor()
        
        # 1. Define the callback for when any member changes
        async def _async_on_state_change(event):
            await self.async_update_group_state()

        # 2. Metadata Change Listener (for Area/Name changes)
        async def _handle_registry_update(event):
            
            action = event.data.get("action")
            entity_id = event.data.get("entity_id")
            changes = event.data.get("changes", {})
            
            # Trigger refresh if an entity is added/removed from the registry
            if action in ("create", "remove"):
                _LOGGER.info("Created/Removed %s", entity_id)
                await self.async_refresh_sensor()
                return
    
            # If a device is moved or updated, we might need to refresh our list
            if action == "update":
                if "labels" in changes or "area_id" in changes:
                    _LOGGER.info("Labels/Area updated for %s", entity_id)
                    await self.async_refresh_sensor()
        
        # 2. Start listening to the member entities
        self.async_on_remove(
            self._hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, _handle_registry_update)
        )
        
        self.async_on_remove(
            async_track_state_change_event(
                self._hass, self._member_entity_ids, _async_on_state_change
            )
        )
        
    async def async_update_group_state(self):
        pass