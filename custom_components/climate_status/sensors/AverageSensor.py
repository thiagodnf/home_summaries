import logging

from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.entity import EntityCategory

from .AreaSummarySensor import AreaSummarySensor
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class AverageSensor(AreaSummarySensor):
    
    def __init__(self, hass, device, name):
        AreaSummarySensor.__init__(self, hass, device, name)
    
    async def fix_issue(self, error_key):
        
        ir.async_delete_issue(self.hass, DOMAIN, f"{self._attr_unique_id}${error_key}")
        
    async def create_issue(self, error_key, error_data):
        
        ir.async_create_issue(
            self._hass,
            DOMAIN,
            f"{self._attr_unique_id}${error_key}",
            is_fixable=False,
            severity=ir.IssueSeverity.WARNING,
            translation_key=error_key,
            translation_placeholders=error_data,
        )
        
    # async def async_update(self):
    async def async_update_group_state(self):
        
        # entry = self.entity_registry.async_get(self.entity_id)
        
        # _LOGGER.info("entry.disabled_by: %s", entry.disabled_by)
        
        # if entry and entry.disabled_by is not None:
        #     return
    
        values = []
        errors = []
    
        for entity_id in self._member_entity_ids:
           
            state_value = self.get_state_value(entity_id)
            
            if state_value is None:
                errors.append(entity_id)
                continue
            
            if state_value in ("unknown", "unavailable"):
                errors.append(entity_id)
                continue
            
            try:
                values.append(float(state_value))
            except (ValueError, TypeError):
                errors.append(entity_id)
        
        _LOGGER.info("Updating Group Values: %s", values)
        
        error_data = {
            "name": self._attr_name,
            "entity_ids": "\n- " + "\n- ".join(errors)
        }
        
        if errors:
            
            self._attr_available = False
            self._attr_native_value = None    
            
            await self.create_issue("group_has_invalid_state", error_data)
                
        else:
            
            await self.fix_issue("group_has_invalid_state")
            
            if values:
                self._attr_available = True
                self._attr_native_value = sum(values) / len(values)
                # await self.async_set_disable(False)
            else:
                self._attr_available = False
                self._attr_native_value = None
                # await self.async_set_disable(True)
    
        # Safety check: Only write state if we are actually 'live' in HA
        if self._hass and self.entity_id:
            self.async_write_ha_state()