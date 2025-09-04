import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow for enabling the integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step initiated by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            # Use an empty schema correctly
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
            )

        return self.async_create_entry(title="Example Integration", data={})

