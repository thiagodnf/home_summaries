import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.area_registry import async_get as async_get_area_registry
from homeassistant.helpers import label_registry as lr

from .const import DOMAIN, INTEGRATION_NAME

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

  async def async_step_user(self, user_input=None):
    """Called every time the user wants to add this integration"""

    await self.async_create_summary_label_if_not_exists()

    entries = self.hass.config_entries.async_entries("home_summaries")

    area_reg = async_get_area_registry(self.hass)
    areas = {area.id: area.name for area in area_reg.async_list_areas()}

    # Show error if there is no area available
    if not areas:
        return self.async_abort(reason="no_areas_found")

    data_schema = {
      vol.Required("areas"): selector.AreaSelector({"multiple": True}),
      vol.Required("label"): selector.LabelSelector({"multiple": False})
    }

    # The user clicked on "Submit"
    if user_input is not None:

        _LOGGER.info("User clicked on Submit with the following input: %s", user_input)

        area_ids = user_input["areas"]
        label_id = user_input["label"]

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
                "areas": entries,
                "label_id": label_id
            }
        )

    return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))

  async def async_create_summary_label_if_not_exists(self):

    label_reg = lr.async_get(self.hass)
    label = label_reg.async_get_label_by_name("Summary")

    if label is None:

      label = label_reg.async_create(
          name="Summary",
          icon="mdi:text-box-outline",
          color="#bd93f9",
          description="Use this label to include the sensor in Home Summaries"
      )
