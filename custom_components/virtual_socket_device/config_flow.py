# config_flow.py
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
import voluptuous as vol

class VirtualSocketConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Virtual Socket Device."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("switch_name"): str
                }),
            )

        return self.async_create_entry(
            title=user_input["switch_name"],
            data=user_input
        )

