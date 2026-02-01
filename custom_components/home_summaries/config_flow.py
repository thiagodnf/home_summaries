import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.area_registry import async_get as async_get_area_registry

from .const import DOMAIN, INTEGRATION_NAME

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input = None):

        _LOGGER.info("Hello!!!")

        area_reg = async_get_area_registry(self.hass)
        areas = {area.id: area.name for area in area_reg.async_list_areas()}

        # There is no area available on home assistant. Just show an error message
        if not areas:
            return self.async_abort(reason="no_areas_found")

        options=[{"value": area_id, "label": name} for area_id, name in areas.items()]

        data_schema = {
            vol.Required("areas"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options = options,
                    multiple = True,
                )
            )
        }

        # The user clicked on "Submit"
        if user_input is not None:

            _LOGGER.info("User clicked on Submit with the following input: %s", user_input)

            area_ids = user_input["areas"]

            # The user did not select any area. Just show an error message
            if not area_ids:

                return self.async_show_form(
                    step_id = "user",
                    errors = {"areas": "no_areas_selected"},
                    data_schema = vol.Schema(data_schema)
                )

            # The user selected at least 1 area. Let them proceed
            entries = [
                {"id": area_id, "name": areas.get(area_id, "Unknown Area")} for area_id in area_ids
            ]

            return self.async_create_entry(
                title = INTEGRATION_NAME,
                data = {
                    "areas": entries
                }
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))
