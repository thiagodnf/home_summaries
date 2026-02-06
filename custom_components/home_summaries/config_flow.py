import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.label_registry import async_get as get_label_registry

from .const import DOMAIN, INTEGRATION_NAME

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

  async def async_step_user(self, user_input=None):
    """Called every time the user wants to add this integration"""

    if self._async_current_entries():
      return self.async_abort(reason="only_single_integration_allowed")

    await self.async_create_summary_label_if_not_exists()

    data_schema = vol.Schema({
      vol.Required("area_ids"): selector.AreaSelector({"multiple": True}),
      vol.Required("label_id"): selector.LabelSelector({"multiple": False})
    })

    errors = {}

    # The user clicked on "Submit"
    if user_input is not None:

      if not user_input.get("area_ids"):
        errors["area_ids"] = "at_least_one_area_required"

      if not user_input.get("label_id"):
        errors["label_id"] = "at_least_one_label_required"

      if not errors:

        _LOGGER.debug("User created entry with: %s", user_input)

        return self.async_create_entry(title = INTEGRATION_NAME, data = user_input)

    return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

  async def async_create_summary_label_if_not_exists(self):

    label_reg = get_label_registry(self.hass)
    label = label_reg.async_get_label_by_name("Summary")

    if label is None:

      label = label_reg.async_create(
          name="Summary",
          icon="mdi:text-box-outline",
          color="#bd93f9",
          description="Use this label to include the sensor in Home Summaries"
      )
