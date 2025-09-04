from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN

class VirtualSocketConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VirtualSocketOptionsFlowHandler(config_entry)


class VirtualSocketOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for a Virtual Socket Switch."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Fetch all available switch entities to populate dropdown
        entity_registry = er.async_get(self.hass)
        switch_entities = [
            e.entity_id for e in entity_registry.entities.values()
            if e.domain == "switch"
        ]

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "linked_switch",
                    default=self.config_entry.options.get("linked_switch", ""),
                ): vol.In(switch_entities)
            }),
        )

