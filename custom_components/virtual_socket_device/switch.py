from homeassistant.core import Event
from functools import cached_property
from typing import Any, override
from habluetooth.const import CALLBACK_TYPE
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import EventStateChangedData, async_track_state_change_event
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # pyright: ignore[reportUnusedParameter]
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up the virtual socket switch from a config entry."""
    switch_name = entry.data["switch_name"]
    async_add_entities([VirtualSocketSwitch(switch_name, entry)])


class VirtualSocketSwitch(SwitchEntity):
    """Virtual Socket Switch entity."""

    def __init__(self, name: str, entry: ConfigEntry):
        self._attr_name: str | None = name
        self._is_on: bool = False
        self._entry: ConfigEntry = entry
        self._unique_id: str = f"{entry.entry_id}_{name}"
        self._unsub: None | CALLBACK_TYPE = None

    @cached_property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    @override
    def is_on(self) -> bool:  # pyright: ignore[reportIncompatibleVariableOverride]
        return self._is_on

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        linked = self._get_linked_switch()
        if linked:
            _ = await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": linked}
            )
        self._is_on = True
        self.async_write_ha_state()

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        linked = self._get_linked_switch()
        if linked:
            _ = await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": linked}
            )
        self._is_on = False
        self.async_write_ha_state()

    @override
    async def async_added_to_hass(self) -> None:
        """Called when entity is added to Home Assistant."""
        # Listen for config entry updates
        _ = self._entry.add_update_listener(self._options_updated)
        await self._subscribe_to_linked_switch()

    async def _subscribe_to_linked_switch(self) -> None:
        """Subscribe to the linked switch, unsubscribe from old if necessary."""
        if self._unsub:
            self._unsub()
            self._unsub = None

        linked = self._get_linked_switch()
        if not linked:
            return

        self._unsub = async_track_state_change_event(
            self.hass,
            [linked],
            self._state_listener,
        )

    @callback
    def _state_listener(self, event: Event[EventStateChangedData]) -> None:
        """Update virtual switch state when linked switch changes."""
        new_state = event.data.get("new_state")
        if new_state:
            self._is_on = new_state.state == STATE_ON
            self.async_write_ha_state()

    @callback
    def _options_updated(self, hass: HomeAssistant, entry: ConfigEntry):  # pyright: ignore[reportUnusedParameter]
        """Handle config entry updates. Return coroutine for HA."""
        return self._handle_options_update(entry)

    async def _handle_options_update(self, entry: ConfigEntry) -> None:
        """Async part of options update."""
        # Update integration title if changed
        new_title = entry.options.get("switch_name") or entry.data.get("switch_name")
        if new_title != self._attr_name:
            self._attr_name = new_title
            self.async_write_ha_state()

        # Re-subscribe to linked switch
        await self._subscribe_to_linked_switch()

    def _get_linked_switch(self) -> str | None:
        """Return the linked switch entity_id, but avoid linking to itself."""
        linked = self._entry.options.get("linked_switch") or self._entry.data.get("linked_switch")
        if linked == self.entity_id:
            return None  # Prevent self-link
        return linked


    @override
    async def async_will_remove_from_hass(self) -> None:
        """Clean up subscriptions when entity is removed."""
        if self._unsub:
            self._unsub()
            self._unsub = None

