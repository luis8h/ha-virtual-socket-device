from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import callback
# Import the helper function
from homeassistant.helpers.event import async_track_state_change_event

DOMAIN = "virtual_socket_device"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switch from config entry."""
    switch_name = entry.data["switch_name"]
    async_add_entities([VirtualSocketSwitch(switch_name, entry)])

class VirtualSocketSwitch(SwitchEntity):
    """Virtual Socket Switch."""

    def __init__(self, name: str, entry):
        self._attr_name = name
        self._is_on = False
        self._entry = entry
        self._unique_id = f"{entry.entry_id}_{name}"
        self._unsub = None

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self):
        linked = self._entry.options.get("linked_switch")
        if linked:
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": linked}
            )
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        linked = self._entry.options.get("linked_switch")
        if linked:
            await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": linked}
            )
        self._is_on = False
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Subscribe to linked switch state changes."""
        linked = self._entry.options.get("linked_switch")
        if not linked:
            return

        # Use the helper function to track state changes for a specific entity.
        self._unsub = async_track_state_change_event(
            self.hass,
            [linked],
            self._state_listener,
        )

    # Use a regular callback function instead of a nested one.
    @callback
    def _state_listener(self, event):
        """Update when linked switch state changes."""
        new_state = event.data.get("new_state")
        if new_state:
            self._is_on = new_state.state == STATE_ON
            self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        """Clean up when entity is removed."""
        if self._unsub:
            self._unsub()
