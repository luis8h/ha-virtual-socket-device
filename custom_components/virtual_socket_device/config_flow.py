from typing import Any, override
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN

class VirtualSocketConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION: int = 1

    @override
    async def async_step_user(self, user_input: Any = None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["switch_name"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("switch_name"): str,
            }),
        )

    @staticmethod
    @callback
    @override
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return VirtualSocketOptionsFlowHandler(config_entry)


class VirtualSocketOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry: config_entries.ConfigEntry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        # Get all switch entities for the dropdown
        entity_registry = er.async_get(self.hass)
        switch_entities = {
            e.entity_id: e.name or e.entity_id
            for e in entity_registry.entities.values()
            if e.domain == "switch"
        }

        # Ensure virtual switch cannot link to itself
        current_entity_id = f"{self.config_entry.entry_id}_{self.config_entry.data['switch_name']}"
        _ = switch_entities.pop(current_entity_id, None)

        if user_input is not None:
            # Update the integration title if the name changed
            new_name = user_input["switch_name"]
            if new_name != self.config_entry.title:
                _ = self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    title=new_name
                )

            # Save linked_switch to options
            return self.async_create_entry(
                title="",
                data={
                    "switch_name": user_input.get("switch_name", self.config_entry.title),
                    "linked_switch": user_input.get("linked_switch")
                }
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("switch_name", default=self.config_entry.options.get("switch_name", self.config_entry.data["switch_name"])): str,
                vol.Optional("linked_switch", default=self.config_entry.options.get("linked_switch")): vol.In(switch_entities)
            }),
        )
