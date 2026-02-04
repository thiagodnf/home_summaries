import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.area_registry import async_get as async_get_area_registry

from .const import DOMAIN, INTEGRATION_NAME

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

  async def async_step_user(self, user_input = None):
    """
      This method is called every time the user wants to add this integration.
    """

    # # Check if an instance is already configured
    # if self._async_current_entries():
    #     return self.async_abort(reason="single_instance_allowed")

    return await self.async_step_areas()

  async def async_step_areas(self, user_input = None):

      entries = self.hass.config_entries.async_entries("home_summaries")

      used_area_ids = set()

      for entry in entries:
        used_area_ids.update(area['id'] for area in entry.data["areas"])

      area_reg = async_get_area_registry(self.hass)
      areas = {area.id: area.name for area in area_reg.async_list_areas()}

      available_areas = {id: name for id, name in areas.items() if id not in used_area_ids}

      # There is no area available on home assistant. Just show an error message
      if not areas:
          return self.async_abort(reason="no_areas_found")

      data_schema = {
        vol.Required("areas"): selector.SelectSelector(
          selector.SelectSelectorConfig(
            options = [{"value": area_id, "label": name} for area_id, name in available_areas.items()],
            multiple = True,
          )
        ),
        # vol.Required("areas"): selector.AreaSelector(
        #     selector.AreaSelectorConfig(
        #       multiple=True
        #     )
        # )
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
          # return await self.async_step_label()

      return self.async_show_form(step_id="areas", data_schema=vol.Schema(data_schema))

  async def async_step_label(self, user_input = None):

    print(user_input)

    data_schema = {
      vol.Required("label"): selector.LabelSelector(
        selector.LabelSelectorConfig(
          multiple=False
        )
      )
    }

    # The user clicked on "Submit"
    if user_input is not None:

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

    return self.async_show_form(step_id="label", data_schema=vol.Schema(data_schema))
